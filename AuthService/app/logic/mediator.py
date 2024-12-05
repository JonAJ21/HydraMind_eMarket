from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from logic.queries.base import QR, QT, BaseQuery, QueryHandler
from domain.events.base import BaseEvent
from logic.exceptions.mediator import CommandHandlersNotRegisteredException, EventHandlersNotRegisteredException, QueryHandlersNotRegisteredException
from logic.commands.base import CR, CT, BaseCommand, CommandHandler
from logic.events.base import ER, ET, EventHandler


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    
    queries_map: dict[QT, QueryHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    
    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)
        
    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)
        
    def register_query(self, query: QT, query_handlers: Iterable[QueryHandler[QT, QR]]):
        self.queries_map[query].extend(query_handlers)
        
    async def handle_events(self, event: BaseEvent) -> Iterable[ER]:
        event_type = event.__class__
        handlers = self.events_map.get(event_type)
        
        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)
        
        return [await handler.handle(event) for handler in handlers]
    
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)
        
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        
        return [await handler.handle(command) for handler in handlers]
    
    async def handle_query(self, query: BaseQuery) -> Iterable[QR]:
        query_type = query.__class__
        handlers = self.queries_map.get(query_type)
        
        if not handlers:
            raise QueryHandlersNotRegisteredException(query_type)
        
        return [await handler.handle(query) for handler in handlers]
    
        