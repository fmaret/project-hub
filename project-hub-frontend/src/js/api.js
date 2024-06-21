const url = "http://localhost:8014"

export async function getUser(userId) {
    const response = await fetch(`${url}/users/${userId}`, {
        method: "GET",
    });
    const user = await response.json();
    return user;
}

