import os



class PersistentCounter:
    def __init__(self, path: str, limit: int = 500):
        self.path = path
        self.limit = limit

    def read(self) -> int:
        """Read the current value from file, create file with 0 if not exists."""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                f.write("0")
            return 0
        try:
            with open(self.path, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def write(self, value: int):
        """Write the given value to the file."""
        with open(self.path, "w") as f:
            f.write(str(value))

    def increment_and_check(self) -> bool:
        """
        Increment the value in the file by 1. If the new value is greater than limit, reset to 0 and return True.
        Otherwise, save incremented value and return False.
        """
        val = self.read()
        val += 1
        if val > self.limit:
            self.write(0)
            return True
        else:
            self.write(val)
            return False

