from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIDMiddleware

setup_logging()

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.add_middleware(RequestIDMiddleware)
app.include_router(api_router)
