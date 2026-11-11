import re

PALETTE = {
    None: "c9d6e8",
    30: "5c6b82",
    31: "ff6b7a",
    32: "5be49b",
    33: "ffb547",
    34: "6c9cff",
    35: "ff7ad0",
    36: "5ce1ff",
    37: "e8f6ff",
    90: "7d8da6",
    91: "ff8a96",
    92: "7dffb4",
    93: "ffd27a",
    94: "8fb4ff",
    95: "ff9bd8",
    96: "9aefff",
    97: "ffffff",
}

FALLBACK = {
    "🟥": "R",
    "🟦": "B",
    "⬜": "G",
    "📡": "~",
    "🗃": "#",
    "🖥": "@",
    "❓": "?",
    "️": "",
}

STATUS_RE = re.compile(r"\[TARGET:([^\]]*)\](?: \[NODE:[^\]]*\])? \[TRACE:(\d+)\] \[REP:(-?\d+)\]")
CSI_RE = re.compile(r"\x1b\[([0-9;?]*)([A-Za-z])")
PARTIAL_RE = re.compile(r"\x1b(\[[0-9;?]*)?$")


def parse_status(lines):
    for line in reversed(lines[-60:]):
        m = STATUS_RE.search(line)
        if m:
            return m.group(1), int(m.group(2)), int(m.group(3))
    return None


def escape_markup(text):
    return text.replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;")


class Screen:
    def __init__(self, cols=80, max_lines=600):
        self.cols = cols
        self.max_lines = max_lines
        self.lines = [[]]
        self.row = 0
        self.col = 0
        self.fg = None
        self.pending = ""
        self.version = 0

    def _line(self):
        while self.row >= len(self.lines):
            self.lines.append([])
        return self.lines[self.row]

    def _newline(self):
        self.row += 1
        self.col = 0
        self._line()
        extra = len(self.lines) - self.max_lines
        if extra > 0:
            del self.lines[:extra]
            self.row -= extra

    def _put(self, ch):
        if self.cols and self.col >= self.cols:
            self._newline()
        line = self._line()
        while len(line) < self.col:
            line.append((" ", None))
        if self.col < len(line):
            line[self.col] = (ch, self.fg)
        else:
            line.append((ch, self.fg))
        self.col += 1

    def _sgr(self, params):
        codes = [int(p) for p in params.split(";") if p.isdigit()] or [0]
        for code in codes:
            if code in (0, 39):
                self.fg = None
            elif 30 <= code <= 37 or 90 <= code <= 97:
                self.fg = code

    def _csi(self, params, final):
        if final == "m":
            self._sgr(params)
        elif final == "J":
            if params in ("2", "3"):
                self.lines = [[]]
                self.row = 0
                self.col = 0
            elif params in ("", "0"):
                line = self._line()
                del line[self.col:]
                del self.lines[self.row + 1:]
        elif final == "H":
            self.row = 0
            self.col = 0
            self._line()
        elif final == "K":
            line = self._line()
            if params in ("", "0"):
                del line[self.col:]
            elif params == "2":
                del line[:]

    def feed(self, text):
        if not text:
            return
        text = self.pending + text
        self.pending = ""
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == "\x1b":
                m = CSI_RE.match(text, i)
                if m:
                    self._csi(m.group(1), m.group(2))
                    i = m.end()
                    continue
                if PARTIAL_RE.match(text, i):
                    self.pending = text[i:]
                    break
                i += 1
                continue
            if ch == "\n":
                self._newline()
            elif ch == "\r":
                self.col = 0
            elif ch == "\b":
                self.col = max(0, self.col - 1)
            elif ch == "\t":
                for _ in range(8 - self.col % 8):
                    self._put(" ")
            elif ch >= " " and ch != "\x7f":
                self._put(ch)
            i += 1
        self.version += 1

    def plain_lines(self):
        return ["".join(c for c, _ in line) for line in self.lines]

    def markup_lines(self):
        out = []
        for line in self.lines:
            parts = []
            run = []
            run_fg = object()
            for ch, fg in line:
                ch = FALLBACK.get(ch, ch)
                if fg != run_fg and run:
                    parts.append(self._wrap("".join(run), run_fg))
                    run = []
                run_fg = fg
                run.append(ch)
            if run:
                parts.append(self._wrap("".join(run), run_fg))
            out.append("".join(parts) if parts else " ")
        return out

    @staticmethod
    def _wrap(text, fg):
        body = escape_markup(text)
        if fg is None:
            return body
        return f"[color=#{PALETTE.get(fg, PALETTE[None])}]{body}[/color]"
