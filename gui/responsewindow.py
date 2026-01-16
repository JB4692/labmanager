import tkinter as tk
import psycopg2

"""
Used for response messages from the PostgreSQL server.
"""


class ResponseWindow:
	def __init__(self, master_window: tk.Tk | tk.Toplevel, message: str, error: psycopg2.Error | None = None):
		self.new_window = tk.Toplevel(master_window)
		self.new_window.title("Response")
		self.new_window.geometry("400x300")

		self.new_window.grid_rowconfigure(0, weight=1)
		self.new_window.grid_rowconfigure(1, weight=1)
		self.new_window.grid_columnconfigure(0, weight=1)

		label_frame = tk.Frame(self.new_window)
		label_frame.grid(row=0, column=0, sticky="nsew")
		label_frame.grid_rowconfigure(0, weight=1)
		label_frame.grid_columnconfigure(0, weight=1)

		label = tk.Label(label_frame, text=ResponseWindow.has_error(message, error), wraplength=200)
		label.grid(row=0, column=0)

		btn_frame = tk.Frame(self.new_window)
		btn_frame.grid(row=1, column=0, sticky="nsew")
		btn_frame.grid_rowconfigure(0, weight=1)
		btn_frame.grid_columnconfigure(0, weight=1)

		ok_btn = tk.Button(
			btn_frame,
			text="OK",
			command=lambda: self.pressed_ok()
		)
		ok_btn.grid(row=0, column=0)

	def pressed_ok(self):
		self.new_window.destroy()

	@staticmethod
	def has_error(msg: str, err: psycopg2.Error | None = None):
		if err:
			return msg + "\n" + str(err)
		else:
			return msg

