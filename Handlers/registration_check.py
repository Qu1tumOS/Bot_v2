from aiogram import Router, F
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from Parser.parser import url_groups, group_to_group_gict
from Keyboard.inline_creator import create_inline_kb
from DataBase.dao import User


router = Router()

class RegisterCheck(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user = await User.user_info(callback.from_user.id)
        return user == None

class GroupCheck(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user = await User.user_info(callback.from_user.id)
        return user.group == None or user.subgroup == None


@router.callback_query(F.data != 'log_button', RegisterCheck())
async def check_register(callback: CallbackQuery):
    await callback.message.edit_text(
        text='тебя нет в базе',
        reply_markup=create_inline_kb(1,
                                      log_button='Регистрация')
    )
    await callback.answer()

@router.callback_query(~F.data.in_(url_groups), ~F.data.in_(['subgroup_1', 'subgroup_2', 'log_button', 'NST']), GroupCheck())
async def check_group(callback: CallbackQuery):
    user = await User.user_info(callback.from_user.id)

    if user.group == None:
        await callback.message.edit_text(
            text='Для начала выбери свою группу и подгруппу',
            reply_markup=create_inline_kb(6,
                                        **group_to_group_gict))

    elif user.subgroup == None:
        await callback.message.edit_text(
            text='Для начала выбери свою подгруппу',
            reply_markup=create_inline_kb(2,
                                          subgroup_1='1',
                                          subgroup_2='2',
                                          log_button='Назад'))

    else:
         await callback.message.edit_text(
            text=f'что-то пошло не так...\nПроверь информацию о себе',
            reply_markup=create_inline_kb(1,
                                          profile='Профиль'))
    await callback.answer()
