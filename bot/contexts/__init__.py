from aiogram import Router
from .wordlie_context import router as router_wordlie_context

main_router_contexts = Router()

main_router_contexts.include_routers(
    router_wordlie_context
)