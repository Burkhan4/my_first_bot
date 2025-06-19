from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import sqlite3
from dotenv import load_dotenv
from os import getenv

load_dotenv()
router = Router()

My_id = getenv("my_id")
@router.message(Command("register"))
async def register_user(msg: Message):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (msg.from_user.id, msg.from_user.username))
    conn.commit()
    conn.close()
    await msg.answer("✅ Siz muvaffaqiyatli ro'yhatdan o'tdingiz!")


@router.message(Command("add_category"))
async def add_category(msg: Message):
    if msg.from_user.id != int(My_id):
        await msg.answer("❌ Sizda ruxsat yo'q.")
        return

    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        await msg.answer("Kategoriya nomini yuboring: /add_category <nom>")
        return

    category_name = args[1]
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()
    conn.close()
    await msg.answer(f"✅ Kategoriya qo‘shildi: {category_name}")


@router.message(Command("add_product"))
async def add_product(msg: Message):
    if msg.from_user.id != int(My_id):
        await msg.answer("❌ Sizda ruxsat yo'q.")
        return

    parts = msg.text.split(maxsplit=4)
    if len(parts) < 5:
        await msg.answer("Mahsulot format: /add_product <nom> <narx> <kategoriya_id> <izoh>")
        return

    name, price, category_id, desc = parts[1], float(parts[2]), int(parts[3]), parts[4]

    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, category_id)
        VALUES (?, ?, ?, ?)
    """, (name, desc, price, category_id))
    conn.commit()
    conn.close()
    await msg.answer(f"✅ Mahsulot qo‘shildi: {name}")


@router.message(Command("products"))
async def list_products(msg: Message):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.price, c.name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await msg.answer("🚫 Mahsulotlar topilmadi.")
        return

    text = "\n\n".join([f"{r[0]} - {r[1]} so'm ({r[2]})" for r in rows])
    await msg.answer("📦 Mahsulotlar:\n\n" + text)


@router.message(Command("search"))
async def search_products(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        await msg.answer("Qidiruv uchun mahsulot nomini yozing: /search <so'z>")
        return

    search_term = args[1]
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE name LIKE ?", (f"%{search_term}%",))
    results = cursor.fetchall()
    conn.close()

    if results:
        text = "\n".join([f"{name} - {price} so'm" for name, price in results])
        await msg.answer("🔍 Natijalar:\n" + text)
    else:
        await msg.answer("🚫 Hech narsa topilmadi.")
