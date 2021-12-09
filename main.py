from asyncio import run

from loguru import logger
from pyrogram import Client, idle


async def main():
    bot_client = Client("bot")
    await bot_client.start()
    import ChannelBan.bot
    setattr(ChannelBan.bot, "bot_client", bot_client)
    bot_info = await bot_client.get_me()
    logger.success(f"Bot instance \"{bot_info.username}\" started.")
    await idle()
    logger.debug(f"Stopping bot instance \"{bot_info.username}\" ...")
    await bot_client.stop()
    logger.info(f"Bot instance \"{bot_info.username}\" stopped.")


if __name__ == '__main__':
    run(main())
