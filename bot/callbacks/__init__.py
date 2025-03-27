from aiogram import Router
from .cross_zeroes_callBack import router as router_cross_zeroes
from .menu_callback import router as router_menu
from .top_callBack import router as router_top
from .wordlie_callback import router as router_wordlie


main_router_callback = Router()

main_router_callback.include_routers(
    router_cross_zeroes,
    router_menu,
    router_top,
    router_wordlie
)