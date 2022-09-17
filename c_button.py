#!/usr/bin/env python3

__version__ = "1.0"
__author__ = "Aditya Marathe"
__email__ = "aditya.marathe09@gmail.com"

import tkinter as tk


class CustomButton(tk.Button):
    def __init__(self, *args, hover_bg=None, hover_fg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._default_bg, self._default_fg = self["bg"], self["fg"]

        self.hover_bg = hover_bg if hover_bg is not None else self._default_bg
        self.hover_fg = hover_fg if hover_fg is not None else self._default_fg

        self.bind("<Enter>", self.hover_event)
        self.bind("<Leave>", self.leave_event)

        self._command = kwargs.get("command", lambda: 0)
        self.bind("<Button-1>", self.exec_command, add=True)

    def hover_event(self, *_) -> None:
        self["bg"] = self.hover_bg
        self["fg"] = self.hover_fg

    def leave_event(self, *_) -> None:
        self["bg"] = self._default_bg
        self["fg"] = self._default_fg

    def exec_command(self, *_) -> str:
        self._command()
        self.hover_event()

        return "break"
