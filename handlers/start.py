from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import UserRepository

# Определение состояний
class Form(StatesGroup):
    waiting_for_username = State()

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:

    user_repo = UserRepository()

    user = user_repo.get_user(user_id=str(message.from_user.id))

    if user is None:
        await message.answer(f"Привет! Для публикации вашего хайлайта, введите ваш логин с нашего сайта:")
        await state.set_state(Form.waiting_for_username)
    else:
        button = InlineKeyboardButton(text="Отправить сообщение, видео, фото", callback_data="send_message")
        button1 = InlineKeyboardButton(text="Изменить логин с сайта", callback_data="change_username")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [button1]])

        await message.answer(f"Ждём ваш хайлайт",
                             reply_markup=keyboard)

@start_router.message(Form.waiting_for_username)
async def process_username(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введите ваш логин. Отправьте текстовое сообщение с вашим логином.")
        return

    username = message.text.strip()  # Убираем лишние пробелы

    user_repo = UserRepository()
    user = user_repo.create_user(user_id=str(message.from_user.id), username=username)

    button = InlineKeyboardButton(text="Отправить сообщение, видео, фото", callback_data="send_message")
    button1 = InlineKeyboardButton(text="Изменить логин с сайта", callback_data="change_username")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [button1]])

    await message.answer(f"Авторизация выполнена, пришлите ваш момент", reply_markup=keyboard)
    await state.clear()



