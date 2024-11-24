from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# ВСТАВЬТЕ_СВОЙ_КЛЮЧ_API в строку ниже
api = '_________________________'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)
#kb.row kb.insert

kb_in = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
        ]
    ]
)
# keyb1 = InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')
# keyb2 = InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas')
# kb_in.add(keyb1,keyb2)
# #kb_in.add(keyb1,keyb2)


# start_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Формулы расчёта'),KeyboardButton(text='Формулы расчёта')],
#         [KeyboardButton(text='Формулы расчёта'),KeyboardButton(text='Формулы расчёта')]
#     ], resize_keyboard=True
# )


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer('Введите свой рост, см:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(gr=message.text)
    await message.answer('Введите свой вес, кг:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(we=message.text)
    data = await state.get_data()
    try:
        cal = int(data['we']) * 10 + 6.25 * int(data['gr']) - 5 * int(data['ag']) + 5
        await message.answer(f'Если вы мужчина, Ваша норма калорий в день составляет {cal}')
        await state.finish()
    except:
        await message.answer('Введены неверные данные! Необходимо вводить только цифры')
        await state.finish()
        await message.answer('Выберите опцию:', reply_markup=kb_in)