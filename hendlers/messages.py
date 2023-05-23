from aiogram import types,Dispatcher
from create_bot_and_logging import dp
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("Hi, iam zxcmusicbot,lets find music for you")
@dp.message_handler(commands='about')
async def about_message(messsage:types.Message):
    await messsage.reply('Its bot was developed by Student of Symy State Unevrsity Yurev Daniil IT-92')
@dp.message_handler(commands='help')
async def help_messages(message:types.Message):
    await message.reply('If you want find music,please type /yt song name')

def registr_hendlers_messages(dp:Dispatcher):
    dp.register_message_handler(send_welcome,commands='start'),
    dp.register_message_handler(about_message,commands='about'),
    dp.register_message_handler(help_messages,commands='help'),