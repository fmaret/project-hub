import functools
import json
import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "db"
DB_USER = "test"
DB_PASSWORD = "test"
DB_HOST = "localhost"
DB_PORT = "8015"

def to_json(keys):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if len(result) != len(keys):
                raise ValueError("The length of the result list and the keys list must be the same")
            result_dict = dict(zip(keys, result))
            return result_dict
        return wrapper
    return decorator

def to_json_get_user_by_id():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result_dict = {
                "username": result[0][0],
                "projects": []
            }
            for r in result:
                projects_names = list(map(lambda x: x.get("name"), result_dict["projects"]))
                if r[1] in projects_names:
                    index = projects_names.index(r[1])
                    result_dict["projects"][index]["roles"].append(r[2])
                    break
                result_dict["projects"].append({
                    "name": r[1],
                    "roles": [r[2]]
                })
            return result_dict
        return wrapper
    return decorator



def with_connection(func):
    def wrapper(*args, **kwargs):
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Connection to the database established successfully.")
            query_data = func(*args, **kwargs)
            with conn.cursor() as cur:
                cur.execute(query_data['sql'], query_data['params'])
                conn.commit()
                print(query_data.get('fetchone'))
                if query_data.get('fetchone'):
                    r = cur.fetchone()
                    if len(r) == 1:
                        result = r[0]
                    else:
                        result = r
                elif query_data.get('fetchall'):
                    result = cur.fetchall()
                else:
                    conn.commit()
            print("before result", result)
            return result
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
            print("Connection to the database closed.")
    return wrapper

@with_connection
def get_user_by_id(user_id):
    query = sql.SQL("SELECT * FROM users WHERE user_id = %s")
    params = (user_id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_user(name: str, email: str, password: str):
    query = sql.SQL("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id")
    params = (name, email, password,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_project(project_name: str, description: str):
    query = sql.SQL("INSERT INTO projects (project_name, description) VALUES (%s, %s) RETURNING project_id")
    params = (project_name, description)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_role(role_name: str):
    query = sql.SQL("INSERT INTO roles (role_name) VALUES (%s) RETURNING role_id")
    params = (role_name,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _add_role_to_user(user_id: int, project_id: int, role_id: int):
    query = sql.SQL("INSERT INTO user_project_roles (user_id, project_id, role_id) VALUES (%s, %s, %s) RETURNING *")
    params = (user_id, project_id, role_id)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json(["projectId", "projectName", "projectDescription"])
@with_connection
def _get_project_by_id(project_id: int):
    query = sql.SQL("SELECT project_id, project_name, description FROM projects WHERE project_id = %s;")
    params = (project_id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json_get_user_by_id()
@with_connection
def _get_user_by_id(project_id: int):
    query = sql.SQL("""
        SELECT username, project_name, role_name 
        FROM users 
        join user_project_roles upr ON upr.user_id  =users.user_id 
        join projects p on p.project_id = upr.project_id 
        join roles r on r.role_id = upr.role_id 
        WHERE users.user_id = %s;
    """)
    params = (project_id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@to_json(["roleId", "roleName"])
@with_connection
def _get_role_by_id(role_id: int):
    query = sql.SQL("SELECT role_id, role_name FROM roles WHERE role_id = %s;")
    params = (role_id,)
    return {'sql': query, 'params': params, 'fetchone': True}
