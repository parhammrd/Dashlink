from decouple import config

from .logs import logger
from app.api.v1.models import (
    User,
    Url,
    Post,
    Token,
    Tags,
    Segmentation,
    Platforms,
    Roles
)

from sqlmodel import SQLModel, create_engine, Session


DATABASE_URL = config('APP_DATABASE_URL')

engine = create_engine(DATABASE_URL)
logger.info("Database engine created")

SQLModel.metadata.create_all(engine)
logger.info("Database schema created")

# Create the foundation
with Session(engine) as session:
    existing_role = session.query(Roles).first()
    if not existing_role:
        initial_roles = [
                Roles(role='Client'),
            ]
        session.add_all(initial_roles)
        session.commit()

    existing_platform = session.query(Platforms).first()
    if not existing_platform:
        initial_platform = [
                Platforms(platform='Unknown'),
            ]
        session.add_all(initial_platform)
        session.commit()
