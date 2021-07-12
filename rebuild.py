#!/usr/bin/python3
import re
import hashlib
import json
import os
import sys
from pathlib import Path

assert len(sys.argv) == 2
name = sys.argv[1]
assert re.search(r"^[a-z]+$", name)
tsv_file = Path(name + ".tsv")
assert tsv_file.exists()

items = []
with tsv_file.open() as f:
    for line in f:
        emoji, keywords = line.rstrip("\n").split("\t", maxsplit=1)
        md5 = hashlib.md5(emoji.encode()).hexdigest()
        icon = " "
        if re.search(r"^[a-zA-Z0-9]+$", emoji):
            icon_file = Path(f"{name}/{emoji}.png")
            if icon_file.exists():
                icon = str(icon_file)
        items.append(
            dict(
                uid=md5,
                title=emoji,
                subtitle=keywords,
                arg=emoji,
                match=keywords,
                icon=dict(path=icon),
            )
        )

cache_file = Path(f"{name}-do-not-edit.json")
cache_file.parent.mkdir(parents=True, exist_ok=True)
with cache_file.open("w") as f:
    json.dump(dict(items=items), f, separators=(",", ":"))
