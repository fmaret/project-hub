from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def read_test():
    return {"message": "This is a test endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8014)
