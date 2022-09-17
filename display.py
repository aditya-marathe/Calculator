#!/usr/bin/env python3

__version__ = "1.0"
__author__ = "Aditya Marathe"
__email__ = "aditya.marathe09@gmail.com"

__all__ = ("Symbol", "Point", "Number", "div_operator", "mul_operator",
           "sub_operator", "add_operator", "Equals", "Display")

import math

import tkinter as tk
from tkinter import messagebox


DECIMAL_PLACES = 9
MAX_CHAR_LIMIT = 11


def simplify(string: str | int | float) -> int | float:
    f = float(string)
    i = int(float(string))

    if i == f:
        return i

    return round(f, DECIMAL_PLACES)


class Symbol:
    pass


class Point(Symbol):
    def __str__(self):
        return "."


class Number(Symbol):
    def __init__(self, value: int | float):
        self.value = value

    def __str__(self):
        return str(self.value)


class Operator(Symbol):
    def __init__(self, value: str, func: callable):
        self.value = value
        self.func = func

        self.left = 0
        self.right = 0

    def eval(self) -> int | float:
        return simplify(self.func(self.left, self.right))

    def __str__(self):
        return f" {self.value} "


class Equals(Symbol):
    pass


div_operator = Operator("\u00f7", lambda l, r: l / r)
mul_operator = Operator("\u00d7", lambda l, r: l * r)
sub_operator = Operator("\u2212", lambda l, r: l - r)
add_operator = Operator("\u002b", lambda l, r: l + r)


class Display:
    def __init__(self, history: tk.StringVar, display: tk.StringVar) -> None:
        self.history_var = history
        self.display_var = display

        # Display
        self.display_str = "0"

        # History
        self.number_1 = ""
        self.number_2 = ""
        self.operator = ""
        self.equals = False
        self.answer_str = ""

        self.prev_answer = Number(0)

        # Flags
        self.decimal_used = False

        # Init
        self.update_display()

    def notify(self, symbol: Symbol) -> None:
        display_number = self.display_var.get()

        if isinstance(symbol, Number):
            if len(list(display_number)) > MAX_CHAR_LIMIT - 1:
                return

            if self.equals and not self.answer_str:
                self.answer_str = Number(simplify(display_number))
                self.display_str = str(symbol)
            elif self.display_str == "0":
                self.display_str = str(symbol)
            else:
                self.display_str += str(symbol)

        if isinstance(symbol, Point):
            if not self.decimal_used:
                self.display_str += str(symbol)
                self.decimal_used = True

        if isinstance(symbol, Operator):
            if self.equals:
                self.number_1 = Number(simplify(display_number))

                self.number_2 = ""
                self.answer_str = ""

                self.equals = False

            elif isinstance(self.operator, Operator):
                self.number_2 = Number(simplify(display_number))

                self.operator.right = self.number_2.value

                self.number_1 = Number(simplify(self.operator.eval()))
                self.number_2 = ""

            else:
                self.number_1 = Number(simplify(display_number))

            self.operator = symbol
            self.operator.left = self.number_1.value

            self.reset_display()
            self.decimal_used = False

        if isinstance(symbol, Equals):
            if not self.operator:
                self.number_1 = Number(simplify(display_number))
                self.operator = ""
                self.number_2 = ""
                self.answer_str = ""

                self.prev_answer = self.number_1
                self.display_str = str(self.number_1)

            elif isinstance(self.operator, Operator):
                self.number_2 = Number(simplify(display_number))

                self.operator.right = self.number_2.value

                try:
                    self.prev_answer = Number(simplify(self.operator.eval()))
                except Exception as e:
                    self.clear_all()
                    messagebox.showerror(f"Error!", str(e).capitalize() + ".")
                    return

                self.display_str = str(self.prev_answer)

            self.equals = True

            self.decimal_used = isinstance(self.prev_answer.value, float)

        self.update_display()
        self.update_history()

    def backspace(self) -> None:
        if self.display_str[-1] == ".":
            self.decimal_used = False

        if self.equals and not self.answer_str:
            self.answer_str = self.display_var.get()

        self.display_str = self.display_str[:-1]

        if not self.display_str:
            self.reset_display()

        self.update_display()
        self.update_history()

    def clear(self) -> None:
        if self.equals:
            self.answer_str = self.prev_answer
            self.update_history()

        self.reset_display()

        self.update_display()

        self.decimal_used = False

    def clear_all(self) -> None:
        self.prev_answer = Number(0)

        self.reset_display()
        self.reset_history()

        self.update_display()
        self.update_history()

        self.decimal_used = False

    def percentage(self) -> None:
        number = simplify(self.display_var.get())

        self.clear_all()

        self.notify(Number(number))
        self.notify(mul_operator)
        self.notify(Number(0.01))
        self.notify(Equals())

    def reciprocal(self) -> None:
        number = simplify(self.display_var.get())

        if isinstance(self.operator, Operator):
            self.operator.right = number
            number = simplify(self.operator.eval())

        self.clear_all()

        self.notify(Number(1))
        self.notify(div_operator)
        self.notify(Number(number))
        self.notify(Equals())

    def square(self) -> None:
        number = simplify(self.display_var.get())

        self.clear_all()

        self.notify(Number(number))
        self.notify(mul_operator)
        self.notify(Number(number))
        self.notify(Equals())

    def square_root(self) -> None:
        number = simplify(self.display_var.get())

        try:
            answer = Number(simplify(math.sqrt(number)))
        except ValueError:
            messagebox.showerror("Error!", "Operation not performed."
                                           "This app does not support complex numbers")
            return

        self.clear_all()

        self.notify(answer)

        self.equals = True
        self.number_1 = f"Sqrt({number})"
        self.answer_str = ""

        self.update_history()

        self.prev_answer = answer

    def toggle_sign(self) -> None:
        if self.equals:
            self.answer_str = self.prev_answer

        number = simplify(self.display_var.get())

        self.clear()

        self.notify(Number(-number))

    def reset_display(self) -> None:
        self.display_str = "0"

    def reset_history(self) -> None:
        self.number_1 = ""
        self.number_2 = ""
        self.operator = ""
        self.equals = False
        self.answer_str = ""

    def update_display(self) -> None:
        self.display_var.set(self.display_str)

    def update_history(self) -> None:
        equals = " = " if self.equals else ""
        self.history_var.set(
            str(self.number_1) +
            str(self.operator) +
            str(self.number_2) +
            equals + str(self.answer_str)
        )
