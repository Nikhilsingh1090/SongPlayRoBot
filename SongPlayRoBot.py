# © TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl
from youtube_search import YoutubeSearch
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

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time_str):
    stringt = str(time_str)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = (
        f'👋 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\n'
        '𝗜 𝗔𝗺 🎸𝐒𝐨𝐧𝐠 𝐏𝐥𝐚𝐲 𝐁𝐨𝐭[🎶](https://telegra.ph/file/6cb884fe1cb943ec12df1.mp4)\n\n'
        '𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗡𝗮𝗺𝗲 𝗢𝗳 𝗧𝗵𝗲 𝗦𝗼𝗻𝗴 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁... 😍🥰🤗\n\n'
        '𝗧𝘆𝗽𝗲 /s 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲\n\n'
        '𝐄𝐠. `/s Faded`'
    )
    message.reply_text(
        text=TamilBots,
        quote=False,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('𝐒𝐔𝐏𝐏𝐎𝐑𝐓 👬', url='https://t.me/TamilSupport'),
                InlineKeyboardButton('𝐀𝐃𝐃 𝐌𝐄 🤗', url='https://t.me/SongProBot?startgroup=true')
            ]
        ])
    )


@bot.on_message(filters.command(['s']))
def a(client, message):
    # build query from command args
    query = ' '.join(message.command[1:]).strip()
    if not query:
        message.reply_text('Please provide a song name. Example: `/s Faded`', quote=True)
        return

    print("Search query:", query)
    m = message.reply_text('🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1

        if not results:
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 😕')
            return

        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0].get("views", "Unknown")
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
        except Exception as e:
            print("Result parsing error:", e)
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 😕')
            return
    except Exception as e:
        m.edit(
            "✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n"
            "𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲.\n\nEg.`/s Faded`"
        )
        print("Search exception:", str(e))
        return

    m.edit("🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐀 𝐒𝐨𝐧𝐠 🎶 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 ⏳️ 𝐅𝐨𝐫 𝐅𝐞𝐰 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 [🚀](https://telegra.ph/file/67f41ae52a85dfc0551ae.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            # This actually downloads when we process info
            ydl.process_info(info_dict)

        # Build caption using the real video link
        rep = (
            f'🎧 𝐓𝐢𝐭𝐥𝐞 : [{title[:35]}]({link})\n'
            f'⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{duration}`\n'
            f'🎬 𝐒𝐨𝐮𝐫𝐜𝐞 : [Youtube]({link})\n'
            f'👁‍🗨 𝐕𝐢𝐞𝐰𝐬 : `{views}`\n\n'
            '💌 𝐁𝐲 : @SongPlayRoBot'
        )
        # convert duration to seconds
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60

        # send audio
        message.reply_audio(audio_file, caption=rep, parse_mode="markdown", quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ 𝐄𝐫𝐫𝐨𝐫\n\n Report This Error To Fix @TamilSupport ❤️')
        print("Download/send error:", e)
    finally:
        # cleanup only if files exist
        try:
            if 'audio_file' in locals() and os.path.exists(audio_file):
                os.remove(audio_file)
            if 'thumb_name' in locals() and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("Cleanup error:", e)


bot.run()
