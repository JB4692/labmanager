import tkinter as tk
from db.manager import DBManager
import re


def get_selected_items_from_listbox(lb: tk.Listbox) -> list[str]:
	selected_indices = lb.curselection()
	selected_items = [lb.get(i) for i in selected_indices]
	return selected_items


def get_users_names(db: DBManager) -> list[str]:
	# return ['testname']  # for testing
	return db.get_users_names()


def get_test_methods(db: DBManager) -> list[str]:
	# return ['test1']  # for testing
	return db.get_tests()


def get_components(db: DBManager) -> list[str]:
	return db.get_components()


def validate_email(email: str) -> bool:
	regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
	print(repr(email))
	return True if re.fullmatch(regex, email.strip()) else False
