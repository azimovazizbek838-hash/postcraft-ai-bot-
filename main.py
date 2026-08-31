import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from openai import AsyncOpenAI

# Maxfiy kalitlarni server environment'idan olamiz
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men sizning AI Post Generator yordamchingizman 🚀\n\n"
        "Menga Telegram kanalingiz uchun har qanday xom matn, g'oya yoki kalit so'zlarni yuboring. "
        "Men uni chiroyli formatlangan, emojilar va hesteglar bilan tayyor postga aylantirib beraman!"
    )

@dp.message(F.text)
async def generate_post(message: types.Message):
    status_msg = await message.answer("📝 Post tayyorlanmoqda, biroz kuting...")
    
    prompt = f"""
    Siz Telegram kanallari uchun professional SMM va kontent meykersiz. 
    Quyidagi matn yoki g'oyani Telegram kanal uchun ideal postga aylantiring:
    - Jozibali sarlavha qo'shing.
    - O'qishga qulay qilib abzatslarga bo'ling.
    - Ma'noga mos emojilardan foydalaning.
    - Oxirida 3-5 ta mos hesteg qo'shing.
    
    Mijoz yuborgan matn:
    {message.text}
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Siz tajribali Telegram SMM mutaxassisiz."},
                {"role": "user", "content": prompt}
            ]
        )
        ready_post = response.choices[0].message.content
        await status_msg.edit_text(ready_post)
    except Exception as e:
        await status_msg.edit_text(f"Xatolik yuz berdi: {str(e)}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
