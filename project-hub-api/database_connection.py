import functools
import json
import time
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


BASE_TYPES = ["STRING", "INTEGER", "MEMBER"]

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
                type_id = r[7]
                if r[0] not in cards_ids: 
                    cards.append({
                        "projectName": r[2],
                        "projectId": r[2],
                        "cardId": r[0],
                        "cardTypeId": r[1],
                        "fields": {
                            r[4]: {
                                "value": r[6] if r[6] else r[5],
                                "type": _get_type_by_id(type_id).get("type")
                            }
                        } 
                    })
                else:
                    card_index = cards_ids.index(r[0])
                    cards[card_index]["fields"][r[4]] = {
                        "value": r[6] if r[6] else r[5],
                        "type": _get_type_by_id(type_id).get("type")
                    } 
            return {
                "cards": cards
            }
        return wrapper
    return decorator

def format_project_card_types():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            card_types = []
            for r in result:
                card_types_ids = list(map(lambda x: x.get("cardTypeId"), card_types))
                type_id = r[5]
                if r[0] not in card_types_ids: 
                    card_types.append({
                        "projectName": r[1],
                        "projectId": r[1],
                        "cardTypeId": r[0],
                        "cardType": r[6],
                        "fields": {
                            r[3]: {
                                "value": r[4],
                                "type": _get_type_by_id(type_id).get("type")
                            }
                        } 
                    })
                else:
                    card_type_index = card_types_ids.index(r[0])
                    card_types[card_type_index]["fields"][r[3]] = {
                        "value": r[4],
                        "type": _get_type_by_id(type_id).get("type")
                    } 
            return {
                "cardTypes": card_types
            }
        return wrapper
    return decorator


def to_json_get_user_account_roles():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            roles = []
            for r in result:
                roles.append(r[2])
            return {
                "username": result[0][0],
                "account": result[0][1],
                "roles": roles
            }
        return wrapper
    return decorator

def to_json_get_project_by_id():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            users = []
            for r in result:
                usernames_list = list(map(lambda x: x.get("username"), users))
                if r[3] in usernames_list:
                    users[usernames_list.index(r[3])]["roles"].append(r[4])
                else:
                    users.append({"username": r[3], "id": r[5], "roles": [r[4]]})
            return {
                "projectId": result[0][0],
                "projectName": result[0][1],
                "projectDescription": result[0][2],
                "users": users
            }
        return wrapper
    return decorator

def to_json_get_card_by_id():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.get("cards")[0]
        return wrapper
    return decorator
def with_connection(func):
    def wrapper(*args, **kwargs):
        try:
            t = time.time()
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            query_data = func(*args, **kwargs)
            with conn.cursor() as cur:
                a = cur.execute(query_data['sql'], query_data['params'])
                conn.commit()
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
            return result
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
            print("time", time.time() - t)
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

