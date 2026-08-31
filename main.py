import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from openai import AsyncOpenAI

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not BOT_TOKEN:
    print("XATO: BOT_TOKEN Environment Variable topilmadi!")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("XATO: OPENAI_API_KEY Environment Variable topilmadi!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men sizning AI Post Generator yordamchingizman 🚀\n\n"
        "Menga Telegram kanalingiz uchun har qanday xom matn yoki g'oyani yuboring."
    )

@dp.message(F.text)
async def generate_post(message: types.Message):
    status_msg = await message.answer("📝 Post tayyorlanmoqda, biroz kuting...")
    
    prompt = f"""
    Siz Telegram kanallari uchun professional SMM mutaxassisiz. 
    Quyidagi matnni Telegram kanal uchun ideal postga aylantiring:
    - Jozibali sarlavha qo'shing.
    - O'qishga qulay qilib abzatslarga bo'ling.
    - Ma'noga mos emojilardan foydalaning.
    - Oxirida 3-5 ta mos hesteg qo'shing.
    
    Matn: {message.text}
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz Telegram SMM mutaxassisiz."},
                {"role": "user", "content": prompt}
            ]
        )
        ready_post = response.choices[0].message.content
        await status_msg.edit_text(ready_post)
    except Exception as e:
        await status_msg.edit_text(f"Xatolik: {str(e)}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
