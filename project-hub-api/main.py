from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database_connection import (
    _create_user, 
    _create_project, 
    _create_role, 
    _add_role_to_user, 
    _get_project_by_id,
    _get_user_account_roles,
    _get_user_by_id,
    _get_role_by_id,
    _get_type_by_id,
    _create_field,
    _get_project_cards,
    _get_card_by_id,
    validate_change_card_fields,
    _get_project_card_types,
    _create_card,
    _get_card_type_by_id,
    validate_change_card_type_fields
)

app = FastAPI()

@app.get("/test")
def read_test():
    return {"message": "This is a test endpoint"}

@app.post("/projects/create")
def create_project(name: str, description: str = None):
    project_id = _create_project(name, description)
    return _get_project_by_id(project_id)


@app.post("/users/create")
def create_user(name: str, email: str, password: str):
    user_id = _create_user(name, email, password).get('result')
    return _get_user_by_id(user_id)

@app.post("/roles/create")
def create_role(name: str):
    return _create_role(name)

@app.post("/users/roles/add/{role}")
def add_role_to_user(role: str):
    return _add_role_to_user(role)

@app.get("/projects/{project_id}")
def get_project_by_id(project_id: int):
    return _get_project_by_id(project_id)

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    res = _get_user_account_roles(user_id)
    res.update(_get_user_by_id(user_id))
    return res

@app.get("/roles/{role_id}")
def get_role_by_id(role_id: int):
    return _get_role_by_id(role_id)

@app.get("/types/{type_id}")
def get_type_by_id(type_id: int):
    return _get_type_by_id(type_id)

@app.post("/fields/create")
def create_field(name: str, typeId: int, projectId: int):
    return _create_field(name, typeId, projectId)

@app.get("/projects/{project_id}/cards")
def get_project_cards(project_id: int, itemsPerPage: int = 10, page: int = 1):
    return _get_project_cards(project_id=project_id, items_per_page=itemsPerPage, page=page)

@app.post("/cards/{card_id}/edit")
def edit_card(card_id: int, fields: dict):
    card = _get_card_by_id(card_id=card_id)
    validate_change_card_fields(card=card, new_fields=fields, project_id=card.get("projectId"))
    return _get_card_by_id(card_id=card_id)

@app.post("/card-types/{card_type_id}/edit")
def edit_card(card_type_id: int, fields: dict):
    card_type = _get_card_type_by_id(card_type_id=card_type_id)
    validate_change_card_type_fields(card_type=card_type, new_fields=fields, project_id=card_type.get("projectId"))
    return _get_card_type_by_id(card_type_id=card_type_id)

@app.get("/cards/{card_id}")
def get_card_by_id(card_id: int):
    return _get_card_by_id(card_id=card_id)

@app.get("/card-type/{card_type_id}")
def get_card_type_by_id(card_type_id: int):
    return _get_card_type_by_id(card_type_id=card_type_id)

@app.get("/projects/{project_id}/card-types")
def get_project_card_types(project_id: int):
    return _get_project_card_types(project_id=project_id)

@app.post("/cards/create")
def create_card(project_id: int, card_type_id: int, fields: dict):
    card_id = _create_card(project_id=project_id, card_type_id=card_type_id)
    card = _get_card_by_id(card_id=card_id)
    validate_change_card_fields(card=card, new_fields=fields, project_id=project_id)
    return _get_card_by_id(card_id=card_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8014)
