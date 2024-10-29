from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import date, timedelta
from calendar import monthrange, monthcalendar
from DataBase.dao import Lesson, User
import asyncio

from Keyboard.inline_creator import create_inline_kb

router = Router()

dates = list()
async def get_dates_from_db():
    if dates:
        dates.clear()
    dates = [str(i.day) for i in await Lesson.find_all()]
    print(dates)


@router.callback_query(F.data == 'settings')
async def log(callback: CallbackQuery):
    await get_dates_from_db()
    
    await callback.message.edit_text(
        text='меню',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(1,
                                        profile='Профиль 👤',
                                        archive='Архив',
                                        support='Поддержка',
                                        log_button='назад'))
    await callback.answer()
    
async def create_dict_for_keyboard(year : int, month :int):
    weekday = date(year, month, 1).weekday()                                        #день недели первого дня месяца
    dates_dict = {f'{i}':'ㅤ' for i in range(weekday)}                              #заполняем словарь пустыми кнопками до первого числа
    
    for i in range(1, monthrange(year, month)[1]+1):                                #заполняем словарь датами на месяц
        date_dt = date(year, month, i)                                              #дата в формате datetime
        
        if date_dt.weekday() != 6:                                                  #если этот день не воскресенье то продолжаем
            check = await Lesson.find_one_or_none(day=date_dt)                      #проверяем есть ли в БД расписание на этот день
            dates_dict[f'{date_dt:%Y-%m-%d}'] = 'ㅤ'                                #заполняем кнопку пустым значением
            
            if check:                                                               #если же в базе есть этот день
                dates_dict[f'{date_dt:%Y-%m-%d}'] = f'{date_dt:%Y-%m-%d}'[8:]       #переписываем значение
                
    max_len = [36, 30][len(dates_dict) <= 30]                                       #длина до которой нужно дополнить словарь (30 или 36)
    
    while len(dates_dict) < max_len:                                                #пока длина словаря не достигла нужного значения
        dates_dict[f'{len(dates_dict)}'] = 'ㅤ'                                      #добавляем в словарь пустые значения
    
    return dates_dict # возвращаем словарь

@router.callback_query(F.data == 'archive')
async def beta_button_2(callback: CallbackQuery):
    month = f'{date.today():%m}'
    new_dict = await create_dict_for_keyboard(2024, int(month))
    
    await callback.message.edit_text(
        text=f'`•             месяц            •\nпн    вт    ср    чт    пт    сб\nㅤ`',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(6,
                                      **new_dict,
                                      settings='назад'))
    await callback.answer('бета')

        

@router.callback_query(F.data.in_(dates))
async def print_day22(callback: CallbackQuery):
    
    print(dates)
    await callback.message.edit_text(
        text=f'`good`',
        parse_mode='MarkdownV2',
        reply_markup=create_inline_kb(1,
                                      archive='назад'))
    await callback.answer()
    
    