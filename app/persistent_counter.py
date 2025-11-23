import os

class PersistentCounter:
    def __init__(self, path: str, modulo: int = 500):
        self.path = path
        self.modulo = modulo

    def _read_and_increment(self) -> int:
        if not os.path.exists(self.path):
            # Create file with 0 if it does not exist
            with open(self.path, "w") as f:
                f.write("0")
        try:
            with open(self.path, "r") as f:
                val = int(f.read().strip())
        except Exception:
            val = 0
        val += 1
        with open(self.path, "w") as f:
            f.write(str(val))
        return val

    def is_modulo(self) -> bool:
        return self._read_and_increment() % self.modulo == 0

