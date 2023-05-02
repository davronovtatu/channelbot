from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

post_callback=CallbackData("create_post","action")



menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✔️Chop Etish",callback_data=post_callback.new(action="post")),
            InlineKeyboardButton(text="❌Bekor qilish",callback_data=post_callback.new(action="cancel")),
        ],
    ]
)