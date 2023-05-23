import logging
from aiogram import Bot, Dispatcher
from config_reader import config
import spotipy
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from spotipy.oauth2 import SpotifyClientCredentials
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
spotify_client_id = '4c0642c263394f1c8e6034f55ca27b94'
spotify_client_secret = 'df7f92496f7d41958491146901665f93'
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))
