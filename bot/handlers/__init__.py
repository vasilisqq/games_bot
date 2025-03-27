from aiogram import Router
from .errors_handler import router as router_errors_handler
from .inline import router as router_inline
from .messages import router as router_messages
from .commands.common_commands import router as router_common_commands
from .commands.mafia_commands import router as router_mafia_commands


main_router_handler = Router()
main_router_handler.include_routers(
    router_common_commands,
    router_mafia_commands,
    router_errors_handler,
    router_inline,
    router_messages
)
