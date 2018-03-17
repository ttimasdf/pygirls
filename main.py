#!/usr/bin/env python3
from pathlib import Path
from pyrogram import Client
from pyrogram.api import functions

SESSION_NAME = 'girls_py'


def main():
    client = Client(SESSION_NAME)
    client.start()

    for dialog in client.send(functions.messages.GetDialogs()).dialogs:
        group_name = client.resolve_peer(dialog.peer)
        print(group_name)

if __name__ == '__main__':
    main()
