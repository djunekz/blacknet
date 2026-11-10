import builtins
import queue
import sys
import threading


class Bridge:
    def __init__(self):
        self._lock = threading.Lock()
        self._chunks = []
        self._inputs = queue.Queue()
        self.closed = False
        self._saved = None

    def write(self, text):
        if text:
            with self._lock:
                self._chunks.append(str(text))
        return len(text) if text else 0

    def flush(self):
        return None

    def isatty(self):
        return False

    def drain(self):
        with self._lock:
            text = "".join(self._chunks)
            self._chunks = []
        return text

    def submit(self, text):
        self.write(text + "\n")
        self._inputs.put(text)

    def close(self):
        self.closed = True
        self._inputs.put(None)

    def input(self, prompt=""):
        if self.closed:
            raise EOFError
        self.write(prompt)
        item = self._inputs.get()
        if item is None:
            self._inputs.put(None)
            raise EOFError
        return item

    def install(self):
        self._saved = (sys.stdout, sys.stderr, builtins.input)
        sys.stdout = self
        sys.stderr = self
        builtins.input = self.input

    def restore(self):
        if self._saved:
            sys.stdout, sys.stderr, builtins.input = self._saved
            self._saved = None
