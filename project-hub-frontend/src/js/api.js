const url = "http://localhost:8014"

export async function getUser(userId) {
    const response = await fetch(`${url}/users/${userId}`, {
        method: "GET",
    });
    const user = await response.json();
    return user;
}

export async function getCards(projectId) {
    const response = await fetch(`${url}/projects/${projectId}/cards`, {
        method: "GET",
    });
    const cards = await response.json();
    return cards;
}

export async function getProject(projectId) {
    const response = await fetch(`${url}/projects/${projectId}`, {
        method: "GET",
    });
    const project = await response.json();
    return project;
}

export async function editCard(cardId) {
    const response = await fetch(`${url}/cards/${cardId}/edit`, {
        method: "GET",
    });
    const project = await response.json();
    return project;
}

