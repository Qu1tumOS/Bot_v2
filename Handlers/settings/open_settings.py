from aiogram import Router, F
from aiogram.types import CallbackQuery

from Keyboard.inline_creator import create_inline_kb

router = Router()

@router.callback_query(F.data == 'settings')
async def log(callback: CallbackQuery):
    await callback.message.edit_text(
        text='меню',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(1,
                                        profile='Профиль 👤',
                                        archive='Архив',
                                        support='Поддержка',
                                        log_button='назад'))
    await callback.answer()
    