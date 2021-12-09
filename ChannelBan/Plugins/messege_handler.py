import asyncio

from loguru import logger
from pyrogram import Client, errors
from pyrogram.raw import types, functions
from pyrogram.raw.base import Update


@Client.on_raw_update()
async def message_handler(client: Client, update: Update, _, chats: dict):
    while True:
        try:
            # Check for message that are from channel
            if (not isinstance(update, types.UpdateNewChannelMessage) or
                    not isinstance(update.message.from_id, types.PeerChannel)):
                return

            # Basic data
            message = update.message
            chat_id = int(f"-100{message.peer_id.channel_id}")
            channel_id = int(f"-100{message.from_id.channel_id}")

            # Check for linked channel
            if ((message.fwd_from and 
                 message.fwd_from.saved_from_peer == message.fwd_from.from_id == message.from_id) or
                channel_id == chat_id):
                return

            # Delete the message sent by channel and ban it.
            await client.send(
                functions.channels.EditBanned(
                    channel=await client.resolve_peer(chat_id),
                    participant=await client.resolve_peer(channel_id),
                    banned_rights=types.ChatBannedRights(
                        until_date=0,
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_polls=True,
                    )
                )
            )
            await client.delete_messages(chat_id, message.id)
            logger.debug(f"Banned channel {channel_id} from group {chat_id}")

            break
        except errors.FloodWait as e:
            logger.debug(f"{e}, retry after {e.x} seconds...")
            await asyncio.sleep(e.x)
        except errors.ChatAdminRequired:
            pass
        except:  # noqa
            logger.exception("An exception occurred in message_handler")
            break
