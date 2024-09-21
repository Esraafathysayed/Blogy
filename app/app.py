from .api.v1.routers import post, user, auth, likes, comments
from fastapi import FastAPI


app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(likes.router)
app.include_router(comments.router)


@app.get("/")
def home():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", reload=True)
