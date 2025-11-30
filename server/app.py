from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from server.database import initialize_tables, drop_tables
from routes.openaudit_routes import openaudit_router
from routes.users_routes import users_router

description = """
Open-AudIT Backend API.. 🚀

"""

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_tables()
    yield


app = FastAPI(
    middleware=middleware,
    title="Open-AudIT Backend API",
    docs_url="/docs",
    description=description,
    summary="Implementation of a Backend API that consumes The Open-AudIT Enterprise REST API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    lifespan=lifespan
)

app.include_router(users_router, tags=["Users"], prefix="/open-audit/api/v1")
app.include_router(openaudit_router, prefix="/open-audit/api/v1")


@app.get("/open-audit/api/v1", tags=["Root"])
async def root(request: Request):
    response = """
                <html>
                    <head>
                        <title>Open-AudIT Backend API</title>
                    </head>
                    <body>
                        <h1>Welcome to Open-AudIT Backend Home API</h1>
                        <p>Please go to the docs: <strong><a href="http://localhost:8000/docs/">API Docs</a></strong></p>
                    </body>
                </html>
               """
    return Response(status_code=status.HTTP_200_OK, content=response, media_type="text/html")