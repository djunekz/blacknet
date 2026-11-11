import os
import threading

os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from core import game
from core.ansi import PALETTE, Screen, parse_status
from core.bridge import Bridge
from core.version import __version__

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "assets", "DejaVuSansMono.ttf")
ICON = os.path.join(HERE, "assets", "icon.png")
CHAR_RATIO = 0.602
FIT_COLUMNS = 68
MIN_FONT = 7.0
MAX_FONT = 26.0

BACKGROUND = (0.027, 0.043, 0.078, 1)
CARD = (0.055, 0.086, 0.153, 1)
PANEL = (0.039, 0.063, 0.118, 1)
LINE = (0.106, 0.165, 0.267, 1)
CYAN = (0.361, 0.882, 1, 1)
CYAN_DARK = (0.016, 0.125, 0.165, 1)
TEXT = (0.788, 0.839, 0.910, 1)
WHITE = (0.91, 0.965, 1, 1)
DIM = (0.49, 0.553, 0.651, 1)
AMBER = (1, 0.71, 0.278, 1)
RED = (1, 0.42, 0.478, 1)
GREEN = (0.357, 0.894, 0.608, 1)

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


class Text(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", FONT)
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "middle")
        kwargs.setdefault("markup", True)
        super().__init__(**kwargs)
        self.bind(size=self._fit)

    def _fit(self, *_):
        self.text_size = self.size


class TermLine(Text):
    pass


Factory.register("TermLine", cls=TermLine)


class Card(BoxLayout):
    def __init__(self, fill=CARD, line=LINE, radius=12, **kwargs):
        super().__init__(**kwargs)
        self.radius = dp(radius)
        with self.canvas.before:
            self._fill_color = Color(*fill)
            self._fill = RoundedRectangle(radius=[self.radius])
            self._line_color = Color(*line)
            self._line = Line(width=1)
        self.bind(pos=self._sync, size=self._sync)

    def set_line(self, color):
        self._line_color.rgba = color

    def _sync(self, *_):
        self._fill.pos = self.pos
        self._fill.size = self.size
        self._line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)


class Pill(Button):
    def __init__(self, fill=CARD, line=LINE, color=TEXT, radius=22, **kwargs):
        kwargs.setdefault("font_name", FONT)
        super().__init__(
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=color,
            **kwargs,
        )
        self.base_fill = fill
        self.radius = dp(radius)
        with self.canvas.before:
            self._fill_color = Color(*fill)
            self._fill = RoundedRectangle(radius=[self.radius])
            self._line_color = Color(*line)
            self._line = Line(width=1)
        self.bind(pos=self._sync, size=self._sync, state=self._sync)

    def _sync(self, *_):
        base = self.base_fill
        if self.state == "down":
            self._fill_color.rgba = tuple(min(1, c + 0.12) for c in base[:3]) + (1,)
        else:
            self._fill_color.rgba = base
        self._fill.pos = self.pos
        self._fill.size = self.size
        self._line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)


