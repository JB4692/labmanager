import tkinter as tk
from gui.responsewindow import ResponseWindow
from gui.addtestwindow import AddTestWindow
from gui.adduserwindow import AddUserWindow
from utils.utils import \
	get_selected_items_from_listbox, \
	get_components, \
	get_users_names, \
	get_test_methods


class LabManagerGUI:
	def __init__(self, database) -> None:
		self.db = database

		self.root = tk.Tk()
		self.root.title("Lab Manager")
		entry_width = 10
		user_names = get_users_names(self.db)

		# VARIABLES
		self.submitter_var = tk.StringVar(value=get_users_names(self.db)[0])
		self.labware_num_var = tk.StringVar()
		self.lot_num_var = tk.StringVar()
		self.analyst_var = tk.StringVar(value=get_users_names(self.db)[0])
		self.tests_var = tk.StringVar()
		self.num_lenses_var = tk.IntVar()
		self.location_var = tk.StringVar(value='KOCG')
		self.comments_var = tk.StringVar()

		# WIDGETS
		# Menu Bar
		self.menu_bar = tk.Menu(self.root)

		file_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.menu_bar.add_cascade(label='File', menu=file_menu)
		file_menu.add_command(label='Open', command=lambda: print("pressed open"))  # make this do something?
		file_menu.add_command(label='Exit', command=self.root.destroy)

		options_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.menu_bar.add_cascade(label='Options', menu=options_menu)
		options_menu.add_command(label='Add Test', command=self.add_test)
		options_menu.add_command(label='Add User', command=self.add_new_employee_roles)
		options_menu.add_command(label='Remove Test', command=self.remove_test)
		options_menu.add_command(label='Remove User', command=self.remove_analyst)

		# Submitter
		submitter_label = tk.Label(self.root, text="Submitter:")
		submitter_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
		self.submitter_menu = tk.OptionMenu(self.root, self.submitter_var, *user_names)
		self.submitter_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')

		# Labware Number
		labware_num_label = tk.Label(self.root, text='Labware Number:')
		labware_num_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		self.labware_num_entry = tk.Entry(self.root, width=entry_width, textvariable=self.labware_num_var)
		self.labware_num_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

		# Lot Number
		lot_num_label = tk.Label(self.root, text='Lot Number:')
		lot_num_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
		self.lot_num_entry = tk.Entry(self.root, width=entry_width, textvariable=self.lot_num_var)
		self.lot_num_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

		# Tests
		tests_label = tk.Label(self.root, text="Tests:")
		tests_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
		self.tests_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=6)
		self.tests_listbox.grid(row=4, column=1, padx=5, pady=5, sticky='w')

		options = get_test_methods(self.db)
		for item in options:
			self.tests_listbox.insert(tk.END, item)

		# Number of lenses
		lenses_label = tk.Label(self.root, text='Number of Lenses:')
		lenses_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
		self.lenses_entry = tk.Entry(self.root,
									 width=entry_width,
									 textvariable=self.num_lenses_var)
		self.lenses_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

		# Location
		location_label = tk.Label(self.root, text="Location:")
		location_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
		self.location_menu = tk.OptionMenu(self.root, self.location_var, 'KOCG', 'ENCO')
		self.location_menu.grid(row=6, column=1, padx=5, pady=5, sticky='w')

		# Comments
		comments_label = tk.Label(self.root, text='Comments:')
		comments_label.grid(row=7, column=0, padx=5, pady=5, sticky='w')
		self.comments_box = tk.Text(self.root,
									width=50,
									height=5,
									wrap='word')
		self.comments_box.grid(row=7, column=1, padx=5, pady=5, sticky='w')

		# Submit and Cancel buttons
		btn_frame = tk.Frame(self.root)
		btn_frame.grid(row=8, column=0, columnspan=2)

		self.submit_btn = tk.Button(btn_frame, text="Submit", command=self.submit)
		self.submit_btn.pack(side="left", padx=5)

		self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel)
		self.cancel_btn.pack(side="left", padx=5)

		self.root.config(menu=self.menu_bar)

	def submit(self):
		# TODO commit the data to the db
		submitter = self.submitter_var.get()
		labware_num = self.labware_num_var.get()
		lot_num = self.lot_num_var.get()
		analyst = self.analyst_var.get()
		tests = get_selected_items_from_listbox(self.tests_listbox)
		if not tests:
			ResponseWindow(self.root, "You need to select at least one test.")
		num_lenses = self.lot_num_var.get()
		comments = self.comments_box.get("1.0", "end-1c")

		# commit the changes to the database
		if tests:
			print("Submitter:", submitter)
			print("Labware Number:", labware_num)
			print("Lot Number:", lot_num)
			print("Analyst:", analyst)
			print('Tests:', tests)
			print('Number of Lenses:', num_lenses)
			print('Comments:', comments)

	# self.db.create_submission(self, Submission)

	def cancel(self):
		# TODO ask the user if they are sure they want to quit. yes->close, no-> go back to main window.
		self.root.destroy()

	def add_new_employee_roles(self):
		AddUserWindow(self.root, self.db)

	def add_test(self):
		AddTestWindow(self.root, self.db)

	def add_submitter(self):
		pass

	def remove_analyst(self):
		pass

	def remove_submitter(self):
		pass

	def remove_test(self, test):
		self.db.remove_test(test)

	def run(self) -> None:
		self.root.mainloop()
