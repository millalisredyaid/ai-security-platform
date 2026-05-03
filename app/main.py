from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.include_router(api_router)
