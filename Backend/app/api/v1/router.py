from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import ValidationError
from datetime import datetime

from sqlmodel import Session, select, func
from . import schemas, models
from app.database import engine
from app.logs import logger


users_router = APIRouter(tags=['users'])
posts_router = APIRouter(tags=['posts'])

@users_router.post('/create-account/')
def create_telegram_account(user: schemas.UserCreate):
    """
    Create account with telegram user
    """
    try:
        validated_data = schemas.UserCreate.model_validate(user)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    with Session(engine) as session:
        # Check if the user already exists
        existing_user = session.exec(
            select(models.User).where(
                (models.User.telegram_id == validated_data.telegram_id)
            )
        ).first()

        if existing_user:
            logger.info('User already exists.')
            raise HTTPException(status_code=400, detail='User already exists.')

        # Create a new user if not exists
        item = models.User(
            name=validated_data.name,
            telegram_id=validated_data.telegram_id,
            username=validated_data.username,
            role='Client',
            signup_at='Telegram',
            created_at=datetime.now(),
        )
        session.add(item)
        session.commit()

    logger.info('User created successfully.')
    return {'message': 'User created successfully'}

@posts_router.post('/set-url/')
def capture_url_from_telegram(urlsinput: schemas.UrlTelegramCreate,
                              background_tasks: BackgroundTasks):
    """
    Capture the URL from the request, store it in the database,
    and start a background task to scrape and create a post.
    """
    try:
        validated_data = schemas.UrlTelegramCreate.model_validate(urlsinput)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # TODO: Prevent duplicate Url and repetitive post scraping
    with Session(engine) as session:
        user_id = session.exec(
            select(models.User.id).where(models.User.telegram_id == validated_data.telegram_id)
        ).one_or_none()

        item = models.Url(
            url=str(validated_data.url),
            user_id=user_id,
        )
        session.add(item)
        session.commit()
        logger.info('Url listed successfully.')

        background_tasks.add_task(scrape_and_create_post,
                                  item.url, item.id, item.user_id)
        logger.info(f'The url scrapping task add in background successfully: {item.url}')

    return {'message': 'Url listed successfully'}

async def scrape_and_create_post(url: str, url_id: int, user_id: int):
    """
    Scrapes the given URL and creates a new post with the scraped content.
    """
    # TODO: Implement the scrapper and validatation
    # scraped_data = scrape_url(url)
    if True:
        with Session(engine) as session:
            max_order = session.exec(select(func.max(models.Post.post_order))).one_or_none()
            new_post_order = (max_order or 0) + 1

            new_post = models.Post(
                user_id=user_id,
                url_id=url_id,
                post_order=new_post_order,
                platform='Unknown',
                title='',# scraped_data.get('title'),
                body='',
                created_at=datetime.now()
            )
            session.add(new_post)
            session.commit()

@posts_router.post('/reload-post/')
async def reload_post():
    # TODO: create a reload option for each url.
    pass
