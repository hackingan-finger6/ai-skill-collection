"""Park one skill with an immutable receipt and restore it; Python 3.10+."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

KEEP = {"skill-creator", "skill-installer", "agent-skill-launcher", "agent-skill-vault"}


def folder_name(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}", value):
        raise ValueError("unsupported skill folder name")
    if value.upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
        raise ValueError("reserved skill folder name")
    return value


def physical(value):
    path = Path(os.path.abspath(value))
    for ancestor in [*reversed(path.parents), path]:
        if not os.path.lexists(ancestor):
            continue
        mode = ancestor.lstat()
        if stat.S_ISLNK(mode.st_mode) or getattr(mode, "st_file_attributes", 0) & 0x400:
            raise ValueError("link or reparse point is unsupported")
    return path


def directory(value):
    path = physical(value)
    if not path.is_dir() or path == Path(path.anchor):
        raise ValueError("expected an existing non-volume directory")
    return path


def signature(folder):
    base = directory(folder)
    if not (base / "SKILL.md").is_file():
        raise ValueError("SKILL.md is missing")
    lines = []
    queue = [base]
    while queue:
        parent = queue.pop(0)
        for member in sorted(parent.iterdir(), key=lambda p: p.name):
            physical(member)
            if member.name == ".git":
                raise ValueError("Git metadata is protected")
            info = member.stat()
            path = member.relative_to(base).as_posix()
            if stat.S_ISDIR(info.st_mode):
                lines.append([path, "dir"])
                queue.append(member)
            elif stat.S_ISREG(info.st_mode):
                checksum = hashlib.sha256()
                with member.open("rb") as handle:
                    for block in iter(lambda: handle.read(131072), b""):
                        checksum.update(block)
                finish = member.stat()
                if (info.st_ino, info.st_mtime_ns, info.st_size) != (finish.st_ino, finish.st_mtime_ns, finish.st_size):
                    raise ValueError("content changed during inventory")
                lines.append([path, "file", finish.st_size, checksum.hexdigest()])
            else:
                raise ValueError("non-regular entry is protected")
    serial = json.dumps(sorted(lines), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(serial).hexdigest()


def catalog(root):
    root = directory(root)
    records = []
    for child in sorted(root.iterdir(), key=lambda p: p.name):
        record = {"name": child.name, "path": str(child)}
        try:
            physical(child)
            if child.name.startswith("."):
                if child.is_dir():
                    records.append({**record, "protected": "hidden management area", "digest": None})
                continue
            if not child.is_dir() or not (child / "SKILL.md").is_file():
                continue
            value = signature(child)
            record.update(digest=value, protected="management helper" if child.name.lower() in KEEP else None)
        except (OSError, ValueError) as error:
            record.update(digest=None, protected=str(error))
        records.append(record)
    compact = [[r["name"], r["digest"], r["protected"]] for r in records]
    revision = hashlib.sha256(json.dumps(compact, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"root": str(root), "revision": revision, "items": records}


def locations(root, vault):
    root, vault = directory(root), directory(vault)
    if root == vault or root in vault.parents or vault in root.parents:
        raise ValueError("vault and root must be separate trees")
    if root.stat().st_dev != vault.stat().st_dev:
        raise ValueError("vault and root must share a filesystem")
    return root, vault


def check_audit(audit, inventory, target):
    if not isinstance(audit, dict) or audit.get("root") != inventory["root"] or audit.get("revision") != inventory["revision"]:
        raise ValueError("dependency audit does not match current inventory")
    if not isinstance(audit.get("scope"), str) or not audit["scope"].strip():
        raise ValueError("dependency investigation scope is required")
    graph = audit.get("references")
    names = {item["name"] for item in inventory["items"]}
    if not isinstance(graph, dict) or set(graph) != names:
        raise ValueError("dependency audit must cover every inventory item")
    for dependencies in graph.values():
        if not isinstance(dependencies, list) or any(not isinstance(name, str) or not name for name in dependencies):
            raise ValueError("invalid dependency list")
    retained = audit.get("retain", [])
    if not isinstance(retained, list) or any(not isinstance(name, str) or name not in names for name in retained):
        raise ValueError("invalid retained items")
    if target in retained or any(target in deps for caller, deps in graph.items() if caller != target):
        raise ValueError("item is retained or required by a remaining item")


def park(root, vault, name, expected, audit):
    folder_name(name)
    root, vault = locations(root, vault)
    inventory = catalog(root)
    check_audit(audit, inventory, name)
    found = [record for record in inventory["items"] if record["name"] == name]
    if len(found) != 1 or found[0]["protected"] or found[0]["digest"] != expected:
        raise ValueError("selected item is absent, protected, or changed")
    origin = physical(root / name)
    ticket = uuid.uuid4().hex
    slot = vault / ticket
    slot.mkdir()
    receipt = {"format": 1, "ticket": ticket, "root": str(root), "name": name,
               "digest": expected, "created_utc": datetime.now(timezone.utc).isoformat()}
    try:
        with (slot / "receipt.json").open("x", encoding="utf-8") as handle:
            json.dump(receipt, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        if signature(origin) != expected:
            raise ValueError("item changed before move")
        os.rename(origin, slot / "payload")
    except Exception as error:
        raise RuntimeError(f"park incomplete; ticket={ticket}; {error}") from error
    return {"operation": "parked", "ticket": ticket, "receipt": str(slot / "receipt.json"), "origin": str(origin)}


def ticket_data(root, vault, ticket):
    root, vault = locations(root, vault)
    if not re.fullmatch(r"[0-9a-f]{32}", ticket):
        raise ValueError("invalid ticket identifier")
    slot = directory(vault / ticket)
    data = json.loads(physical(slot / "receipt.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != 1 or data.get("ticket") != ticket or data.get("root") != str(root):
        raise ValueError("receipt is not bound to this ticket and root")
    name = data.get("name")
    folder_name(name)
    if name.lower() in KEEP:
        raise ValueError("invalid or protected original name")
    if not isinstance(data.get("digest"), str) or not re.fullmatch(r"[0-9a-f]{64}", data["digest"]):
        raise ValueError("invalid receipt digest")
    return data, physical(root / name), physical(slot / "payload")


def state_of(data, origin, payload):
    at_origin, in_vault = os.path.lexists(origin), os.path.lexists(payload)
    if at_origin and in_vault:
        return "conflict"
    if not at_origin and not in_vault:
        return "missing"
    if signature(origin if at_origin else payload) != data["digest"]:
        return "changed"
    return "at_origin" if at_origin else "parked"


def status(root, vault, ticket):
    data, origin, payload = ticket_data(root, vault, ticket)
    return {"ticket": ticket, "state": state_of(data, origin, payload), "origin": str(origin), "payload": str(payload)}


def restore(root, vault, ticket):
    data, origin, payload = ticket_data(root, vault, ticket)
    state = state_of(data, origin, payload)
    if state == "at_origin":
        return {"operation": "already_at_origin", "path": str(origin), "ticket": ticket}
    if state != "parked":
        raise ValueError("restore refused: " + state)
    if os.path.lexists(origin):
        raise ValueError("original path became occupied")
    os.rename(payload, origin)
    return {"operation": "restored", "path": str(origin), "ticket": ticket}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    listing = actions.add_parser("catalog")
    listing.add_argument("--root", required=True)
    move = actions.add_parser("park")
    for option in ("root", "vault", "name", "expected", "audit"):
        move.add_argument("--" + option, required=True)
    for action in ("status", "restore"):
        command = actions.add_parser(action)
        for option in ("root", "vault", "ticket"):
            command.add_argument("--" + option, required=True)
    args = parser.parse_args()
    try:
        if args.action == "catalog":
            result = catalog(args.root)
        elif args.action == "park":
            audit = json.loads(Path(args.audit).read_text(encoding="utf-8-sig"))
            result = park(args.root, args.vault, args.name, args.expected, audit)
        elif args.action == "status":
            result = status(args.root, args.vault, args.ticket)
        else:
            result = restore(args.root, args.vault, args.ticket)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
