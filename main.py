from fastapi import FastAPI

obj = FastAPI()


@obj.get("/")
def greet():
    return "Hello, World!"
