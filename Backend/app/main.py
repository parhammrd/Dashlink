#!/usr/bin/env python

from .logs import logger
from decouple import config

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router


FRONT_URL = config('FRONT_URL')

app = FastAPI()

# TODO: Implement hte Front
# origins = [FRONT_URL] # React frontend URL

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(router.users_router)
app.include_router(router.posts_router)


@app.get('/')
def root():
    logger.info('Attempting to get root direction.')
    return Response('<h1>Dashboard.</h1>')
