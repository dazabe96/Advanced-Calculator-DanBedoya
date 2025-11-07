# Advanced Calculator project

# Advanced Calculator GUI
# Author: Dan Bedoya
# Description: A polished calculator app using tkinter with math validation and keyboard support.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ---------------------------
# Safe math evaluator
# ---------------------------
def safe_eval(expr: str):
    """
    Safely evaluates a math expression using only basic operators.
    It accepts digits, parentheses, decimals, and + - * / % .
    Returns the result or raises ValueError on invalid input.
    """
    allowed_chars = "0123456789.+-*/()% ×÷ "
    if any(c not in allowed_chars for c in expr):
        raise ValueError("Invalid character in expression")

    # Replace symbols for Python evaluation
    expr = expr.replace("×", "*").replace("÷", "/")

    # Prevent unsupported operators
    if "//" in expr or "**" in expr:
        raise ValueError("Unsupported operation")

    try:
        result = eval(expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        raise
    except Exception:
        raise ValueError("Malformed expression")
    return result

# ---------------------------
# Calculator App Class
# ---------------------------
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Advanced Calculator - Dan Bedoya")
        root.resizable(False, False)

        # Set ttk style
        style = ttk.Style(root)
        try:
            style.theme_use('clam')
        except Exception:
            pass

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Display entry
        self.display_var = tk.StringVar()
        self.display = ttk.Entry(main_frame, textvariable=self.display_var, font=("Consolas", 20), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="we", pady=(0, 8))
        self.display_var.set("0")

        # Last result label
        self.last_var = tk.StringVar()
        self.last_var.set("Last: ")
        self.last_label = ttk.Label(main_frame, textvariable=self.last_var, font=("Consolas", 9))
        self.last_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 6))

        # Button layout
        buttons = [
            ("C", 2, 0), ("⌫", 2, 1), ("%", 2, 2), ("÷", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
            ("±", 6, 0), ("0", 6, 1), (".", 6, 2), ("=", 6, 3)
        ]

        for (text, r, c) in buttons:
            b = ttk.Button(main_frame, text=text, command=lambda t=text: self.on_button(t))
            b.grid(row=r, column=c, padx=4, pady=4, ipadx=8, ipady=8, sticky="nsew")

        # Grid configuration for even resizing
        for i in range(4):
            main_frame.columnconfigure(i, weight=1)
        for i in range(2, 7):
            main_frame.rowconfigure(i, weight=1)

        # Keyboard bindings
        root.bind("<Return>", lambda e: self.on_button("="))
        root.bind("<BackSpace>", lambda e: self.on_button("⌫"))
        for key in "0123456789":
            root.bind(key, lambda e, k=key: self.on_button(k))
        for key in "+-*/%.":  # Allow keyboard math input
            root.bind(key, lambda e, k=key: self.on_button(k))
        root.bind("*", lambda e: self.on_button("×"))
        root.bind("/", lambda e: self.on_button("÷"))

        # Internal flag for last evaluation
        self.just_evaluated = False

    # ---------------------------
    def on_button(self, token):
        """Handle button presses"""
        cur = self.display_var.get()
        if cur == "0" and token not in ("C", "⌫", ".", "±"):
            cur = ""

        # Clear display
        if token == "C":
            self.display_var.set("0")
            return

        # Backspace
        if token == "⌫":
            new = cur[:-1] if len(cur) > 0 else ""
            self.display_var.set(new if new != "" else "0")
            return

        # Toggle sign
        if token == "±":
            try:
                if cur and cur != "0":
                    if cur.startswith("-"):
                        self.display_var.set(cur[1:])
                    else:
                        self.display_var.set("-" + cur)
            except Exception:
                pass
            return

        # Evaluate expression
        if token == "=":
            expr = cur
            try:
                result = safe_eval(expr)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.last_var.set(f"Last: {result}")
                self.display_var.set(str(result))
                self.just_evaluated = True
            except ZeroDivisionError:
                messagebox.showerror("Math error", "Division by zero")
                self.display_var.set("0")
            except ValueError:
                messagebox.showerror("Error", "Malformed expression")
            return

        # If just evaluated and typing a number, reset display
        if self.just_evaluated and token in "0123456789.":
            cur = ""
            self.just_evaluated = False

        # Prevent consecutive operators
        current_display = self.display_var.get()
        if current_display == "0" and token not in ("."):
            current_display = ""
        if token in "+-×÷*/%":
            if len(current_display) == 0:
                if token != "-":
                    return
            elif current_display[-1] in "+-×÷*/%":
                current_display = current_display[:-1]

        # Append token visually
        current_display += token
        self.display_var.set(current_display)
        self.just_evaluated = False


# ---------------------------
def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



