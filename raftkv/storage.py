"""持久化层: Raft hard state、日志条目、快照。

每个节点一个数据目录:
    hardstate.json   {"term": int, "voted_for": str|None}   —— 每次变更原子写入
    log.jsonl        每行一个日志条目 {"index","term","cmd"} —— 截断/快照时整体重写
    snapshot.json    {"last_included_index","last_included_term","config","data"}

所有写入均先写临时文件再 os.replace, 保证崩溃时不会留下半个文件。
"""

import json
import os


class Storage:
    def __init__(self, directory):
        self.dir = directory
        os.makedirs(directory, exist_ok=True)

    def _path(self, name):
        return os.path.join(self.dir, name)

    @staticmethod
    def _atomic_write(path, text):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)

    # ---------------- hard state ----------------
    def load_hard_state(self):
        try:
            with open(self._path("hardstate.json"), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {"term": 0, "voted_for": None}

    def save_hard_state(self, term, voted_for):
        self._atomic_write(
            self._path("hardstate.json"),
            json.dumps({"term": term, "voted_for": voted_for}),
        )

    # ---------------- log ----------------
    def load_log(self):
        entries = []
        try:
            with open(self._path("log.jsonl"), encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
        except FileNotFoundError:
            pass
        return entries

    def save_log(self, entries):
        text = "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries)
        self._atomic_write(self._path("log.jsonl"), text)

    # ---------------- snapshot ----------------
    def load_snapshot(self):
        try:
            with open(self._path("snapshot.json"), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def save_snapshot(self, snapshot):
        self._atomic_write(self._path("snapshot.json"),
                           json.dumps(snapshot, ensure_ascii=False))
