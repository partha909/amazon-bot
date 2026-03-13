from telethon import TelegramClient, events
import re
import requests

# TELEGRAM API
api_id = 35703686
api_hash = "c9cfc4dc32c1302b7f287b818b69e0f8"

# SOURCE CHANNEL
source_channels = [
-1001805243449,-1002165035485,-1001462060305,
]

# TARGET CHANNEL
target_channel = "bestdell90"

affiliate_tag = "partha07e-21"

client = TelegramClient("session", api_id, api_hash)

posted=set()

link_pattern=r"(https?://\S+)"


# expand amzn.to
def expand_url(url):

    try:
        r=requests.get(url,allow_redirects=True,timeout=10)
        return r.url
    except:
        return url


# replace affiliate
def add_affiliate(link):

    link=re.sub(r'([&?])tag=[^&]+','',link)

    if "?" in link:
        link+="&tag="+affiliate_tag
    else:
        link+="?tag="+affiliate_tag

    return link


@client.on(events.NewMessage(chats=source_channels))
async def handler(event):

    text=event.message.text

    if not text:
        return

    links=re.findall(link_pattern,text)

    for link in links:

        if "amazon" not in link and "amzn.to" not in link:
            continue

        if "amzn.to" in link:
            link=expand_url(link)

        link=add_affiliate(link)

        if link in posted:
            return

        posted.add(link)

        msg=f"""
🔥 Amazon Deal

🛒 BUY NOW
{link}
"""

        await client.send_message(
            target_channel,
            msg,
            link_preview=False
        )

        print("Posted:",link)


print("Amazon link repost bot running...")

client.start()
client.run_until_disconnected()