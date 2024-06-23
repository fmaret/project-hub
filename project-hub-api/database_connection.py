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


BASE_TYPES = ["STRING", "INTEGER"]

def recurse_format_type(types, id):
        first_type = list(filter(lambda x: x[0] == id, types))[0]
        type_name = first_type[1]
        if type_name in BASE_TYPES:
            if first_type[2]:
                return f"OPTIONAL[{type_name}]"
            else:
                return type_name
        elif type_name == "LIST":
            return f"LIST[{recurse_format_type(types, first_type[3])}]"
        elif type_name == "TUPLE":
            tuple_elements = list(filter(lambda x: x[0] == id, types))
            tuple_elements.sort(key=lambda x: x[4])
            return f"({','.join(map(lambda x: recurse_format_type(types, x[3]), tuple_elements))})"

def format_output_type_get_type_by_id():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return {
                "id": result[0][0],
                "type": recurse_format_type(result, result[0][0])
            }
        return wrapper
    return decorator

def format_project_cards():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            cards = []
            for r in result:
                cards_ids = list(map(lambda x: x.get("cardId"), cards))
                if r[0] not in cards_ids: 
                    cards.append({
                        "projectName": r[2],
                        "projectId": r[2],
                        "cardId": r[0],
                        "cardTypeId": r[1],
                        "fields": {
                            r[4]: r[6] if r[6] else r[5] 
                        } 
                    })
                else:
                    card_index = cards_ids.index(r[0])
                    cards[card_index]["fields"][r[4]] = r[6] if r[6] else r[5] 
            return {
                "cards": cards
            }
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
                a = cur.execute(query_data['sql'], query_data['params'])
                print("aa", a)
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
def get_user_by_id(id):
    query = sql.SQL("SELECT * FROM users WHERE id = %s")
    params = (id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_user(name: str, email: str, password: str):
    query = sql.SQL("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id")
    params = (name, email, password,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_project(name: str, description: str):
    query = sql.SQL("INSERT INTO projects (name, description) VALUES (%s, %s) RETURNING id")
    params = (name, description)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _create_role(role_name: str):
    query = sql.SQL("INSERT INTO roles (role_name) VALUES (%s) RETURNING id")
    params = (role_name,)
    return {'sql': query, 'params': params, 'fetchone': True}

@with_connection
def _add_role_to_user(user_id: int, project_id: int, role_id: int):
    query = sql.SQL("INSERT INTO user_project_roles (user_id, project_id, role_id) VALUES (%s, %s, %s) RETURNING *")
    params = (user_id, project_id, role_id)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json(["projectId", "projectName", "projectDescription"])
@with_connection
def _get_project_by_id(id: int):
    query = sql.SQL("SELECT id, name, description FROM projects WHERE id = %s;")
    params = (id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json_get_user_by_id()
@with_connection
def _get_user_by_id(id: int):
    query = sql.SQL("""
        SELECT username, p.name, r.name 
        FROM users 
        join user_project_roles upr ON upr.user_id  =users.id 
        join projects p on p.id = upr.project_id 
        join roles r on r.id = upr.role_id 
        WHERE users.id = %s;
    """)
    params = (id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@to_json(["roleId", "roleName"])
@with_connection
def _get_role_by_id(id: int):
    query = sql.SQL("SELECT id, name FROM roles WHERE id = %s;")
    params = (id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@format_output_type_get_type_by_id()
@with_connection
def _get_type_by_id(id: int):
    query = sql.SQL("""
    WITH RECURSIVE type_hierarchy AS (
        SELECT c.id, c.type, c.is_optional, cte.custom_type_child_id, cte.index
        FROM custom_types c
        LEFT join custom_types_elements cte ON cte.custom_type_parent_id = c.id
        WHERE c.id = %s
        UNION ALL
        SELECT c.id, c.type, c.is_optional, cte.custom_type_child_id, cte.index
        FROM custom_types c
        LEFT join custom_types_elements cte ON cte.custom_type_parent_id = c.id
        join type_hierarchy th ON th.custom_type_child_id = c.id
    )
    SELECT id, type, is_optional, custom_type_child_id, index from type_hierarchy;
    """)
    params = (id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@with_connection
def _create_field(name: str, type_id: int, project_id: int):
    print("aze1")
    query = sql.SQL("INSERT INTO fields (project_id, name, custom_type_id) VALUES (%s, %s, %s) RETURNING id")
    params = (project_id, name, type_id)
    print("aze2")
    return {'sql': query, 'params': params, 'fetchone': True}

# @with_connection
# def _create_card_type():
#     query = sql.SQL("INSERT INTO fields (project_id, name, custom_type_id) VALUES (%s, %s, %s) RETURNING id")
#     params = (project_id, name, type_id)
#     print("aze2")
#     return {'sql': query, 'params': params, 'fetchone': True}

# @with_connection
# def _create_card(card_type_id: int):
#     query = sql.SQL("INSERT INTO fields (project_id, name, custom_type_id) VALUES (%s, %s, %s) RETURNING id")
#     params = (project_id, name, type_id)
#     print("aze2")
#     return {'sql': query, 'params': params, 'fetchone': True}

# @with_connection
# def _get_card_by_id(card_id: int):
#     query = sql.SQL("INSERT INTO fields (project_id, name, custom_type_id) VALUES (%s, %s, %s) RETURNING id")
#     params = (project_id, name, type_id)
#     print("aze2")
#     return {'sql': query, 'params': params, 'fetchone': True}

@format_project_cards()
@with_connection
def _get_project_cards(project_id: int = None, card_type_id: int = None):
    query = """
    select c.id as card_id, c.card_type_id as card_type_id, c.project_id, ctf.field_id as field_id, f.name as field_name, default_value, cf.current_value from cards c
    join card_type_fields ctf on ctf.card_type_id = c.card_type_id
    join fields f on f.id = ctf.field_id
    left join card_fields cf on (cf.card_type_id = c.id and cf.field_id = f.id)
    """
    wheres = []
    params = []
    if project_id:
        wheres.append("c.project_id = %s")
        params.append(project_id)
    if card_type_id:
        wheres.append("c.project_id = %s")
        params.append(card_type_id)
    if wheres:
        query += " where " + " and ".join(wheres) + ";"
    else:
        query += ";"
    query = sql.SQL(query)
    params = tuple(params)
    return {'sql': query, 'params': params, 'fetchall': True}

