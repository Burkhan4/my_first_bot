from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from db import get_random_questions
from keyboards import answer_options_keyboard, test_count_keyboard
import random

user_sessions = {}

router = Router()

@router.message(Command("test"))
async def test_command(msg: Message):
    await msg.answer("Nechta savol yechmoqchisiz?", reply_markup=test_count_keyboard())

@router.callback_query(F.data.startswith("test:"))
async def handle_test_start(callback: CallbackQuery):
    count = int(callback.data.split(":")[1])
    questions = get_random_questions(count)
    user_sessions[callback.from_user.id] = {
        "questions": questions,
        "current": 0,
        "correct": 0,
    }
    await send_question(callback.message, callback.from_user.id)

async def send_question(message: Message, user_id: int):
    session = user_sessions[user_id]
    index = session["current"]
    if index >= len(session["questions"]):
        await message.answer(
            f"Test yakunlandi. To‘g‘ri javoblar soni: {session['correct']} / {len(session['questions'])}"
        )
        del user_sessions[user_id]
        return

    q = session["questions"][index]
    country, correct, opt1, opt2, opt3 = q[1], q[2], q[3], q[4], q[5]
    options = [correct, opt1, opt2, opt3]
    random.shuffle(options)

    await message.answer(
        f"{index+1}-savol: {country} davlatining poytaxti qaysi?",
        reply_markup=answer_options_keyboard(q[0], options)
    )

@router.callback_query(F.data.regexp(r"^\d+:.+"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_sessions:
        await callback.answer("Avval testni boshlang!", show_alert=True)
        return

    question_id, answer = callback.data.split(":")
    session = user_sessions[user_id]
    question = next(q for q in session["questions"] if str(q[0]) == question_id)

    if answer == question[2]:
        session["correct"] += 1
        await callback.message.answer("✅ To‘g‘ri!")
    else:
        await callback.message.answer(f"❌ Noto‘g‘ri! To‘g‘ri javob: {question[2]}")

    session["current"] += 1
    await send_question(callback.message, user_id)
