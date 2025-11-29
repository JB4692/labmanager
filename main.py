import tkinter as tk
import os
from gui.gui import LabManagerGUI
from db.manager import DBManager	
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
	db_name = os.getenv("DB_NAME")
	db_user = os.getenv("DB_USER")
	db_password = os.getenv("DB_PASSWORD")
	db_host = os.getenv("DB_HOST")
	db_port = os.getenv("DB_PORT")

	db = DBManager(db_name, db_user, db_password, db_host, db_port)

	app = LabManagerGUI(db)
	app.run()

	db.close()
