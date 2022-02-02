from telethon import TelegramClient
import json
import random
import time
import asyncio
from telethon.tl.functions.channels import JoinChannelRequest


class Group:
    def __init__(self, group_id, group_interval):
        self.group_id = group_id
        if group_interval == 0:
            group_interval = 1
        self.interval = group_interval
        self.current_index = 0


api_id = 10956225
api_hash = '78f50dacad7c81fbe9c7f14baf73f9fc'
messages = []
accounts = []
message_count = 0
account_count = 0

clients = []

groups = []


def get_groups():
    f = open('groups.json')
    data = json.load(f)
    global groups
    json_groups = data["accounts"]
    for json_group in json_groups:
        group_id = json_group["groupID"]
        group_interval = json_group["intervalMin"]
        group = Group(group_id, group_interval)
        global groups
        groups.append(group)


def get_messages():
    message_file = open('messages.txt', 'r')
    global messages
    messages = message_file.readlines()
    global message_count
    message_count = len(messages)


def get_accounts():
    f = open('accounts.json')
    account = json.load(f)
    global api_id
    global api_hash
    api_id = account["api_id"]
    api_hash = account["api_hash"]
    global accounts
    accounts = account["accounts"]
    global account_count
    account_count = len(accounts)


async def get_profile(client):
    async with client:
        me = await client.get_me()
        username = me.username
        print("{} : connected".format(username))


async def main():
    while True:
        for index, group in enumerate(groups):
            # print("index {}:{}".format(index, groups[index].current_index))
            if (group.current_index == 0):
                # priZnt("send message  {}".format(index))
                for account in accounts:
                    client = TelegramClient(account, api_id, api_hash)
                    clients.append(client)
                if message_count == 0 or account_count == 0:
                    return
                message_index = random.randint(0, message_count - 1)
                account_index = random.randint(0, account_count - 1)
                message = messages[message_index]
                client = clients[account_index]
                async with client:
                    try:
                        await client(JoinChannelRequest(group.group_id))
                        await client.send_message(group.group_id, message)
                    except:
                        print("Please check this group agian : ",group.group_id)
            groups[index].current_index = (groups[index].current_index + 1) % groups[index].interval
        time.sleep(60)


def init():
    get_messages()
    get_accounts()
    get_groups()


if __name__ == "__main__":
    init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
