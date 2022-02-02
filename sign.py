from telethon import TelegramClient

session_name = "genius15"
api_id = 10956225
api_hash = '78f50dacad7c81fbe9c7f14baf73f9fc'
with TelegramClient(session_name, api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
