from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


# @app.get("/items/{name}")
# async def read_item(request: Request, name: str):
#     return templates.TemplateResponse("index.html", {"request": request, "name": name})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/team")
async def team(request: Request):
    return templates.TemplateResponse("team.html", {"request": request})