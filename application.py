from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return f"Home Page"

@app.get('/about')
def about():
    return f"About Page"
