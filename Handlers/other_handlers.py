from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


router = Router()


@router.message()
async def delete_message(message: Message):
    await message.delete()
    
@router.callback_query(F.data.in_(['profile', 'support', 'fast_success']))     
async def answer(callback: CallbackQuery):
    await callback.answer('в разработке')