@to_json_get_project_by_id()
@with_connection
def _get_project_by_id(id: int):
    query = sql.SQL("""
        SELECT p.id, p.name, description , u.username, r.name, u.id  FROM projects p
        join user_project_roles upr on upr.project_id = p.id
        join roles r on r.id = upr.role_id 
        join users u on u.id = upr.user_id 
        WHERE p.id = %s;
    """)
    params = (id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@to_json_get_user_by_id()
@with_connection
def _get_user_by_id(id: int):
    query = sql.SQL("""
        SELECT username, p.name, r.name, a.name, au.role_id
        FROM users 
        join user_project_roles upr ON upr.user_id  =users.id 
        join projects p on p.id = upr.project_id 
        join roles r on r.id = upr.role_id 
        join account_users au on au.user_id = users.id
        join accounts a on a.id = au.account_id
        WHERE users.id = %s;
    """)
    params = (id,)
    return {'sql': query, 'params': params, 'fetchall': True}



@to_json_get_user_account_roles()
@with_connection
def _get_user_account_roles(id: int):
    query = sql.SQL("""
    SELECT username, a.name, r.name
    FROM users 
    join account_users au on au.user_id = users.id
    join accounts a on a.id = au.account_id
    join roles r on r.id = au.role_id
    WHERE users.id = %s;
    """)
    params = (id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@to_json(["fieldId", "projectId", "name", "customTypeId", "defaultValue"])
@with_connection
def _get_field_by_id(id: int):
    query = sql.SQL("SELECT id, project_id, name, custom_type_id, default_value FROM fields WHERE id = %s;")
    params = (id,)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json(["fieldId", "projectId", "name", "customTypeId", "defaultValue"])
@with_connection
def _get_field_by_name(name: str, project_id: str):
    query = sql.SQL("SELECT id, project_id, name, custom_type_id, default_value FROM fields WHERE name = %s and (project_id is null or project_id = %s);")
    params = (name, project_id)
    return {'sql': query, 'params': params, 'fetchone': True}



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
    query = sql.SQL("INSERT INTO fields (project_id, name, custom_type_id) VALUES (%s, %s, %s) RETURNING id")
    params = (project_id, name, type_id)
    return {'sql': query, 'params': params, 'fetchone': True}

@to_json_get_card_by_id()
def _get_card_by_id(card_id: int):
    return _get_project_cards(card_id=card_id)

def validate_field_type(card, field_name, field_type, field_value, project_id, insert=False):
    if field_type == "STRING":
        if type(field_value) == str:
            if insert:
                _insert_or_update_card_field(card.get("cardId"), _get_field_by_name(name=field_name, project_id=project_id).get("fieldId"), current_value=f"\"{field_value}\"")
    elif field_type == "INTEGER":
        if type(field_value) == int:
            if insert:
                _insert_or_update_card_field(card.get("cardId"), _get_field_by_name(name=field_name, project_id=project_id).get("fieldId"), current_value=field_value)
    elif field_type.startswith("LIST"):
        list_type = field_type[5:-1]
        if type(field_value) == list and all([validate_field_type(card=card, field_name=field_name, field_type=list_type, field_value=v, project_id=project_id) for v in field_value]):
            if insert:
                _insert_or_update_card_field(card.get("cardId"), _get_field_by_name(name=field_name, project_id=project_id).get("fieldId"), current_value=f"\"{field_value}\"")
    elif field_type == "MEMBER":
        user = _get_user_by_id(field_value)
        project = _get_project_by_id(project_id)
        return project.get("projectName") in list(map(lambda x: x.get("name"), user.get("projects")))

def validate_change_fields(card, new_fields, project_id):
    for k, v in card.get("fields").items():
        if k in new_fields:
            validate_field_type(card=card, field_name=k, field_type=v.get("type"), field_value=new_fields[k], project_id=project_id, insert=True)
    return

@with_connection
def _insert_or_update_card_field(card_id, field_id, current_value):
    query = sql.SQL("""
    INSERT INTO card_fields (card_id, field_id, current_value)
    SELECT %s, %s, %s
    ON CONFLICT (card_id, field_id)
    DO UPDATE SET current_value = EXCLUDED.current_value;
    """)
    params = (card_id, field_id, current_value)
    return {'sql': query, 'params': params, 'fetchall': True}

@format_project_card_types()
@with_connection
def _get_project_card_types(project_id: int):
    query = sql.SQL("""
    select card_types.id as card_type_id, card_types.project_id, ctf.field_id as field_id, f.name as field_name, default_value, ct.id as field_id, card_types.name as card_type_name
    from card_types join card_type_fields ctf on ctf.card_type_id = card_types.id
    join fields f on f.id = ctf.field_id
    join custom_types ct on ct.id = f.custom_type_id
    where card_types.project_id = %s;
    """)
    params = (project_id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@format_project_card_types()
@with_connection
def _get_card_type_by_id(card_type_id: int):
    query = sql.SQL("""
    select card_types.id as card_type_id, card_types.project_id, ctf.field_id as field_id, f.name as field_name, default_value, ct.id as field_id, card_types.name as card_type_name
    from card_types join card_type_fields ctf on ctf.card_type_id = card_types.id
    join fields f on f.id = ctf.field_id
    join custom_types ct on ct.id = f.custom_type_id
    where card_types.id = %s;
    """)
    params = (card_type_id,)
    return {'sql': query, 'params': params, 'fetchall': True}

@with_connection
def _create_card(project_id: int, card_type_id: int):
    query = sql.SQL("""
    insert into cards (card_type_id, project_id) values (%s, %s) returning id
    """)
    params = (card_type_id, project_id)
    return {'sql': query, 'params': params, 'fetchone': True}


@format_project_cards()
@with_connection
def _get_project_cards(project_id: int = None, card_type_id: int = None, card_id: int = None):
    query = """
    select c.id as card_id, c.card_type_id as card_type_id, c.project_id, ctf.field_id as field_id, f.name as field_name, default_value, cf.current_value, ct.id as field_id from cards c
    join card_type_fields ctf on ctf.card_type_id = c.card_type_id
    join fields f on f.id = ctf.field_id
    left join card_fields cf on (cf.card_id = c.id and cf.field_id = f.id)
    join custom_types ct on ct.id = f.custom_type_id
    """
    wheres = []
    params = []
    if project_id:
        wheres.append("c.project_id = %s")
        params.append(project_id)
    if card_type_id:
        wheres.append("c.card_type_id = %s")
        params.append(card_type_id)
    if card_id:
        wheres.append("c.id = %s")
        params.append(card_id)
    if wheres:
        query += " where " + " and ".join(wheres) + ";"
    else:
        query += ";"
    query = sql.SQL(query)
    params = tuple(params)
    return {'sql': query, 'params': params, 'fetchall': True}
