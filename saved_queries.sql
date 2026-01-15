CREATE TABLE IF NOT EXISTS components (
	component_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	component_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tests (
	test_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	test_number TEXT NOT NULL,
	title TEXT NOT NULL,
	solvent TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS testcomponents (
	test_id INT REFERENCES tests(test_id),
	component_id INT REFERENCES components(component_id)
);

CREATE TABLE IF NOT EXISTS users (
	user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE
);

SELECT test_number, title, solvent, component_name
FROM tests
INNER JOIN testcomponents ON tests.test_id = testcomponents.test_id
INNER JOIN components ON components.component_id = testcomponents.component_id
WHERE test_number = 'TM-0001';
