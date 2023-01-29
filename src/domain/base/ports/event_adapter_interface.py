import abc
from domain.base.event import DomainEvent


class DomainEventPublisher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def publish(self, event: DomainEvent):
        raise NotImplementedError
