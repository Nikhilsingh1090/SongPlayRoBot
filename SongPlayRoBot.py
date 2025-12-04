# © TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
import yt_dlp
from youtubesearchpython import VideosSearch
import requests
import os
import time
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

@bot.on_message(filters.command(['start']))
async def start(client, message):
    TamilBots = (
        f'👋 Hello @{message.from_user.username}\n\n'
        'I Am 🎸 Song Play Bot\n\n'
        'Send The Name Of The Song You Want... 😍🥰🤗\n\n'
        'Type /s Song Name\n\n'
        'Eg. `/s Faded`'
    )
    await message.reply_text(
        text=TamilBots,
        quote=False,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('SUPPORT 👬', url='https://t.me/TamilSupport'),
                InlineKeyboardButton('ADD ME 🤗', url='https://t.me/SongProBot?startgroup=true')
            ]
        ])
    )

@bot.on_message(filters.command(['s']))
async def search_song(client, message):
    query = ' '.join(message.command[1:]).strip()
    if not query:
        await message.reply_text('Please provide a song name. Example: `/s Faded`', quote=True)
        return
    
    m = await message.reply_text('🔎 Searching the song...')
    
    try:
        # YouTube Search
        search = VideosSearch(query, limit=1)
        results = search.result()
        
        if not results['result']:
            await m.edit('Found Nothing. Try Changing The Spelling A Little 😕')
            return
        
        video = results['result'][0]
        link = video['link']
        title = video['title']
        thumbnail = video['thumbnails'][0]['url']
        duration = video.get('duration', 'N/A')
        views = video.get('viewCount', {}).get('text', 'Unknown')
        
        # Download thumbnail
        thumb_name = f'thumb{message.id}.jpg'
        try:
            thumb = requests.get(thumbnail, timeout=10)
            with open(thumb_name, 'wb') as f:
                f.write(thumb.content)
        except:
            thumb_name = None
        
        await m.edit("🔎 Downloading song... Please wait ⏳️")
        
        # Download audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.rsplit(".", 1)[0] + ".mp3"
        
        # Prepare caption
        caption = (
            f'🎧 **Title:** [{title[:35]}]({link})\n'
            f'⏳ **Duration:** `{duration}`\n'
            f'👁 **Views:** `{views}`\n\n'
            '💌 **By:** @SongPlayRoBot'
        )
        
        # Send audio
        await message.reply_audio(
            audio_file,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            quote=False,
            title=title[:64],
            thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None
        )
        
        await m.delete()
        
    except Exception as e:
        error_msg = str(e)[:100]
        await m.edit(f'❌ Error: {error_msg}\n\nReport to @TamilSupport')
        print(f"Error: {e}")
    
    finally:
        # Cleanup
        try:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
            if 'thumb_name' in locals() and thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")

if __name__ == "__main__":
    print("Bot starting...")
    bot.run()
