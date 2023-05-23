from aiogram import types, Dispatcher
import yt_dlp
import os
import time
from create_bot_and_logging import dp, sp, bot
async def search_spotify(query):
    results = sp.search(q=query, limit=1, type='track')
    tracks = results['tracks']['items']
    return tracks

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames=[]
        self.filenames.append(information["filepath"])
        return [], information

async  def search_similar_tracks(query):
    results = sp.search(q=query, limit=5, type='track')
    tracks = results['tracks']['items']
    return tracks

@dp.callback_query_handler(lambda c: c.data.startswith('similar'))
async def process_similar_callback(callback_query: types.CallbackQuery):
    query = callback_query.data.split(':')[1]
    tracks = await search_similar_tracks(query)
    if not tracks:
        await callback_query.answer("Unfortunately, I could not find any similar songs.")
        return

    similar_tracks_message = "Here are some similar tracks:\n"
    for track in tracks:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        track_url = track['external_urls']['spotify']
        similar_tracks_message += f"{track_name} by {artist_name}\n{track_url}\n\n"

    await bot.send_message(callback_query.from_user.id, similar_tracks_message)

@dp.message_handler(commands=['yt'])
async def youtube(message: types.Message):
    arguments = message.get_args()
    query = arguments
    tracks = await search_spotify(query)
    if not tracks:
        await message.reply("Unfortunately, I could not find any songs for your query.")
        return

    track = tracks[0]
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    track_url = track['external_urls']['spotify']
    await message.reply("Please wait...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': "ytsearch",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        filename_collector = FilenameCollectorPP()
        ydl.add_post_processor(filename_collector)
        ydl.download([arguments])
        file_path = filename_collector.filenames[0]

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        youtube_button = types.InlineKeyboardButton(text="YouTube", url=f"https://www.youtube.com/results?search_query={query}")
        spotify_button = types.InlineKeyboardButton(text="Spotify", url=track_url)
        similar_button = types.InlineKeyboardButton(text="Similar tracks", callback_data=f"similar:{track['artists'][0]['name']}")
        keyboard.add(youtube_button, spotify_button, similar_button)

        with open(file_path, 'rb') as audio_file:
            caption = f"<b>{track_name}</b> by <i>{artist_name}</i>"
            await message.reply_document(audio_file, caption=caption, reply_markup=keyboard, parse_mode='HTML')
        time.sleep(5)
        os.remove(filename_collector.filenames[0])
        return filename_collector.filenames[0]


def registr_hendlers_messages(dp:Dispatcher):
    dp.register_message_handler(youtube,commands='yt')

def callback_hendlers(dp:Dispatcher):
    dp.callback_query_handler(process_similar_callback)