import os
import threading

os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from core import game
from core.ansi import PALETTE, Screen
from core.bridge import Bridge
from core.version import __version__

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "DejaVuSansMono.ttf")
CHAR_RATIO = 0.602
FIT_COLUMNS = 68
MIN_FONT = 7.0
MAX_FONT = 26.0
BACKGROUND = (0.04, 0.045, 0.06, 1)

CHIPS = (
    ("help", True),
    ("ls", True),
    ("cd ..", True),
    ("status", True),
    ("netmap", True),
    ("jobs", True),
    ("lay-low", True),
    ("ids", True),
    ("exploit ", False),
    ("crack ", False),
    ("ssh ", False),
    ("sudo ", False),
    ("cat ", False),
    ("cd ", False),
    ("pivot ", False),
    ("contest ", False),
    ("take ", False),
    ("complete ", False),
    ("persist ", False),
    ("reconnect", True),
    ("exit", True),
)


class TermLine(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._fit)

    def _fit(self, *_):
        self.text_size = self.size


Factory.register("TermLine", cls=TermLine)


class TermView(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RecycleBoxLayout(
            default_size=(None, dp(16)),
            default_size_hint=(1, None),
            size_hint=(1, None),
            orientation="vertical",
        )
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.layout.bind(height=self._pin)
        self.add_widget(self.layout)
        self.stick = True
        self.viewclass = "TermLine"
        self.bar_width = dp(4)
        self.scroll_type = ["bars", "content"]

    def _pin(self, *_):
        if self.stick:
            for delay in (0, 0.1, 0.3):
                Clock.schedule_once(self._bottom, delay)

    def _bottom(self, _dt):
        if self.stick:
            self.scroll_y = 0

    def on_touch_up(self, touch):
        result = super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            Clock.schedule_once(self._check_stick, 0.5)
        return result

    def _check_stick(self, _dt):
        self.stick = self.scroll_y <= 0.05 or self.layout.height <= self.height


class BlacknetApp(App):
    title = "BLACKNET"

    def build(self):
        Window.clearcolor = BACKGROUND
        Window.softinput_mode = "below_target"

        self.bridge = Bridge()
        self.screen = Screen(cols=FIT_COLUMNS)
        self.rendered_version = -1
        self.finished = False
        self.stop_at = None
        self.font_size = self._fit_font_size()

        root = BoxLayout(orientation="vertical", padding=dp(4), spacing=dp(4))

        top = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(4))
        top.add_widget(Label(
            text=f"BLACKNET v{__version__}",
            font_name=FONT,
            color=(0.55, 0.9, 1, 1),
            halign="left",
            valign="middle",
        ))
        smaller = Button(text="A-", size_hint_x=None, width=dp(48), font_name=FONT)
        larger = Button(text="A+", size_hint_x=None, width=dp(48), font_name=FONT)
        smaller.bind(on_release=lambda *_: self._resize_font(-1))
        larger.bind(on_release=lambda *_: self._resize_font(1))
        top.add_widget(smaller)
        top.add_widget(larger)
        root.add_widget(top)

        self.view = TermView()
        root.add_widget(self.view)

        chips_scroll = ScrollView(
            size_hint_y=None,
            height=dp(42),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=0,
        )
        chips = BoxLayout(size_hint=(None, 1), spacing=dp(4))
        chips.bind(minimum_width=chips.setter("width"))
        for text, send_now in CHIPS:
            btn = Button(
                text=text.strip(),
                size_hint=(None, 1),
                width=dp(24) + dp(10) * len(text.strip()),
                font_name=FONT,
            )
            btn.bind(on_release=lambda _b, t=text, s=send_now: self._chip(t, s))
            chips.add_widget(btn)
        chips_scroll.add_widget(chips)
        root.add_widget(chips_scroll)

        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(4))
        self.entry = TextInput(
            multiline=False,
            font_name=FONT,
            font_size=dp(16),
            hint_text="command",
            write_tab=False,
            keyboard_suggestions=False,
            background_color=(0.1, 0.11, 0.15, 1),
            foreground_color=(0.85, 0.85, 0.85, 1),
            cursor_color=(0.55, 0.9, 1, 1),
        )
        self.entry.bind(on_text_validate=self._submit)
        send = Button(text="Send", size_hint_x=None, width=dp(72), font_name=FONT)
        send.bind(on_release=self._submit)
        row.add_widget(self.entry)
        row.add_widget(send)
        root.add_widget(row)

        self._apply_font()
        return root

    def on_start(self):
        self.bridge.install()
        self.thread = threading.Thread(target=self._run_game, daemon=True)
        self.thread.start()
        Clock.schedule_interval(self._refresh, 0.1)
        Clock.schedule_once(lambda _dt: setattr(self.entry, "focus", True), 0.5)

    def on_pause(self):
        return True

    def on_stop(self):
        self.bridge.close()
        self.bridge.restore()

    def _run_game(self):
        try:
            game.run()
        except Exception as exc:
            self.bridge.write(f"\n[!] fatal error: {type(exc).__name__}: {exc}\n")
        finally:
            self.finished = True

    def _fit_font_size(self):
        size = Window.width / (FIT_COLUMNS * CHAR_RATIO)
        return max(MIN_FONT, min(MAX_FONT, size))

    def _resize_font(self, step):
        self.font_size = max(MIN_FONT, min(MAX_FONT, self.font_size + step))
        self._apply_font()
        self.rendered_version = -1

    def _apply_font(self):
        cols = max(20, int(Window.width / (self.font_size * CHAR_RATIO)) - 1)
        self.screen.cols = cols
        self.line_height = self.font_size * 1.25
        self.view.layout.default_size = (None, self.line_height)

    def _chip(self, text, send_now):
        if send_now:
            self.entry.text = ""
            self._send(text)
        else:
            self.entry.text = text
            self.entry.focus = True
            self.entry.cursor = (len(text), 0)

    def _submit(self, *_):
        text = self.entry.text
        self.entry.text = ""
        self._send(text)
        Clock.schedule_once(lambda _dt: setattr(self.entry, "focus", True), 0.1)

    def _send(self, text):
        if self.finished:
            return
        self.bridge.submit(text)

    def _refresh(self, _dt):
        chunk = self.bridge.drain()
        if chunk:
            self.screen.feed(chunk)

        if self.screen.version != self.rendered_version:
            self.rendered_version = self.screen.version
            rows = self.screen.markup_lines()
            color = PALETTE[None]
            self.view.data = [
                {
                    "text": row,
                    "markup": True,
                    "font_name": FONT,
                    "font_size": self.font_size,
                    "size_hint_y": None,
                    "height": self.line_height,
                    "halign": "left",
                    "valign": "middle",
                    "color": (
                        int(color[0:2], 16) / 255,
                        int(color[2:4], 16) / 255,
                        int(color[4:6], 16) / 255,
                        1,
                    ),
                }
                for row in rows
            ]

        if self.finished and not chunk and self.stop_at is None:
            self.stop_at = 15
        if self.stop_at is not None:
            self.stop_at -= 1
            if self.stop_at <= 0:
                self.stop()


if __name__ == "__main__":
    BlacknetApp().run()
