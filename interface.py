#!/usr/bin/env python3

__version__ = "1.0"
__author__ = "Aditya Marathe"
__email__ = "aditya.marathe09@gmail.com"

import tkinter as tk

from c_button import CustomButton
from display import *

SMALL_FONT = ("Segoe UI Semilight", 14)
MEDIUM_FONT = ("Segoe UI Semilight", 15)
LARGE_FONT = ("Segoe UI Semilight", 40)

WHITE = "#FFFFFF"
BLACK = "#000000"
SLATE = "#212121"
GREY = "#363636"
LIGHT_GREY = "#404040"
BLUE = "#4aaeff"
LIGHT_BLUE = "#53b0fc"


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.width, self.height = 325, 500
        self.SCR_WIDTH = self.winfo_screenwidth()
        self.SCR_HEIGHT = self.winfo_screenheight()
        x = (self.SCR_WIDTH - self.width) // 2
        y = (self.SCR_HEIGHT - self.height) // 2

        # Hides window
        self.attributes("-alpha", 0)

        # Window
        self.title("Calculator")
        self.iconphoto(True, tk.PhotoImage(file="logo.png"))
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.minsize(self.width, self.height)

        self.configure(bg=SLATE)

        self.init_layout()

        # Widgets
        self.history = tk.StringVar(self)
        tk.Label(
            self,
            textvariable=self.history,
            font=MEDIUM_FONT,
            justify=tk.RIGHT,
            bg=SLATE, fg=WHITE
        ).grid(row=0, columnspan=4, sticky=tk.E, padx=5, pady=(5, 0))

        self.display = tk.StringVar(self)
        tk.Entry(
            self,
            textvariable=self.display,
            justify=tk.RIGHT,
            font=LARGE_FONT,
            state=tk.DISABLED,
            relief=tk.FLAT,
            disabledbackground=SLATE,
            disabledforeground=WHITE
        ).grid(row=1, columnspan=4, sticky=tk.NSEW, padx=5)

        # Display object
        self.display_manager = Display(self.history, self.display)

        # Input buttons
        buttons = {
            "%": (lambda: self.display_manager.percentage(), "%"),
            "AC": (lambda: self.display_manager.clear_all(), "Delete"),
            "C": (lambda: self.display_manager.clear(), "c"),
            "⌫": (lambda: self.display_manager.backspace(), "BackSpace"),  # Alternative: \u2190
            "\xb9\u2044\u2093": (lambda: self.display_manager.reciprocal(), "r"),
            "x\xb2": (lambda: self.display_manager.square(), "s"),
            "\u221ax": (lambda: self.display_manager.square_root(), "r"),
            "\u00f7": (lambda: self.display_manager.notify(div_operator), "/"),
            "7": (lambda: self.display_manager.notify(Number(7)), "7"),
            "8": (lambda: self.display_manager.notify(Number(8)), "8"),
            "9": (lambda: self.display_manager.notify(Number(9)), "9"),
            "\u00d7": (lambda: self.display_manager.notify(mul_operator), "*"),
            "4": (lambda: self.display_manager.notify(Number(4)), "4"),
            "5": (lambda: self.display_manager.notify(Number(5)), "5"),
            "6": (lambda: self.display_manager.notify(Number(6)), "6"),
            "\u2212": (lambda: self.display_manager.notify(sub_operator), "minus"),
            "1": (lambda: self.display_manager.notify(Number(1)), "1"),
            "2": (lambda: self.display_manager.notify(Number(2)), "2"),
            "3": (lambda: self.display_manager.notify(Number(3)), "3"),
            "\u002b": (lambda: self.display_manager.notify(add_operator), "plus"),
            "+/-": (lambda: self.display_manager.toggle_sign(), "_"),
            "0": (lambda: self.display_manager.notify(Number(0)), "0"),
            ".": (lambda: self.display_manager.notify(Point()), "."),
            "\u003d": (lambda: self.display_manager.notify(Equals()), "=")
        }

        row, col = 0, 0
        for i, (button, (command, keybind)) in enumerate(buttons.items()):
            extra_pad_x = (0, 0)

            if not i % 4:
                row += 1
                extra_pad_x = (4, 0)

            extra_pad_y = 4 if row == 6 else 0
            extra_pad_x = (0, 4) if col == 3 else extra_pad_x

            col = 0 if col == 4 else col

            fg = WHITE

            if (i < 8) or (i in [11, 15, 19]):
                bg = GREY
                hover_bg = LIGHT_GREY

            elif i == len(buttons) - 1:
                bg = LIGHT_BLUE
                hover_bg = BLUE
                fg = BLACK
            else:
                bg = LIGHT_GREY
                hover_bg = GREY

            button = CustomButton(
                self,
                text=button,
                font=SMALL_FONT,
                relief=tk.FLAT,
                bg=bg, fg=fg,
                hover_bg=hover_bg,
                command=command
            )
            button.grid(
                row=row + 2,
                column=col,
                sticky=tk.NSEW,
                padx=(2 + extra_pad_x[0], 2 + extra_pad_x[1]),
                pady=(2, 2 + extra_pad_y)
            )

            if keybind is not None:
                self.bind_all(f"<KeyPress-{keybind}>", button.exec_command)
                self.bind_all(f"<KeyRelease-{keybind}>", button.leave_event)

            col += 1

        # Shows window
        self.after(350, lambda *_: self.attributes("-alpha", 1))

    def init_layout(self) -> None:
        # Grid Layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=0)
        for n in range(6):
            self.grid_rowconfigure(n + 3, weight=1)

        for n in range(4):
            self.grid_columnconfigure(n, weight=1)
