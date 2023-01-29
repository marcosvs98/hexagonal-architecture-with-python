from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import motor.motor_asyncio
from settings import MongoDatabaseSettings


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine)


def get_db():
    session: Session = session_local()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


def get_mongo_db(config: MongoDatabaseSettings):
    uri = f'mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_SERVER}:{config.MONGO_PORT}'
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client.OrderingService
    return db