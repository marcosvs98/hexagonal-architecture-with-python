import pymongo
from domain.base.event import DomainEvent
from database import get_mongo_db
from bson.objectid import ObjectId
from settings import MongoDatabaseSettings
from domain.base.ports.event_adapter_interface import DomainEventPublisher


class OrderEventPublisher(DomainEventPublisher):
    def __init__(self, collection_name='order_events'):
        self.db = get_mongo_db(MongoDatabaseSettings())
        self.collection_name = collection_name

    async def publish(self, event: DomainEvent):
        await self.db[self.collection_name].insert_one(event.dict())
