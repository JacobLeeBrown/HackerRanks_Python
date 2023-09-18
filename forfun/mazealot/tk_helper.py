from tkinter import Canvas


def rect(c: Canvas, x1: int, y1: int, x2: int, y2: int, color: str) -> None:
    c.create_rectangle(x1, y1, x2 - 1, y2 - 1, fill=color, outline=color)
