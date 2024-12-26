from dataclasses import dataclass

from logic.services.recomendation import BaseRecomendationService
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class GenerateRecomendationsCommand(BaseCommand):
    token: str
    n_recommendations: int
    
@dataclass(frozen=True)
class GenerateRecomendationsCommandHandler(CommandHandler[GenerateRecomendationsCommand, None]):
    recomendation_service: BaseRecomendationService

    async def handle(self, command: GenerateRecomendationsCommand) -> None:
        return await self.recomendation_service.generate_recomendation(command.token, command.n_recommendations)
