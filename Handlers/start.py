from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User
from datetime import date
from Parser.parser import group_to_group_gict, url_groups

import redis


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
            text="Войди в аккаунт или пройди небольшую регистрацию",
            reply_markup=create_inline_kb(1,
                                        log_button='Вход')
            )


@router.callback_query(F.data == 'log_button')
async def log(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(callback.from_user.id)
    redis_connect = redis.Redis(host='localhost')
    redis_connect.getset(name=f'more_info_{id}', value=-1)
    redis_connect.close()
    
    if not user:
        await User.add(id=callback.from_user.id,
                       name=callback.from_user.username,
                       user_name=callback.from_user.first_name,
                       date_of_registration=date.today())

        await callback.message.edit_text(
            text='Выбери свою группу и подгруппу',
            reply_markup=create_inline_kb(6,
                                          **group_to_group_gict))
        
    elif not user.subgroup:
        await callback.message.edit_text(
            text='Выбери свою группу и подгруппу',
            reply_markup=create_inline_kb(6,
                                          **group_to_group_gict))

    else:
        await callback.message.edit_text(
            text=f'•{" "*40}•',
            reply_markup=create_inline_kb(2,
                                          today_lessons='пары',
                                          settings='меню',
                                          fast_success='быстрый доступ'))
    await callback.answer()
    




@router.callback_query(F.data.in_(group_to_group_gict))
async def add_group(callback: CallbackQuery):
    id = callback.from_user.id
    user = await User.user_info(id)
    await User.update_user(id, group=int(callback.data))
    
    if user.subgroup == None:
        await callback.message.edit_text(
            text='Выберите свою подгруппу',
            reply_markup=create_inline_kb(2,
                                          subgroup_1='1',
                                          subgroup_2='2',
                                          log_button='Назад')
        )
    await callback.answer()

@router.callback_query(F.data.in_(['subgroup_1', 'subgroup_2']))
async def add_subgroup(callback: CallbackQuery):
    id = callback.from_user.id
    await User.update_user(id, subgroup=int(callback.data[-1]))
    
    await callback.message.edit_text(
            text=f'•{" "*40}•',
            reply_markup=create_inline_kb(2,
                                          today_lessons='пары',
                                          settings='меню',
                                          fast_success='быстрый доступ'))
    await callback.answer()