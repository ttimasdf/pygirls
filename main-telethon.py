#!/usr/bin/env python3
import socks
from pathlib import Path
from math import log, ceil
from telethon import TelegramClient, utils
from telethon.tl.types import Message, MessageMediaPhoto, MessageMediaDocument, PhotoCachedSize
from telethon.tl.functions.upload import GetFileRequest
from config import api_id, api_hash, socks_host, socks_port

SESSION_NAME = 'girls_py'

def main():
    if socks_host and socks_port:
        client = TelegramClient(SESSION_NAME, api_id, api_hash, proxy=(socks.SOCKS5, socks_host, socks_port))
    else:
        client = TelegramClient(SESSION_NAME, api_id, api_hash)

    client.start()

    # print(client.get_me().stringify())

    root = Path("downloads")

    for dialog in client.get_dialogs():
        group_name = utils.get_display_name(dialog.entity)
        print("Fetching", group_name)
        for msg in client.get_messages(dialog.entity, limit=10):
            if isinstance(msg, Message) and msg.media is not None:
                media = msg.media
                print(msg)
                if isinstance(media, MessageMediaPhoto):
                    media.photo.sizes.sort(
                        key=lambda s: len(s.bytes) if isinstance(s, PhotoCachedSize) else s.size
                    )
                    loc = media.photo.sizes[-1].location
                    size = media.photo.sizes[-1].size
                    suffix = ".jpg"
                elif isinstance(media, MessageMediaDocument) and "video" in media.document.mime_type:
                    loc = media.document
                    size = media.document.size
                    suffix = '.mp4'
                else:
                    continue
                
                target = root / ''.join(' ' if c in '*!|#$`~&;\'"/\\' else c for c in group_name) / (str(msg.id) + suffix)

                target.parent.mkdir(parents=True, exist_ok=True)

                with target.open('wb') as f:
                    print("Downloading", target.name, "...", end='')
                    import pdb; pdb.set_trace()
                    bytes = client(GetFileRequest(loc, 0, pow(2, ceil(log(size, 2))))).bytes
                    f.write(bytes)
                    print("saved")

if __name__ == '__main__':
    main()
