from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from Parser.week_lessons import print_day

import redis

router = Router()


@router.callback_query(F.data == 'view_lessons_more_info')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    week_number = date.today().weekday()

    
    page = int(redis_connect.get(name=id))
    page_day_number = (date.today() + timedelta(page)).weekday()
    if page_day_number == 6:
        page += 1
     
    if page != 0:
        if page == week_number * -1:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                pass_day=' ',
                                                view_lessons='инфо',
                                                tomorrow_lessons_more_info='>',
                                                today_lessons_more_info='назад'))
        elif page + week_number == 12:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons_more_info='<',
                                                view_lessons='инфо',
                                                pass_day=' ',
                                                today_lessons_more_info='назад'))
        else:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons_more_info='<',
                                                view_lessons='инфо',
                                                tomorrow_lessons_more_info='>',
                                                today_lessons_more_info='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page, True),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons_more_info='<',
                                            view_lessons='инфо',
                                            tomorrow_lessons_more_info='>',
                                            log_button='назад'))
    await callback.answer()
    

@router.callback_query(F.data == 'today_lessons_more_info')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    
    
    redis_connect.set(name=id, value=0)
    page = int(redis_connect.get(name=id))
    
    page_day_number = (date.today() + timedelta(page)).weekday()
    if page_day_number == 6:
        page += 1
    else:
        page = 0
    
    
        
    redis_connect.getset(name=id, value=0)
    redis_connect.close()
        
    await callback.message.edit_text(
        text=await print_day(user, more=True),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        yesterday_lessons_more_info='<',
                                        view_lessons='инфо',
                                        tomorrow_lessons_more_info='>',
                                        log_button='назад'))
    await callback.answer()
    

@router.callback_query(F.data == 'yesterday_lessons_more_info')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    week_number = date.today().weekday()
    
    page = int(redis_connect.get(name=id))-1
    page_day_number = (date.today() + timedelta(page)).weekday()
    if page_day_number == 6:
        page -= 1
    

    
    if page != 0:
        if page != week_number * -1:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons_more_info='<',
                                                view_lessons='инфо',
                                                tomorrow_lessons_more_info='>',
                                                today_lessons_more_info='назад'))
        else:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                pass_day=' ',
                                                view_lessons='инфо',
                                                tomorrow_lessons_more_info='>',
                                                today_lessons_more_info='назад'))
    
    else:
        await callback.message.edit_text(
            text=await print_day(user, page, True),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons_more_info='<',
                                            view_lessons='инфо',
                                            tomorrow_lessons_more_info='>',
                                            log_button='назад'))    
        
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()
    
    
@router.callback_query(F.data == 'tomorrow_lessons_more_info')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    week_number = date.today().weekday()
   
    page = int(redis_connect.get(name=id))+1
    page_day_number = (date.today() + timedelta(page)).weekday()
    if page_day_number == 6:
        page += 1
    
    if page != 0:
        if page + week_number == 12:
            await callback.message.edit_text(
            text=await print_day(user, page, True),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons_more_info='<',
                                            view_lessons='инфо',
                                            pass_day=' ',
                                            today_lessons_more_info='назад'))
            
        else:
            await callback.message.edit_text(
                text=await print_day(user, page, True),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons_more_info='<',
                                                view_lessons='инфо',
                                                tomorrow_lessons_more_info='>',
                                                today_lessons_more_info='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page, True),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons_more_info='<',
                                            view_lessons='инфо',
                                            tomorrow_lessons_more_info='>',
                                            log_button='назад'))
        
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()

    