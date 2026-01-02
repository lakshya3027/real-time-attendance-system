import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2


def get_button(window, text, color, command, fg='white'):
    return tk.Button(
        window,
        text=text,
        bg=color,
        fg=fg,
        command=command,
        height=2,
        width=20,
        font=('Arial', 20)
    )


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=('Arial', 20), justify='left')
    return label


def get_entry_text(window):
    return tk.Text(window, height=1, width=20, font=('Arial', 20))


def msg_box(title, description):
    messagebox.showinfo(title, description)


def cv2_to_tk(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    return ImageTk.PhotoImage(img)
