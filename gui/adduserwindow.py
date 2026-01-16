import tkinter as tk
import psycopg2
from .responsewindow import ResponseWindow
from db.manager import DBManager
from utils.utils import get_selected_items_from_listbox, get_components, validate_email


class AddUserWindow:
	def __init__(self, master_window: tk.Tk, database: DBManager):
		self.db = database
		self.new_window = tk.Toplevel(master_window)
		self.new_window.title('Add User')

		first_name_var = tk.StringVar()
		last_name_var = tk.StringVar()
		email_var = tk.StringVar()
		role_var = tk.StringVar()

		first_name_label = tk.Label(self.new_window, text='First Name:')
		first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		first_name_entry = tk.Entry(self.new_window, width=20, textvariable=first_name_var)
		first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

		last_name_label = tk.Label(self.new_window, text='Last Name:')
		last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
		last_name_entry = tk.Entry(self.new_window, width=20, textvariable=last_name_var)
		last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

		email_label = tk.Label(self.new_window, text='Email:')
		email_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
		email_entry = tk.Entry(self.new_window, width=20, textvariable=email_var)
		email_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

		role_label = tk.Label(self.new_window, text='Role:')
		role_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
		role_menu = tk.OptionMenu(self.new_window, role_var, 'Analyst', 'Submitter')
		role_menu.grid(row=4, column=1, padx=5, pady=5, sticky='w')

		btn_frame = tk.Frame(self.new_window)
		btn_frame.grid(row=5, column=0, columnspan=2)
		self.submit_btn = tk.Button(btn_frame,
									text="Add User",
									command=lambda: self.add_user(first_name_var.get(),
																  last_name_var.get(),
																  email_var.get(),
																  role_var.get()))
		self.submit_btn.pack(side="left", padx=5)
		self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.new_window.destroy)
		self.cancel_btn.pack(side="left", padx=5)

	def add_user(self, fname, lname, email, role):
		if validate_email(email):
			self.db.insert_users_table(fname, lname, email)
		else:
			print("Something went wrong,... uh oh. :c")