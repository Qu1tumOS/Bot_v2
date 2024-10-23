import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, Router
from config import settings
from Handlers import start, registration_check, other_handlers
from Handlers.lessons import today, today_more_info
from Handlers.settings import open_settings
from DataBase.connect import engine, Base
from Apscheduler.lessons import add_lessons_to_table



router = Router()

async def main() -> None:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all) #----- удаление БД ------
    #     await conn.run_sync(Base.metadata.create_all) #----- создание новой ------

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    

    dp.include_router(registration_check.router)
    
    dp.include_router(start.router)
    dp.include_router(today.router)
    dp.include_router(today_more_info.router)
    
    dp.include_router(open_settings.router)
    
    dp.include_router(other_handlers.router)
    
    
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(add_lessons_to_table,
                      'cron',
                      hour='01',
                      minute='16',
                      second='20')

    scheduler.start()
    
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, skip_updates=False)

if __name__ == '__main__':
    asyncio.run(main())