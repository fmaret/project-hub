-- Create database
-- CREATE DATABASE project_hub;

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS user_project_roles CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;


-- Table for users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(100) UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for projects
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for roles
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL
);

-- Table for user roles in projects
CREATE TABLE user_project_roles (
    user_id INT,
    project_id INT,
    role_id INT,
    PRIMARY KEY (user_id, project_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Table for tasks
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    project_id INT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50),
    assigned_to INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (assigned_to) REFERENCES users(user_id)
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
INSERT INTO roles (role_name) VALUES ('ADMIN'), ('MEMBER'), ('VIEWER');
INSERT INTO users (username, email, password) VALUES ('Florent', 'test@test.com', 'test');
INSERT INTO users (username, email, password) VALUES ('Wendy', 'test@test2.com', 'test');
INSERT INTO users (username, email, password) VALUES ('Mathilda', 'test@test3.com', 'test');
INSERT INTO projects (project_name, description) VALUES ('Backend', 'Mon project Backend');
INSERT INTO projects (project_name, description) VALUES ('Frontend', 'Mon project Frontend');
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'Florent'),
    (SELECT project_id FROM projects WHERE project_name = 'Backend'),
    (SELECT role_id FROM roles WHERE role_name = 'ADMIN')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'Florent'),
    (SELECT project_id FROM projects WHERE project_name = 'Backend'),
    (SELECT role_id FROM roles WHERE role_name = 'MEMBER')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'Florent'),
    (SELECT project_id FROM projects WHERE project_name = 'Frontend'),
    (SELECT role_id FROM roles WHERE role_name = 'MEMBER')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'Wendy'),
    (SELECT project_id FROM projects WHERE project_name = 'Frontend'),
    (SELECT role_id FROM roles WHERE role_name = 'ADMIN')
);
INSERT INTO user_project_roles (user_id, project_id, role_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'Mathilda'),
    (SELECT project_id FROM projects WHERE project_name = 'Backend'),
    (SELECT role_id FROM roles WHERE role_name = 'MEMBER')
);