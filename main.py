import os
from config import Config
from database import Database
from utils import Utils
from model import *

from fastapi import FastAPI, Response, status, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware





db = Database(base_path="./data/base.json")
config = Config(password=os.getenv("UNI_PASSWORD", "qwerty"))


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/faculty", response_model=list[str])
async def get_faculty():
    return db.get_faculty()


@app.post("/api/faculty", responses={200: {"description": "Не возвращается!!!"}, 201: {"model": list[str]}, 403: {"model": CheckPasswordError}})
async def create_faculty(body: CreateFacultyRequest, response: Response):
    if not Utils.check_password(body.password, config):
        response.status_code = status.HTTP_403_FORBIDDEN
        return CheckPasswordError(message="wrong password")
    db.create_faculty(body.faculty)
    response.status_code = status.HTTP_201_CREATED
    return db.get_faculty()


@app.get("/api/winners", response_model=list[str])
async def get_winners():
    return db.get_winners()


@app.post("/api/winners", responses={200: {"description": "Не возвращается!!!"}, 201: {"model": list[str]}, 403: {"model": CheckPasswordError}})
async def create_winners(body: CreateFacultyRequest, response: Response):
    if not Utils.check_password(body.password, config):
        response.status_code = status.HTTP_403_FORBIDDEN
        return CheckPasswordError(message="wrong password")
    Utils.check_password(body.password, config)
    db.create_winners(body.faculty)
    response.status_code = status.HTTP_201_CREATED
    return db.get_winners()


@app.get("/final/audience", response_model=list[OneFinalAudienceResult])
async def get_audience():
    return db.get_audience()


@app.post("/final/audience", responses={200: {"description": "Не возвращается!!!"}, 201: {"model": list[OneFinalAudienceResult]}, 403: {"model": CheckPasswordError}})
async def create_audience(body: CreateFinalAudienceResult, response: Response):
    if not Utils.check_password(body.password, config):
        response.status_code = status.HTTP_403_FORBIDDEN
        return CheckPasswordError(message="wrong password")
    db.create_audience(body.data)
    response.status_code = status.HTTP_201_CREATED
    return db.get_audience()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
            await manager.broadcast(f"activated")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Univision backend",
        version="0.0.1",
        description="OpenAPI schema for univision site.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
