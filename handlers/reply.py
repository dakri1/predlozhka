from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from database.database import UserRepository, AdminRepository


# Определение состояний
class Form(StatesGroup):
    waiting_for_message = State()


reply_router = Router()

ADMIN_CHAT_ID = '1290725432'  # Замените на ID вашего администратора

@reply_router.message(Command('cancel'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Отменено')

    await state.clear()

@reply_router.callback_query(lambda c: c.data == "send_message")
async def handle_send_message(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await callback_query.message.answer("Пожалуйста, пришлите ваш момент")
    await state.set_state(Form.waiting_for_message)


@reply_router.message(Form.waiting_for_message)
async def process_message(message: Message, state: FSMContext) -> None:
    user_repo = UserRepository()
    user = user_repo.get_user(user_id=str(message.from_user.id))

    current_date = datetime.now().date()
    count = user_repo.get_message_count(user_id=str(message.from_user.id))
    reset_date = user_repo.get_reset_date(user_id=str(message.from_user.id))

    if reset_date and datetime.strptime(reset_date, "%Y-%m-%d").date() < current_date:
        user_repo.reset_message_count_and_date(user_id=str(message.from_user.id))
        count = 0

    if count >= 10:
        await message.answer("Вы достигли лимита на отправку сообщений. Пожалуйста, попробуйте завтра.")
        return

    if message.content_type == types.ContentType.TEXT:
        await process_text_message(message, state, user)
    elif message.content_type == types.ContentType.VIDEO:
        await process_video_message(message, state, user)
    elif message.content_type == types.ContentType.PHOTO:
        await process_photo_message(message, state, user)

        # Увеличиваем счетчик и устанавливаем дату сброса
    user_repo.increment_message_count(user_id=str(message.from_user.id))
    user_repo.set_reset_date(user_id=str(message.from_user.id), date=str(current_date))
    # Add condition for link or any other content types if needed


async def process_text_message(message: Message, state: FSMContext, user) -> None:
    # Your text message processing logic here
    admin_repo = AdminRepository()
    user_repo = UserRepository()

    admins = admin_repo.get_all_admins()

    for admin in admins:
        await message.bot.send_message(admin.user_id, f"Telegram id: {message.from_user.id}\n"
                                                      f"Username: {user.username}\n"
                                                      f"Message: {message.text}")
    await message.answer("Спасибо за ваш хайлайт, ожидайте результата в скором времени")

    await state.clear()



async def process_video_message(message: Message, state: FSMContext, user) -> None:
    # Ваше видео сообщение обработка здесь

    admin_repo = AdminRepository()

    admins = admin_repo.get_all_admins()

    # Проверяем, что у нас есть видео для отправки
    if message.video:
        for admin in admins:
            await message.bot.send_video(admin.user_id, message.video.file_id,
                                         caption=f"Telegram id: {message.from_user.id}\n"
                                                 f"Username: {user.username}"
                                                 )

    await message.answer("Спасибо за ваш хайлайт, ожидайте результата в скором времени")

    await state.clear()


async def process_photo_message(message: Message, state: FSMContext, user) -> None:

    if message.photo:
        best_photo = message.photo[-1]

        media = {
            'type': 'photo',
            'media': best_photo.file_id,
            'caption': f"User: {message.from_user.id}\nUsername: {user.username}"
        }

        admin_repo = AdminRepository()

        admins = admin_repo.get_all_admins()

        for admin in admins:
            await message.bot.send_photo(admin.user_id, media['media'], caption=media['caption'])

    await message.answer("Спасибо за ваш хайлайт, ожидайте результата в скором времени")

    await state.clear()

