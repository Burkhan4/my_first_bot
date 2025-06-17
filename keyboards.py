from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def answer_options_keyboard(question_id: int, options: list[str]):
    buttons = [
        [InlineKeyboardButton(text=option, callback_data=f"{question_id}:{option}")]
        for option in options
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def test_count_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="3 ta savol", callback_data="test:3")],
        [InlineKeyboardButton(text="5 ta savol", callback_data="test:5")],
        [InlineKeyboardButton(text="10 ta savol", callback_data="test:10")],
    ])
