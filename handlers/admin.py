from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import UserRepository, AdminRepository


class Form(StatesGroup):
    waiting_for_id = State()
    remove_admin = State()
    waiting_for_message_id = State()

admin_router = Router()


@admin_router.message(Command("admin"))
async def command_start_handler(message: Message) -> None:
    user_repo = AdminRepository()
    user = user_repo.get_admin(user_id=str(message.from_user.id))

    if user is not None:
        button = InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")
        button1 = InlineKeyboardButton(text="Удалить админа", callback_data="remove_admin")
        button2 = InlineKeyboardButton(text="Отправить сообщение пользователю", callback_data="send_message_to_user")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], [button1], [button2]])

        await message.answer(f"Admin panel)",
                             reply_markup=keyboard)

@admin_router.callback_query(lambda c: c.data == "send_message_to_user")
async def send_message_to_user(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_repo = AdminRepository()
    user = user_repo.get_admin(user_id=str(callback_query.from_user.id))

    if user is not None:
        await callback_query.answer()
        await callback_query.message.answer('Введите telegram id пользователя, затем сообщение (Пример: 123456789 Сообщение пользователю).')

        await state.set_state(Form.waiting_for_message_id)


@admin_router.message(Form.waiting_for_message_id)
async def get_telegram_id(message: Message, state: FSMContext) -> None:
    input_data = message.text.strip().split(' ', 1)  # Ожидаем, что сообщение будет в формате: ID текст

    if len(input_data) < 2:
        await message.answer(
            "Формат неверный. Пожалуйста, введите telegram id и сообщение (Пример: 123456789 Сообщение пользователю).")
        return

    chat_id, msg_text = input_data[0], input_data[1]

    try:
        await message.bot.send_message(chat_id, 'Сообщение от администратора:\n' + msg_text)  # Отправляем сообщение
        await message.answer("Сообщение успешно отправлено.")
    except Exception as e:
        await message.answer(f"Не удалось отправить сообщение. Ошибка: {str(e)}")

    await state.clear()

@admin_router.callback_query(lambda c: c.data == "add_admin")
async def add_admin(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_repo = AdminRepository()
    user = user_repo.get_admin(user_id=str(callback_query.from_user.id))

    if user is not None:
        await callback_query.message.answer('Введите telegram id пользователя')

        await state.set_state(Form.waiting_for_id)

@admin_router.message(Form.waiting_for_id)
async def get_telegram_id(message: Message, state: FSMContext) -> None:
    tg_id = message.text

    admin_repo = AdminRepository()

    admin_repo.create_admin(tg_id)

    await message.answer('Админ успешно добавлен')

    await state.clear()


@admin_router.callback_query(lambda c: c.data == "remove_admin")
async def add_admin(callback_query: CallbackQuery, state: FSMContext) -> None:

    user_repo = AdminRepository()
    user = user_repo.get_admin(user_id=str(callback_query.from_user.id))

    if user is not None:
        await callback_query.message.answer('Введите telegram id пользователя')

        await state.set_state(Form.remove_admin)

@admin_router.message(Form.remove_admin)
async def get_telegram_id(message: Message, state: FSMContext) -> None:
    tg_id = message.text

    admin_repo = AdminRepository()

    admin_repo.delete_admin(tg_id)

    await message.answer('Админ успешно удален')

    await state.clear()



