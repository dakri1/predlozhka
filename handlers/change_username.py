from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import UserRepository

# Определение состояний
class Form(StatesGroup):
    waiting_for_change_username = State()

change_username_route = Router()

ADMIN_CHAT_ID = '1290725432'  # Замените на ID вашего администратора

@change_username_route.callback_query(lambda c: c.data == "change_username")
async def handle_send_message(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.answer("Введите ваше имя")
    await state.set_state(Form.waiting_for_change_username)

@change_username_route.message(Form.waiting_for_change_username)
async def process_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введите ваш логин. Отправьте текстовое сообщение с вашим логином.")
        return

    username = message.text.strip()  # Убираем лишние пробелы
    user_repo = UserRepository()
    user = user_repo.get_user(user_id=str(message.from_user.id))

    user_repo.change_username(user_id=str(user.user_id), username=username)

    button = InlineKeyboardButton(text="Отправить сообщение, видео, фото", callback_data="send_message")
    button1 = InlineKeyboardButton(text="Изменить логин с сайта", callback_data="change_username")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [button1]])

    await message.answer("Ваш логин успешно изменен", reply_markup=keyboard)

    await state.clear()






