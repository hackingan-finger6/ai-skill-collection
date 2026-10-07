"""Inspect requirements and import one reviewed local skill; Python 3.10+."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import sys
import uuid


def plain_path(value):
    path = Path(os.path.abspath(value))
    for item in [*reversed(path.parents), path]:
        if not os.path.lexists(item):
            continue
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("linked path is unsupported: " + str(item))
    return path


def valid_name(value):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value):
        raise ValueError("invalid skill folder name")
    if value.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
        raise ValueError("reserved folder name")
    return value


def contents(value):
    base = plain_path(value)
    if not base.is_dir() or not (base / "SKILL.md").is_file():
        raise ValueError("source must contain SKILL.md")
    entries = []
    pending = [base]
    while pending:
        current = pending.pop()
        for item in sorted(current.iterdir(), key=lambda p: p.name):
            plain_path(item)
            if item.name == ".git":
                raise ValueError("Git metadata is unsupported")
            before = item.stat()
            relative = item.relative_to(base).as_posix()
            if item.is_dir():
                entries.append({"path": relative, "kind": "directory"})
                pending.append(item)
            elif stat.S_ISREG(before.st_mode):
                digest = hashlib.sha256()
                with item.open("rb") as stream:
                    for block in iter(lambda: stream.read(65536), b""):
                        digest.update(block)
                after = item.stat()
                if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                    raise ValueError("file changed while reading")
                entries.append({"path": relative, "kind": "file", "size": after.st_size, "sha256": digest.hexdigest()})
            else:
                raise ValueError("special file is unsupported")
    entries.sort(key=lambda row: row["path"])
    packed = json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"digest": hashlib.sha256(packed).hexdigest(), "entries": entries}


def probe(requirements):
    if not isinstance(requirements, dict):
        raise ValueError("requirements must be an object")
    valid_name(requirements.get("skill", ""))
    fields = {}
    for field in ("commands", "environment", "systems", "machines"):
        values = requirements.get(field, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values):
            raise ValueError(field + " must be a list of nonempty strings")
        fields[field] = values
    for command in fields["commands"]:
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]*", command):
            raise ValueError("commands must be bare executable names")
    for key in fields["environment"]:
        if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", key):
            raise ValueError("invalid environment variable name")
    commands = {command: bool(shutil.which(command)) for command in fields["commands"]}
    environment = {key: bool(os.environ.get(key)) for key in fields["environment"]}
    system, machine = platform.system(), platform.machine()
    compatible = (not fields["systems"] or system in fields["systems"]) and (not fields["machines"] or machine in fields["machines"])
    state = "platform_mismatch" if not compatible else "blocked" if not all([*commands.values(), *environment.values()]) else "conditions_present"
    return {"skill": requirements["skill"], "system": system, "machine": machine,
            "commands_present": commands, "environment_present": environment,
            "local_check": state, "agent_discovery": "unchecked", "authentication": "unchecked", "feature_execution": "unchecked"}


def add(source, root, name, reviewed_digest):
    origin, destination_root = plain_path(source), plain_path(root)
    valid_name(name)
    if not destination_root.is_dir() or destination_root == Path(destination_root.anchor):
        raise ValueError("installation root must be an existing non-volume directory")
    if origin == destination_root or origin in destination_root.parents or destination_root in origin.parents:
        raise ValueError("source and installation root must not overlap")
    destination = destination_root / name
    if os.path.lexists(destination):
        raise ValueError("destination already exists")
    snapshot = contents(origin)
    if snapshot["digest"] != reviewed_digest:
        raise ValueError("source differs from the reviewed digest")
    staging = destination_root / (".import-" + uuid.uuid4().hex)
    try:
        shutil.copytree(origin, staging)
        if contents(staging)["digest"] != reviewed_digest or contents(origin)["digest"] != reviewed_digest:
            raise ValueError("copy verification failed or source changed")
        if os.path.lexists(destination):
            raise ValueError("destination appeared during copy")
        os.rename(staging, destination)
    except Exception as error:
        raise RuntimeError(f"import failed; staging={staging}; {error}") from error
    return {"operation": "added", "path": str(destination), "digest": reviewed_digest, "agent_discovery": "unchecked"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    check = commands.add_parser("probe")
    check.add_argument("--requirements", required=True)
    review = commands.add_parser("review")
    review.add_argument("--source", required=True)
    install = commands.add_parser("add")
    install.add_argument("--source", required=True)
    install.add_argument("--root", required=True)
    install.add_argument("--name", required=True)
    install.add_argument("--reviewed-digest", required=True)
    args = parser.parse_args()
    try:
        if args.action == "probe":
            result = probe(json.loads(Path(args.requirements).read_text(encoding="utf-8-sig")))
        elif args.action == "review":
            result = contents(args.source)
        else:
            result = add(args.source, args.root, args.name, args.reviewed_digest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
