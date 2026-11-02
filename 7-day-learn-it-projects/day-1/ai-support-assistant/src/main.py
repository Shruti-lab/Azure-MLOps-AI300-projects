from contextlib import asynccontextmanager

from fastapi import FastAPI



ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize db
    yield
    # clode db


app = FastAPI(lifespan=lifespan)
