from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from Parser.week_lessons import print_day

import redis

router = Router()


@router.callback_query(F.data == 'view_lessons')
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
                text=await print_day(user, page),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                pass_day=' ',
                                                view_lessons_more_info='инфо',
                                                tomorrow_lessons='>',
                                                today_lessons='назад'))
        elif page + week_number == 12:
            await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            view_lessons_more_info='инфо',
                                            pass_day=' ',
                                            today_lessons='назад'))
            
        else:
            await callback.message.edit_text(
                text=await print_day(user, page),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons='<',
                                                view_lessons_more_info='инфо',
                                                tomorrow_lessons='>',
                                                today_lessons='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            view_lessons_more_info='инфо',
                                            tomorrow_lessons='>',
                                            log_button='назад'))
    await callback.answer()
    
    
@router.callback_query(F.data == 'today_lessons')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id = id)
    redis_connect = redis.Redis(host='localhost')
    
    page = int(redis_connect.get(name=id))
    
    if not page:
        redis_connect.set(name=id, value=0)
        page_day_number = (date.today() + timedelta(page)).weekday()
    elif page_day_number == 6:
        page += 1
    else:
        page = 0

        
    await callback.message.edit_text(
        text=await print_day(user, page),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        yesterday_lessons='<',
                                        view_lessons_more_info='инфо',
                                        tomorrow_lessons='>',
                                        log_button='назад'))
    
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    await callback.answer()
    

@router.callback_query(F.data == 'yesterday_lessons')
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
                text=await print_day(user, page),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons='<',
                                                view_lessons_more_info='инфо',
                                                tomorrow_lessons='>',
                                                today_lessons='назад'))
        else:
            await callback.message.edit_text(
                text=await print_day(user, page),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                pass_day=' ',
                                                view_lessons_more_info='инфо',
                                                tomorrow_lessons='>',
                                                today_lessons='назад'))
    
    else:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            view_lessons_more_info='инфо',
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
    week_number = date.today().weekday()
    
    
    page = int(redis_connect.get(name=id))+1
    page_day_number = (date.today() + timedelta(page)).weekday()
    
    if page_day_number == 6:
        page += 1
        
    
    
    if page != 0:
        if page + week_number == 12:
            await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            view_lessons_more_info='инфо',
                                            pass_day=' ',
                                            today_lessons='назад'))
            
        else:
            await callback.message.edit_text(
                text=await print_day(user, page),
                parse_mode='MarkdownV2',
                reply_markup=create_inline_kb(3,
                                                yesterday_lessons='<',
                                                view_lessons_more_info='инфо',
                                                tomorrow_lessons='>',
                                                today_lessons='назад'))
    else:
        await callback.message.edit_text(
            text=await print_day(user, page),
            parse_mode='MarkdownV2',
            reply_markup=create_inline_kb(3,
                                            yesterday_lessons='<',
                                            view_lessons_more_info='инфо',
                                            tomorrow_lessons='>',
                                            log_button='назад'))
    redis_connect.getset(name=id, value=page)
    redis_connect.close()
    
    await callback.answer()
    
@router.callback_query(F.data == 'pass_day')
async def log(callback: CallbackQuery):
    await callback.answer()
    
