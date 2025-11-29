import psycopg2
import os
from psycopg2.extras import RealDictCursor

class DBManager:
	def __init__(self, 
			  dbname, 
			  user, 
			  password, 
			  host, 
			  port
			  ):
		try:
			self.conn = psycopg2.connect(
				dbname = dbname,
				user = user,
				password = password,
				host = host,
				port = port)
			self.cur =  self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			self.create_test_methods_table()
			self.create_roles_table()
			self.create_employees_table()
			self.create_employee_roles_table()

		except psycopg2.Error as e:
			print(f"There was an error conencting to PostgreSQL: {e}")

	
	def close(self):
		self.cur.close()
		self.conn.close()
	
	def create_test_methods_table(self):
		self.cur.execute(''' 
				   CREATE TABLE IF NOT EXISTS test_methods (
				   id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
				   test_number varchar(10) NOT NULL UNIQUE,
				   test_name varchar(50) NOT NULL,
				   main_component varchar(40) NOT NULL);
				   ''')
		self.conn.commit()
	
	def create_employees_table(self):
		self.cur.execute('''
				CREATE TABLE IF NOT EXISTS employees (
				   employee_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
				   employee_name TEXT NOT NULL,
				   employee_email TEXT NOT NULL UNIQUE);
				''')
		self.conn.commit()
	
	def create_roles_table(self):
		self.cur.execute('''
				CREATE TABLE IF NOT EXISTS roles (
					role_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
				   	role_name TEXT UNIQUE NOT NULL);
				''')
		self.conn.commit()
	
	def create_employee_roles_table(self):
		self.cur.execute('''
			CREATE TABLE IF NOT EXISTS employee_roles (
				employee_id INT REFERENCES employees(employee_id),
				role_id INT REFERENCES roles(role_id),
				PRIMARY KEY (employee_id, role_id));
			''')
		self.conn.commit()
	
	def insert_employee_table(self, name, email, role):
		self.cur.execute(f'''
			INSERT INTO employees (employee_name, employee_email) 
			VALUES (%s, %s)
			ON CONFLICT (employee_email) DO NOTHING
			RETURNING employee_id; 
			''', (name, email)
			)
		row = self.cur.fetchone()
		employee_id = None

		# If the insert works, get new id
		if row:
			employee_id = row['employee_id']
		else:
			# Employee exists already, get their id
			self.cur.execute('''
				SELECT employee_id
				FROM employees
				WHERE employee_email = %s;
				''', (email,)
			)
			employee_id = self.cur.fetchone()['employee_id']

		self.cur.execute('''
			SELECT role_id 
			FROM roles
			WHERE role_name = %s;
			''', (role.lower(),)
			)
		role_id = self.cur.fetchone()['role_id']

		self.cur.execute(f'''
			INSERT INTO employee_roles (employee_id, role_id)
			VALUES (%s, %s)
			ON CONFLICT DO NOTHING;
			''', (employee_id, role_id)
			)
		self.conn.commit()
			
	def insert_test_method_table(self, num, name, component) -> None:
		self.cur.execute(f'''
			INSERT INTO test_methods (test_number, test_name, main_component)
			VALUES (%s, %s, %s)
			ON CONFLICT DO NOTHING;
			''', (num, name, component))
		self.conn.commit()

	def get_all_analyst_names(self):
		self.cur.execute('''
			SELECT e.employee_name
			FROM employees e
			JOIN employee_roles er ON e.employee_id = er.employee_id
			JOIN roles r ON er.role_id = r.role_id
			WHERE r.role_name = %s
			ORDER BY e.employee_name ASC;
			''', ('analyst',))
		analyst_names = [name['employee_name'] for name in self.cur.fetchall()]
		return analyst_names

	def get_all_submitter_names(self):
		self.cur.execute('''
			SELECT e.employee_name
			FROM employees e
			JOIN employee_roles er ON e.employee_id = er.employee_id
			JOIN roles r ON er.role_id = r.role_id
			WHERE r.role_name = %s
			ORDER BY e.employee_name ASC;
			''', ('submitter',))
		return [name['employee_name'] for name in self.cur.fetchall()]
	
	def get_all_test_methods(self):
		self.cur.execute('''
				SELECT test_number FROM test_methods
				ORDER BY test_number ASC;
				''')
		return [test['test_number'] for test in self.cur.fetchall()]
	
	def remove_test(self, test_num):
		self.cur.execute('''
		DELETE FROM test_methods
		WHERE test_number = %s;
		''', (test_num,))
		self.conn.commit()
		return 