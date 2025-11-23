class PersistentCounter:
    def __init__(self, path: str, modulo: int = 500):
        self.path = path
        self.modulo = modulo
        self.value = self._read_and_increment()

    def _read_and_increment(self) -> int:
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
        return self.value % self.modulo == 0

    def get(self) -> int:
        return self.value
