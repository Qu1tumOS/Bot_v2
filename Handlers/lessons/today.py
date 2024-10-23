from aiogram import Router, F
from aiogram.types import CallbackQuery

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from Parser.week_lessons import print_day

import redis

router = Router()

@router.callback_query(F.data == 'today_lessons')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    
    page = redis_connect.get(name=id)
    
    if not page:
        redis_connect.set(name=id, value=0)
        
    redis_connect.getset(name=id, value=0)
    redis_connect.close()
        
    await callback.message.edit_text(
        text=await print_day(user),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        yesterday_lessons='<',
                                        more_info='инфо',
                                        tomorrow_lessons='>',
                                        log_button='назад'))
    await callback.answer()
    

@router.callback_query(F.data == 'yesterday_lessons')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    
    page = int(redis_connect.get(name=id))-1
    
    if page != 0:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            more_info='инфо',
                                            tomorrow_lessons='>',
                                            today_lessons='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            more_info='инфо',
                                            tomorrow_lessons='>',
                                            log_button='назад'))
        
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()
    
    
@router.callback_query(F.data == 'tomorrow_lessons')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    
    page = int(redis_connect.get(name=id))+1
    
    if page != 0:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            more_info='инфо',
                                            tomorrow_lessons='>',
                                            today_lessons='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            more_info='инфо',
                                            tomorrow_lessons='>',
                                            log_button='назад'))
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()
