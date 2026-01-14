import tkinter as tk
from utils.utils import Submission

class LabManagerGUI:
	def __init__(self, database) -> None:
		self.root = tk.Tk()
		self.db = database
	
		self.root.title("Lab Manager")
		entry_width = 10
		user_names = self.get_users_names()

		# VARIABLES
		self.submitter_var = tk.StringVar(value=self.get_users_names()[0])
		self.labware_num_var = tk.StringVar()
		self.lot_num_var = tk.StringVar()
		self.analyst_var = tk.StringVar(value=self.get_users_names()[0])
		self.tests_var = tk.StringVar()
		self.num_lenses_var = tk.IntVar()
		self.location_var = tk.StringVar(value='KOCG')
		self.comments_var = tk.StringVar()

		# WIDGETS
		# Menu Bar
		self.menu_bar = tk.Menu(self.root)

		file_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.menu_bar.add_cascade(label='File', menu=file_menu)
		file_menu.add_command(label='Open', command= lambda: print("pressed open"))
		file_menu.add_command(label='Exit', command=self.root.destroy)
		
		options_menu = tk.Menu(self.menu_bar, tearoff=False)
		self.menu_bar.add_cascade(label='Options', menu=options_menu)
		options_menu.add_command(label='Add New Analyst/Submitter', command=self.add_new_employee_roles)
		options_menu.add_command(label='Add New Test', command=self.add_test)
		options_menu.add_command(label='Remove Analyst/Submitter', command=self.remove_analyst)
		options_menu.add_command(label='Remove Test', command=self.remove_test)

		# Submitter
		submitter_label = tk.Label(self.root, text="Submitter:")
		submitter_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
		self.submitter_menu = tk.OptionMenu(self.root, self.submitter_var, *user_names)
		self.submitter_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')
		
		# Labware Number
		labware_num_label = tk.Label(self.root, text='Labware Number:')
		labware_num_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		self.labware_num_entry = tk.Entry(self.root, width=entry_width, textvariable= self.labware_num_var)
		self.labware_num_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
		
		# Lot Number
		lot_num_label = tk.Label(self.root, text='Lot Number:')
		lot_num_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
		self.lot_num_entry = tk.Entry(self.root, width=entry_width, textvariable= self.lot_num_var)
		self.lot_num_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

		# Tests
		tests_label = tk.Label(self.root, text="Tests:")
		tests_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
		self.tests_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=6)
		self.tests_listbox.grid(row=4, column=1, padx=5, pady=5, sticky='w')

		options = self.get_test_methods()
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
		#TODO commit the data to the db
		submitter = self.submitter_var.get()
		labware_num = self.labware_num_var.get()
		lot_num = self.lot_num_var.get()
		analyst = self.analyst_var.get()
		tests = self.get_selected_tests()
		if tests == []:
			self.prompt_box("You need to select at least one test.")
		num_lenses = self.lot_num_var.get()
		comments = self.comments_box.get("1.0", "end-1c")

		#commit the changes to the database
		if tests != []:
			print("Submitter:", submitter)
			print("Labware Number:", labware_num)
			print("Lot Number:", lot_num)
			print("Analyst:", analyst)
			print('Tests:', tests)
			print('Number of Lenses:', num_lenses)
			print('Comments:', comments)
		
		# self.db.create_submission(self, Submission)
	
	def cancel(self):
		#TODO ask the user if they are sure they want to quit. yes->close, no-> go back to main window.
		self.root.destroy()
	
	def get_users_names(self) -> list[str]:
		# return ['testname']
		return self.db.get_users_names()

	def get_test_methods(self) -> list[str]:
		# return ['test1']
		return self.db.get_tests()
	
	def get_selected_tests(self):
		selected_indicies = self.tests_listbox.curselection()
		selected_tests = [self.tests_listbox.get(i) for i in selected_indicies]
		return selected_tests

	def add_new_employee_roles(self):
		def commit_analyst(name, email, role):
			self.db.insert_employee_table(name, email, role)
		
		new_window = tk.Toplevel(self.root)
		new_window.title('Add Analyst/Submitter')

		first_name_var = tk.StringVar()
		last_name_var = tk.StringVar()
		email_var = tk.StringVar()
		role_var = tk.StringVar()

		first_name_label = tk.Label(new_window, text='First Name:')
		first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		first_name_entry = tk.Entry(new_window, width=20, textvariable= first_name_var)
		first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

		last_name_label = tk.Label(new_window, text='Last Name:')
		last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
		last_name_entry = tk.Entry(new_window, width=20, textvariable= last_name_var)
		last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

		email_label = tk.Label(new_window, text='Email:')
		email_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
		email_entry = tk.Entry(new_window, width=20, textvariable= email_var)
		email_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

		role_label = tk.Label(new_window, text='Role:')
		role_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
		role_menu = tk.OptionMenu(new_window, role_var, 'Analyst', 'Submitter')
		role_menu.grid(row=4, column=1, padx=5, pady=5, sticky='w')

		btn_frame = tk.Frame(new_window)
		btn_frame.grid(row=5, column=0, columnspan=2)
		self.submit_btn = tk.Button(btn_frame, 
							  		text="Add Analyst", 
									command=lambda: commit_analyst(
										first_name_var.get(), 
										last_name_var.get(), 
										email_var.get()))
		self.submit_btn.pack(side="left", padx=5)
		self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=new_window.destroy)
		self.cancel_btn.pack(side="left", padx=5)
	
	def add_test(self):
		def commit_test(test_number, test_name, main_component):
			self.db.insert_test_method_table(test_number, test_name, main_component)
		
		new_window = tk.Toplevel(self.root)
		new_window.title('Add New Test')
		# new_window.geometry('300x300')

		test_num_var = tk.StringVar()
		test_name_var = tk.StringVar()
		component_var = tk.StringVar()

		test_num_label = tk.Label(new_window, text='Test Number:')
		test_num_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
		test_num_entry = tk.Entry(new_window, width=20, textvariable= test_num_var)
		test_num_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

		test_name_label = tk.Label(new_window, text='Test Name:')
		test_name_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
		test_name_entry = tk.Entry(new_window, width=20, textvariable= test_name_var)
		test_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

		component_label = tk.Label(new_window, text='Main Component:')
		component_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
		component_entry = tk.Entry(new_window, width=20, textvariable= component_var)
		component_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

		btn_frame = tk.Frame(new_window)
		btn_frame.grid(row=4, column=0, columnspan=2, pady=0)
		self.submit_btn = tk.Button(btn_frame, 
							  text="Add Test", 
							  command=lambda: commit_test(
								  test_num_var.get(), 
								  test_name_var.get(), 
								  component_var.get()))
		self.submit_btn.pack(side="left", padx=5, pady=5)
		self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=new_window.destroy)
		self.cancel_btn.pack(side="left", padx=5, pady=5)
	
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
	
	def prompt_box(self, msg: str):
		def pressed_ok(root):
			root.destroy()

		new_window = tk.Toplevel(self.root)
		new_window.title("Action Interrupted")
		new_window.geometry("250x100")

		label_frame = tk.Frame(new_window, width=250, height = 50)
		label_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
		label = tk.Label(label_frame, text=msg, wraplength=200)
		label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

		btn_frame = tk.Frame(new_window, width = 250, height=50)
		btn_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
		ok_btn = tk.Button(btn_frame, text="OK", command=lambda: pressed_ok(new_window))
		ok_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


