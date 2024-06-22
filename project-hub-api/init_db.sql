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




CREATE TYPE custom_type_enum AS ENUM ('STRING', 'INTEGER', 'LIST', 'ENUM', 'UNION', 'TUPLE');

CREATE TABLE custom_types (
    id SERIAL PRIMARY KEY,
    type custom_type_enum NOT NULL,
    is_optional BOOLEAN DEFAULT FALSE
);

CREATE TABLE custom_types_elements (
    id SERIAL PRIMARY KEY,
    custom_type_parent_id INT REFERENCES custom_types(id) NOT NULL,
    custom_type_child_id INT REFERENCES custom_types(id) NOT NULL,
    index INT,
    value VARCHAR(50)

);

CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id),
    name VARCHAR(255),
    custom_type_id INT REFERENCES custom_types(id)
);
