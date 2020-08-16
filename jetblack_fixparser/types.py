from abc import ABCMeta, abstractmethod
from typing import Callable, Awaitable, MutableMapping, Any, Tuple

Event = MutableMapping[str, Any]
Send = Callable[[Event], Awaitable[None]]
Receive = Callable[[], Awaitable[Event]]
Handler = Callable[[Send, Receive], Awaitable[None]]
Middleware = Callable[[Send, Receive, Handler], Awaitable[None]]


class Session(metaclass=ABCMeta):

    @property
    @abstractmethod
    def sender_comp_id(self) -> str:
        raise NotImplementedError

    @property
    def target_comp_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_seqnums(self) -> Tuple[int, int]:
        raise NotImplementedError

    @abstractmethod
    async def set_seqnums(self, outgoing_seqnum: int, incoming_seqnum: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_outgoing_seqnum(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def set_outgoing_seqnum(self, seqnum: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_incoming_seqnum(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def set_incoming_seqnum(self, seqnum: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save_message(self, buf: bytes) -> None:
        raise NotImplementedError


class Store(metaclass=ABCMeta):

    def get_session(self, sender_comp_id: str, target_comp_id: str) -> Session:
        raise NotImplementedError
