from aiogram import executor
from create_bot_and_logging import dp
from hendlers import music_search_and_recomend_handler
from hendlers import messages
messages.registr_hendlers_messages(dp)
music_search_and_recomend_handler.registr_hendlers_messages(dp)
music_search_and_recomend_handler.callback_hendlers(dp)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)