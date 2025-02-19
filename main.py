from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram import Bot,Dispatcher,types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from asyncio import sleep
import requests
import asyncio

ESP32_IP="http://192.168.1.100:8000" 

bot=Bot(token="7421660198:AAHoxDOM6VocJccGd2UEg7DB0RP2JPjBD3k")
dp=Dispatcher()
sugormoqda=False
admin=""

osimliklar = {
    "Kaktus 🌵": "30",
    "Orxideya 🌺": "60",
    "Spathiphyllum 🍀": "70",
    "Fikus 🌿": "50",
    "Aloe Vera 🌵": "40",
    "Sansevieriya 🪴": "35",
    "Dratsena 🎋": "55",
    "Monstera 🍃": "65",
    "Benjamin fukusi 🌳": "45",
    "Dollar gul 💰": "40",
    "Begoniya 🌸": "60",
    "Geran 🌷": "50",
    "Kalateya 🍂": "75",
    "Anturium ❤️": "65",
    "Gloxinia 🌼": "55"
}

def get_keyboard(on: bool):
    if on:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="❌ To'xtatish"),KeyboardButton(text="O'simlik holati🪴")],[KeyboardButton(text="O'zimlikni tanlash🌴")]],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Sugo'rish 🚰"),KeyboardButton(text="O'simlik holati🪴")],[KeyboardButton(text="O'zimlikni tanlash🌴")]],
            resize_keyboard=True
        )



@dp.message(Command("start"))
async def start(msg:Message):
    await msg.react([types.ReactionTypeEmoji(emoji='🔥')])
    async with ChatActionSender.typing(bot=bot,chat_id=msg.from_user.id):
        await sleep(0.5)
        await msg.answer(f"<i>Assalomu alykum <b>{msg.from_user.full_name}</b> 👋. Botga hush kelibsiz. Biz bilan yashillikni asrang 🍀.</i>",parse_mode="html",reply_markup=get_keyboard(on=False))


@dp.message()
async def command(msg:Message):
    global sugormoqda,osimliklar
    text=msg.text        
    osimlik=next((name for name in osimliklar if name in text), None)
    if text=="Sugo'rish 🚰":
        sugormoqda=True
        async with ChatActionSender.typing(bot=bot,chat_id=msg.from_user.id):
            await sleep(0.5)
            await msg.answer("<b>Boshlandi!</b>",reply_markup=get_keyboard(on=True),parse_mode="html")
    elif text=="❌ To'xtatish":
        sugormoqda=False
        async with ChatActionSender.typing(bot=bot,chat_id=msg.from_user.id):
            await sleep(0.5)
            await msg.answer("<b>Tugatildi!</b>",parse_mode="html",reply_markup=get_keyboard(on=False))
    elif text=="O'zimlikni tanlash🌴":
        buttons = [KeyboardButton(text=name) for name in osimliklar.keys()]  
        keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)] 
        async with ChatActionSender.typing(bot=bot,chat_id=msg.from_user.id):
            await sleep(0.5)
            await msg.answer("<i>Gulingizni tanlang. 🌸</i>",parse_mode="html",reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard))
    elif osimlik:
        async with ChatActionSender.typing(bot=bot,chat_id=msg.from_user.id):
            await sleep(0.5)
            namlik=osimliklar[osimlik]
            await msg.reply("<b>Gulingiz tanlandi shu moslashuvda ishlaymiz.</b>",parse_mode="html")
            await msg.answer(f"<b>{osimlik}</b> uchun tuproq namligi <code>{namlik}%</code> deb tafsiya etilgan.",parse_mode="html",reply_markup=get_keyboard(on=False))
    elif text=="O'simlik holati🪴":
        try:
            response = requests.get(f"{ESP32_IP}/data") 
            if response.status_code == 200:
                data = response.json()
                namlik = data.get("namlik", "Noma’lum")
                await msg.answer(f"O'simlik tuproq namligi: {namlik}%")
            else:
                await msg.answer("ESP32 bilan bog'lanib bo'lmadi! 😕")
        except Exception as e:
            await msg.answer(f"*Xatolik yuz berdi*:```{e}```",parse_mode="markdown")

async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())

