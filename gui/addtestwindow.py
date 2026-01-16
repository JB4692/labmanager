import tkinter as tk
from psycopg2 import Error
from .responsewindow import ResponseWindow
from db.manager import DBManager
from utils.utils import get_selected_items_from_listbox, get_components


class AddTestWindow:
	def __init__(self, master_window: tk.Tk, database: DBManager):
		self.db = database
		self.new_window = tk.Toplevel(master_window)
		self.new_window.title('Add New Test')

		test_num_var = tk.StringVar()
		test_name_var = tk.StringVar()
		solvent_var = tk.StringVar()
		# components taken from the listbox with get_selected_items

		r = 1  # row number

		test_num_label = tk.Label(self.new_window, text='Test Number:')
		test_num_label.grid(row=r, column=0, padx=5, pady=5, sticky='w')
		test_num_entry = tk.Entry(self.new_window, width=20, textvariable=test_num_var)
		test_num_entry.grid(row=r, column=1, padx=5, pady=5, sticky='w')
		r += 1

		test_name_label = tk.Label(self.new_window, text='Title:')
		test_name_label.grid(row=r, column=0, padx=5, pady=5, sticky='w')
		test_name_entry = tk.Entry(self.new_window, width=20, textvariable=test_name_var)
		test_name_entry.grid(row=r, column=1, padx=5, pady=5, sticky='w')
		r += 1

		solvent_label = tk.Label(self.new_window, text='Solvent:')
		solvent_label.grid(row=r, column=0, padx=5, pady=5, sticky='w')
		solvent_entry = tk.Entry(self.new_window, width=20, textvariable=solvent_var)
		solvent_entry.grid(row=r, column=1, padx=5, pady=5, sticky='w')
		r += 1

		components_label = tk.Label(self.new_window, text="Tests:")
		components_label.grid(row=r, column=0, padx=5, pady=5, sticky='w')
		components_listbox = tk.Listbox(self.new_window, selectmode=tk.MULTIPLE, height=6)
		components_listbox.grid(row=r, column=1, padx=5, pady=5, sticky='w')
		r += 1

		options = get_components(self.db)
		for item in options:
			components_listbox.insert(tk.END, item)

		btn_frame = tk.Frame(self.new_window)
		btn_frame.grid(row=r, column=0, columnspan=2, pady=0)
		add_btn = tk.Button(btn_frame,
							text="Add Test",
							command=lambda: self.create_test(
								test_num_var.get(),
								test_name_var.get(),
								solvent_var.get(),
								components_listbox))
		add_btn.pack(side="left", padx=5, pady=5)
		cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.new_window.destroy)
		cancel_btn.pack(side="left", padx=5, pady=5)

	def create_test(self, test_number: str, title: str, solvent: str, components_lb: tk.Listbox):
		components: list[str] = get_selected_items_from_listbox(components_lb)
		ret: bool
		error: Error
		ret, error = self.db.insert_tests_table(test_number.upper(), title, solvent, components)
		if ret:
			ResponseWindow(self.new_window, "Test was created successfully.", None)
		else:
			ResponseWindow(self.new_window, "Test creation was unsuccessful.", error)
