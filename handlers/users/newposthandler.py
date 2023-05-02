from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from loader import dp,bot
from keyboards.inline.inlinemenu import menu,post_callback
from states.post import NewPost
from aiogram.dispatcher import FSMContext




# create_post   komandasi uchun handlers



@dp.message_handler(commands="create_post")
async def select_post(message:types.Message):
    await message.answer("Kanalga yuborish uchun Post yuboring")
    await NewPost.NewMessage.set()


@dp.message_handler(state=NewPost.NewMessage)
async def enter_message(message:types.Message,state:FSMContext):
    await state.update_data(text=message.html_text,mention=message.from_user.get_mention())
    await message.answer(f"Postni tekshirish uchun yuboraymi ?",reply_markup=menu)
    await NewPost.next()


@dp.callback_query_handler(post_callback.filter(action="post"),state=NewPost.Confirm)
async def select_message(call:CallbackQuery,state:FSMContext):
    async with state.proxy() as data:
        text=data.get("text")
        mention=data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post adminga yuborildi")
    await bot.send_message(ADMINS[0],f"Foydalanuvchi {mention} quyidagi postni yubormoqchi")
    await bot.send_message(ADMINS[0],text,parse_mode="HTML",reply_markup=menu)



@dp.callback_query_handler(post_callback.filter(action="cancel"),state=NewPost.Confirm)
async def calback_cancel(call:CallbackQuery,state:FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Rad etilidi")


@dp.message_handler(state=NewPost.Confirm)
async def select_menu(message:types.Message):
    await message.answer("Rad etish yoki yuborish tugmasini bosing")


#adminlar uchun

@dp.callback_query_handler(post_callback.filter(action="post"),user_id=ADMINS)
async def sen_post_admin(call:CallbackQuery):
    await call.answer("Chop etishga ruxsat berdingiz",show_alert=True)
    channell="@testchannelbotuchun"
    message =await call.message.edit_reply_markup()
    await message.send_copy(chat_id=channell)


@dp.callback_query_handler(post_callback.filter(action="cancel"),user_id=ADMINS)
async def sen_post_admin(call:CallbackQuery):
    await call.answer("Rad etildi",show_alert=True)
    await call.message.edit_reply_markup()