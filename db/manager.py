import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import IntegrityError, Error, errors


class DBManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,
                 dbname,
                 user,
                 password,
                 host,
                 port):
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port)

            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            if self.cursor is None:
                print("Could not connect to PostgreSQL.")
            else:
                print("Connected to PostgreSQL successfully.")

            self.cursor.execute("SELECT version();")
            version: dict = self.cursor.fetchone()
            if version is None:
                print("Could not reach database.")
            else:
                print("PostgreSQL version: ", version['version'])

            self.cursor.execute("SELECT current_database();")
            db_name: dict = self.cursor.fetchone()
            if db_name is None:
                print("Could not connect to database.")
            else:
                print("Connected to database:", db_name['current_database'])

            self.create_tests_table()
            self.create_users_table()
            self.create_components_table()
            self.create_testcomponents_table()
            self.placeholders()

        except psycopg2.Error as e:
            print(f"There was an error connecting to PostgreSQL: {e}")

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def placeholders(self) -> None:
        pass
    # self.cursor.execute('''
    # 	INSERT INTO components (component_name) VALUES ('test_component');
    # ''')
    # self.connection.commit()

    def create_tests_table(self) -> None:
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS tests (
                test_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                test_number TEXT NOT NULL,
                title TEXT NOT NULL,
                solvent TEXT NOT NULL
            );
        ''')
        self.connection.commit()

    def create_users_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        ''')
        self.connection.commit()

    def create_components_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS components (
                component_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                component_name TEXT NOT NULL
            );
        ''')
        self.connection.commit()

    def create_testcomponents_table(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS testcomponents (
                test_id INT REFERENCES tests(test_id),
                component_id INT REFERENCES components(component_id)
            );
        ''')
        self.connection.commit()

    def get_users_names(self) -> list[str]:
        self.cursor.execute('''
            SELECT first_name, last_name
            FROM users;
        ''')
        names = self.cursor.fetchall()
        return [name['first_name'] + ' ' + name['last_name'] for name in names]

    def get_tests(self) -> list[str]:
        self.cursor.execute('''
            SELECT test_number
            FROM tests
            ORDER BY test_number ASC;
        ''')
        tests = self.cursor.fetchall()
        return [test['test_number'] for test in tests]

    def get_components(self) -> list[str]:
        self.cursor.execute('''
            SELECT component_name
            FROM components
            ORDER BY component_name ASC;
        ''')
        components = self.cursor.fetchall()
        return [component['component_name'] for component in components]

    def insert_users_table(self, fname: str, lname: str, email: str) -> (bool, str):
        self.cursor.execute('''
            INSERT INTO users (first_name, last_name, email)
            VALUES (%s, %s, %s);
        ''', (fname, lname, email))
        self.connection.commit()

        # TODO ADD ERROR CHECKING HERE ^^^

    def insert_tests_table(self,
                           test_number: str,
                           title: str,
                           solvent: str,
                           components: list[str]) -> tuple[bool, psycopg2.Error | None]:
        try:
            self.cursor.execute('''
                SELECT *
                FROM components
                WHERE component_name = ANY(%s)
            ''', (components,))
            component_dict = self.cursor.fetchall()
            print(component_dict)
            # insert into tests table with the num, title, solvent -> return the new test id
            self.cursor.execute('''
                INSERT INTO tests (title, solvent, test_number) 
                VALUES (%s, %s, %s)
                RETURNING test_id; 
            ''', (title, solvent, test_number))
            returned_test_id = self.cursor.fetchone()['test_id']
            print(returned_test_id)
            # insert into testcomponents the test id and every component id from the component_dict
            for component in component_dict:
                self.cursor.execute('''
                    INSERT INTO testcomponents (test_id, component_id)
                    VALUES (%s, %s)
                ''', (returned_test_id, component['component_id'],))
            self.connection.commit()
            return (True, None)
        except IntegrityError as e:
            print("This test number already exists.")
            self.connection.rollback()
            return (False, e)
        except psycopg2.Error as e:
            self.connection.rollback()
            print("An error ocurred while inserting into tests table.")
            return (False, e)

