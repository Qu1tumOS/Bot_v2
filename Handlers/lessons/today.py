from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from Parser.week_lessons import print_day

router = Router()

@router.callback_query(F.data == 'day_0')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_01='<',
                                        more_info='инфо',
                                        day_1='>',
                                        log_button='назад'))
    await callback.answer()
    
@router.callback_query(F.data == 'day_1')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 1),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_0='<',
                                        more_info='инфо',
                                        day_2='>',
                                        log_button='назад'))
    await callback.answer()
    
@router.callback_query(F.data == 'day_2')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 2),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_1='<',
                                        more_info='инфо',
                                        day_3='>',
                                        log_button='назад'))
    await callback.answer()
    
@router.callback_query(F.data == 'day_3')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 3),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_2='<',
                                        more_info='инфо',
                                        day_4='>',
                                        log_button='назад'))
    await callback.answer()
    
@router.callback_query(F.data == 'day_4')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 4),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_3='<',
                                        more_info='инфо',
                                        day_5='>',
                                        log_button='назад'))
    await callback.answer()
      
@router.callback_query(F.data == 'day_5')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 5),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_4='<',
                                        more_info='инфо',
                                        day_6='>',
                                        log_button='назад'))
    await callback.answer()
       
@router.callback_query(F.data == 'day_6')
async def log(callback: CallbackQuery):
    user = await User.user_info(id = callback.from_user.id)
        
    await callback.message.edit_text(
        text=await print_day(user, 6),
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(3,
                                        day_5='<',
                                        more_info='инфо',
                                        day_7=' ',
                                        log_button='назад'))
    await callback.answer()
    
@router.callback_query(F.data == 'day_7')
async def log(callback: CallbackQuery):
    await callback.answer()