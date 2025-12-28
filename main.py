import tkinter as tk
import os
from gui.gui import LabManagerGUI
from db.manager import DBManager	
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

	db = DBManager(os.getenv("DB_NAME"), 
				os.getenv("DB_USER"), 
				os.getenv("DB_PASSWORD"), 
				os.getenv("DB_HOST"), 
				os.getenv("DB_PORT"))

	app = LabManagerGUI(db)
	app.run()

	db.close()
