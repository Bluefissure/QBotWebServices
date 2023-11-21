import time
import re

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route

from .resources import router
# from .models import database


def get_app() -> FastAPI:
    app = FastAPI()

    # origins = [
    #     "http://localhost",
    #     "http://localhost:8080",
    # ]

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # app.add_middleware(
    #     GZipMiddleware,
    #     minimum_size=500
    # )

    # @app.middleware("http")
    # async def add_process_time_header(request: Request, call_next):
    #     start_time = time.time()
    #     response = await call_next(request)
    #     process_time = time.time() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #     return response

    app.include_router(router)

    for route in app.router.routes:
        if isinstance(route, Route):
            route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)

    # No database needs, for now
    # @app.on_event("startup")
    # async def startup():
    #     await database.connect()

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await database.disconnect()

    return app
