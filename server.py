from fastapi import FastAPI
from starlette.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return FileResponse("./index.html")


if __name__ == '__main__':
    uvicorn.run(app, port=3000)
