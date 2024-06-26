-- Create database
-- CREATE DATABASE project_hub;

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS user_project_roles CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS list CASCADE;
DROP TABLE IF EXISTS custom_types CASCADE;
DROP TABLE IF EXISTS fields CASCADE;
DROP TABLE IF EXISTS custom_types_elements CASCADE;
DROP TYPE IF EXISTS custom_type_enum;
DROP TABLE IF EXISTS card_types CASCADE;
DROP TABLE IF EXISTS card_type_fields CASCADE;
DROP TABLE IF EXISTS cards CASCADE;
DROP TABLE IF EXISTS card_fields CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS account_users CASCADE;
DROP CONSTRAINT IF EXISTS card_fields_unique_constraint;

-- Table for users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Table for user roles in projects
CREATE TABLE user_project_roles (
    user_id INT,
    project_id INT,
    role_id INT,
    PRIMARY KEY (user_id, project_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Table for tasks
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    id INT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50),
    assigned_to INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES projects(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

-- Trigger function to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update the updated_at column on update
CREATE TRIGGER update_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


-- Insert default roles
INSERT INTO roles (name) VALUES ('ADMIN'), ('MEMBER'), ('VIEWER');
INSERT INTO users (username, email, password) VALUES ('Florent', 'test@test.com', 'test');
INSERT INTO users (username, email, password) VALUES ('Wendy', 'test@test2.com', 'test');
INSERT INTO users (username, email, password) VALUES ('Mathilda', 'test@test3.com', 'test');
INSERT INTO projects (name, description) VALUES ('Backend', 'Mon project Backend');
INSERT INTO projects (name, description) VALUES ('Frontend', 'Mon project Frontend');
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT id FROM users WHERE username = 'Florent'),
    (SELECT id FROM projects WHERE name = 'Backend'),
    (SELECT id FROM roles WHERE name = 'ADMIN')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT id FROM users WHERE username = 'Florent'),
    (SELECT id FROM projects WHERE name = 'Backend'),
    (SELECT id FROM roles WHERE name = 'MEMBER')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT id FROM users WHERE username = 'Florent'),
    (SELECT id FROM projects WHERE name = 'Frontend'),
    (SELECT id FROM roles WHERE name = 'MEMBER')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT id FROM users WHERE username = 'Wendy'),
    (SELECT id FROM projects WHERE name = 'Frontend'),
    (SELECT id FROM roles WHERE name = 'ADMIN')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT id FROM users WHERE username = 'Mathilda'),
    (SELECT id FROM projects WHERE name = 'Backend'),
    (SELECT id FROM roles WHERE name = 'MEMBER')
);




CREATE TYPE custom_type_enum AS ENUM ('STRING', 'INTEGER', 'LIST', 'ENUM', 'UNION', 'TUPLE', 'MEMBER');

CREATE TABLE custom_types (
    id SERIAL PRIMARY KEY,
    type custom_type_enum NOT NULL,
    is_optional BOOLEAN DEFAULT FALSE
);

CREATE TABLE custom_types_elements (
    id SERIAL PRIMARY KEY,
    custom_type_parent_id INT REFERENCES custom_types(id) NOT NULL,
    custom_type_child_id INT REFERENCES custom_types(id),
    index INT,
    value VARCHAR(50)

);

CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id),
    name VARCHAR(255),
    custom_type_id INT REFERENCES custom_types(id),
    default_value JSONB
);


INSERT INTO custom_types (type, is_optional) VALUES ('STRING', true);
INSERT INTO custom_types (type, is_optional) VALUES ('STRING', false);
INSERT INTO custom_types (type, is_optional) VALUES ('INTEGER', false);
INSERT INTO custom_types (type, is_optional) VALUES ('LIST', false);
INSERT INTO custom_types (type, is_optional) VALUES ('TUPLE', false);
INSERT INTO custom_types (type, is_optional) VALUES ('LIST', false);
INSERT INTO custom_types (type, is_optional) VALUES ('MEMBER', false);
INSERT INTO custom_types_elements (custom_type_parent_id, custom_type_child_id) VALUES (4, 5);
INSERT INTO custom_types_elements (custom_type_parent_id, custom_type_child_id) VALUES (6, 7);
INSERT INTO custom_types_elements (custom_type_parent_id, custom_type_child_id, index) VALUES (5, 2, 0);
INSERT INTO custom_types_elements (custom_type_parent_id, custom_type_child_id, index) VALUES (5, 3, 1);

INSERT INTO fields (name, custom_type_id) VALUES ('description', 2);
INSERT INTO fields (name, custom_type_id) VALUES ('title', 2);
INSERT INTO fields (name, custom_type_id) VALUES ('assignees', 6);



CREATE TABLE card_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

INSERT INTO card_types (project_id, name) VALUES (1, 'Ticket');

CREATE TABLE card_type_fields (
    id SERIAL PRIMARY KEY,
    card_type_id INT,
    field_id INT,
    FOREIGN KEY (card_type_id) REFERENCES card_types(id),
    FOREIGN KEY (field_id) REFERENCES fields(id)
);

INSERT INTO card_type_fields (card_type_id, field_id) VALUES (1, 1);
INSERT INTO card_type_fields (card_type_id, field_id) VALUES (1, 2);
INSERT INTO card_type_fields (card_type_id, field_id) VALUES (1, 3);

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    card_type_id INT REFERENCES card_types(id),
    project_id INT REFERENCES projects(id)
);

INSERT INTO cards (card_type_id, project_id) VALUES (1, 1);

CREATE TABLE card_fields (
    id SERIAL PRIMARY KEY,
    card_id INT REFERENCES cards(id),
    field_id INT REFERENCES fields(id),
    current_value JSONB
);

INSERT INTO card_fields (card_id, field_id, current_value) VALUES (1, 1, '"Coucou"');

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE account_users (
    account_id INT REFERENCES accounts(id),
    user_id INT REFERENCES users(id),
    role_id INT REFERENCES roles(id),
    PRIMARY KEY (account_id, user_id, role_id)
);

INSERT INTO accounts (name) VALUES ('Mon entreprise');

INSERT INTO account_users (account_id, user_id, role_id) VALUES (1, 1, 1);
INSERT INTO account_users (account_id, user_id, role_id) VALUES (1, 2, 1);
INSERT INTO account_users (account_id, user_id, role_id) VALUES (1, 3, 2);


ALTER TABLE card_fields
ADD CONSTRAINT card_fields_unique_constraint UNIQUE (card_id, field_id);

INSERT INTO custom_types (type, is_optional) VALUES ('ENUM', false);
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-01');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-02');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-03');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-04');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-05');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-06');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-07');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-08');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-09');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-10');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-11');
INSERT INTO custom_types_elements (custom_type_parent_id, value) VALUES (8, '2024-12');

INSERT INTO custom_types (type, is_optional) VALUES ('LIST', false);
INSERT INTO custom_types_elements (custom_type_parent_id, custom_type_child_id) VALUES (9, 8);

INSERT INTO fields (name, custom_type_id) VALUES ('sprint', 9);
INSERT INTO card_type_fields (card_type_id, field_id) VALUES (1, 4);