class Bar(Widget):
    value = NumericProperty(0)
    tint = ListProperty(AMBER)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(*LINE)
            self._track = RoundedRectangle(radius=[dp(3)])
            self._fill_color = Color(*AMBER)
            self._fill = RoundedRectangle(radius=[dp(3)])
        self.bind(pos=self._sync, size=self._sync, value=self._sync, tint=self._sync)

    def _sync(self, *_):
        self._track.pos = self.pos
        self._track.size = self.size
        ratio = max(0, min(100, self.value)) / 100
        width = self.width * ratio
        if self.value > 0:
            width = max(width, dp(6))
        self._fill.pos = self.pos
        self._fill.size = (width, self.height)
        self._fill_color.rgba = self.tint


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
        self.bar_width = dp(3)
        self.bar_color = CYAN[:3] + (0.6,)
        self.bar_inactive_color = CYAN[:3] + (0.2,)
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
    icon = ICON

    def build(self):
        Window.clearcolor = BACKGROUND
        Window.softinput_mode = "below_target"

        self.bridge = Bridge()
        self.screen = Screen(cols=FIT_COLUMNS)
        self.rendered_version = -1
        self.finished = False
        self.stop_at = None
        self.font_size = self._fit_font_size()

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(12), dp(10), dp(12), dp(10)],
            spacing=dp(10),
        )

        root.add_widget(self._build_header())
        root.add_widget(self._build_hud())

        panel = Card(
            fill=PANEL,
            line=LINE,
            radius=16,
            padding=[dp(10), dp(10), dp(6), dp(10)],
        )
        self.view = TermView()
        panel.add_widget(self.view)
        root.add_widget(panel)

        root.add_widget(self._build_chips())
        root.add_widget(self._build_input())

        self._apply_font()
        return root

    def _build_header(self):
        header = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        logo = Image(source=ICON, size_hint=(None, 1), width=dp(40), fit_mode="contain")
        header.add_widget(logo)

        titles = BoxLayout(orientation="vertical", spacing=dp(2))
        titles.add_widget(Text(
            text="B L A C K N E T",
            font_size=dp(18),
            color=WHITE,
        ))
        titles.add_widget(Text(
            text=f"v{__version__} / underground access",
            font_size=dp(10),
            color=DIM,
        ))
        header.add_widget(titles)

        smaller = Pill(text="A-", size_hint=(None, None), size=(dp(44), dp(44)), radius=12, font_size=dp(14))
        larger = Pill(text="A+", size_hint=(None, None), size=(dp(44), dp(44)), radius=12, font_size=dp(16))
        smaller.bind(on_release=lambda *_: self._resize_font(-1))
        larger.bind(on_release=lambda *_: self._resize_font(1))
        header.add_widget(smaller)
        header.add_widget(larger)
        return header

    def _build_hud(self):
        hud = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(8))

        target = Card(orientation="vertical", size_hint_x=1.5, padding=[dp(10), dp(6)], spacing=dp(2))
        target.add_widget(Text(text="TARGET", font_size=dp(9), color=DIM))
        self.target_value = Text(text="LOCAL", font_size=dp(13), color=CYAN)
        target.add_widget(self.target_value)

        trace = Card(orientation="vertical", size_hint_x=1.6, padding=[dp(10), dp(6)], spacing=dp(4))
        row = BoxLayout()
        row.add_widget(Text(text="TRACE", font_size=dp(9), color=DIM))
        self.trace_value = Text(text="0%", font_size=dp(10), color=AMBER, halign="right")
        row.add_widget(self.trace_value)
        trace.add_widget(row)
        self.trace_bar = Bar(size_hint_y=None, height=dp(6))
        trace.add_widget(self.trace_bar)

        rep = Card(orientation="vertical", size_hint_x=1, padding=[dp(10), dp(6)], spacing=dp(2))
        rep.add_widget(Text(text="REP", font_size=dp(9), color=DIM))
        self.rep_value = Text(text="0", font_size=dp(13), color=GREEN)
        rep.add_widget(self.rep_value)

        hud.add_widget(target)
        hud.add_widget(trace)
        hud.add_widget(rep)
        return hud

    def _build_chips(self):
        scroll = ScrollView(
            size_hint_y=None,
            height=dp(46),
            do_scroll_x=True,
            do_scroll_y=False,
            bar_width=0,
        )
        chips = BoxLayout(size_hint=(None, 1), spacing=dp(8), padding=[0, dp(1)])
        chips.bind(minimum_width=chips.setter("width"))
        for index, (text, send_now) in enumerate(CHIPS):
            label = text.strip()
            primary = index == 0
            btn = Pill(
                text=label,
                size_hint=(None, None),
                size=(dp(30) + dp(9) * len(label), dp(44)),
                fill=CARD,
                line=CYAN if primary else LINE,
                color=CYAN if primary else TEXT,
                font_size=dp(13),
            )
            btn.bind(on_release=lambda _b, t=text, s=send_now: self._chip(t, s))
            chips.add_widget(btn)
        scroll.add_widget(chips)
        return scroll

    def _build_input(self):
        row = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(8))
        field = Card(radius=16, padding=[dp(14), 0, dp(6), 0], spacing=dp(6))
        field.add_widget(Text(
            text="$",
            font_size=dp(15),
            color=CYAN,
            size_hint_x=None,
            width=dp(14),
        ))
        self.entry = TextInput(
            multiline=False,
            font_name=FONT,
            font_size=dp(15),
            hint_text="command",
            hint_text_color=DIM,
            write_tab=False,
            keyboard_suggestions=False,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            foreground_color=TEXT,
            cursor_color=CYAN,
            padding=[dp(2), dp(16), dp(2), dp(10)],
        )
        self.entry.bind(on_text_validate=self._submit)
        self.entry.bind(focus=lambda _w, value: field.set_line(CYAN if value else LINE))
        field.add_widget(self.entry)

        send = Pill(
            text="→",
            size_hint=(None, None),
            size=(dp(54), dp(54)),
            fill=CYAN,
            line=CYAN,
            color=CYAN_DARK,
            radius=16,
            font_size=dp(24),
        )
        send.bind(on_release=self._submit)
        row.add_widget(field)
        row.add_widget(send)
        return row

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

    def _text_width(self):
        return max(dp(100), Window.width - dp(24) - dp(16) - dp(10) - dp(6))

    def _fit_font_size(self):
        size = self._text_width() / (FIT_COLUMNS * CHAR_RATIO)
        return max(MIN_FONT, min(MAX_FONT, size))

    def _resize_font(self, step):
        self.font_size = max(MIN_FONT, min(MAX_FONT, self.font_size + step))
        self._apply_font()
        self.rendered_version = -1

    def _apply_font(self):
        cols = max(20, int(self._text_width() / (self.font_size * CHAR_RATIO)))
        self.screen.cols = cols
        self.line_height = self.font_size * 1.3
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

    def _update_hud(self):
        status = parse_status(self.screen.plain_lines())
        if not status:
            return
        target, trace, rep = status
        self.target_value.text = target or "LOCAL"
        self.trace_value.text = f"{trace}%"
        self.trace_bar.value = trace
        tint = RED if trace >= 70 else AMBER
        self.trace_bar.tint = list(tint)
        self.trace_value.color = tint
        self.rep_value.text = str(rep)

    def _refresh(self, _dt):
        chunk = self.bridge.drain()
        if chunk:
            self.screen.feed(chunk)

        if self.screen.version != self.rendered_version:
            self.rendered_version = self.screen.version
            rows = self.screen.markup_lines()
            color = PALETTE[None]
            base = (
                int(color[0:2], 16) / 255,
                int(color[2:4], 16) / 255,
                int(color[4:6], 16) / 255,
                1,
            )
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
                    "color": base,
                }
                for row in rows
            ]
            self._update_hud()

        if self.finished and not chunk and self.stop_at is None:
            self.stop_at = 15
        if self.stop_at is not None:
            self.stop_at -= 1
            if self.stop_at <= 0:
                self.stop()


if __name__ == "__main__":
    BlacknetApp().run()
