from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from Parser.week_lessons import print_day

import redis

router = Router()


@router.callback_query(F.data.in_(['today_lessons', 'tomorrow', 'yesterday', 'more']))
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    week_number = date.today().weekday()
    data = callback.data 

    


    if 'today' in data:
        redis_connect.set(name=id, value=0)
        redis_connect.set(name=f'more_info_{id}', value=-1)
        
        page = int(redis_connect.get(name=id))
        page_day_number = (date.today() + timedelta(page)).weekday()
        if page_day_number == 6:
            page += 1
    elif 'tomorrow' in data:
        page = int(redis_connect.get(name=id))+1
        page_day_number = (date.today() + timedelta(page)).weekday()
    
        if page_day_number == 6:
            page += 1
    elif 'yesterday' in data:
        page = int(redis_connect.get(name=id))-1
        page_day_number = (date.today() + timedelta(page)).weekday()
        if page_day_number == 6:
            page -= 1
    elif 'more' in data:
        page = int(redis_connect.get(name=id))
        more = int(redis_connect.get(name=f'more_info_{id}'))
        redis_connect.getset(name=f'more_info_{id}', value=-1*more)
        
    more = int(redis_connect.get(name=f'more_info_{id}'))
    text = await print_day(user, page, more==1)
        
    
    if page != 0: #если это не начальная страница
        if page == week_number * -1 or text == "расписания на этот день нет":
            buttons = {
                'pass_day': ' ',
                'more': 'инфо',
                'tomorrow': '>',
                'today_lessons': 'назад'
            }
        elif page + week_number == 12: 
            buttons = {
                'yesterday': '<',
                'more': 'инфо',
                'pass_day': ' ',
                'today_lessons': 'назад'
            }         
        else: 
            buttons = {
                'yesterday': '<',
                'more': 'инфо',
                'tomorrow': '>',
                'today_lessons': 'назад'
            }
    else:
        buttons = {
            'yesterday': '<',
            'more': 'инфо',
            'tomorrow': '>',
            'log_button': 'назад'
        }
        
    await callback.message.edit_text(
            text=text,
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3, **buttons))
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()
    
    
@router.callback_query(F.data == 'pass_day')
async def log(callback: CallbackQuery):
    await callback.answer()
    
