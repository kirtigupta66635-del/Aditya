import asyncio
import importlib
import threading
from flask import Flask

import config
from config import OWNER_ID

from pyrogram import idle
from pyrogram.types import BotCommand

from RISHUCHATBOT import (
    RISHUCHATBOT,
    userbot,
    LOGGER,
    load_clone_owners,
)
from RISHUCHATBOT.modules import ALL_MODULES
from RISHUCHATBOT.modules.Clone import restart_bots
from RISHUCHATBOT.modules.Id_Clone import restart_idchatbots


# -------------------- BOT STARTUP --------------------

async def start_bot():
    try:
        await RISHUCHATBOT.start()
        LOGGER.info("Main bot started")

        try:
            await RISHUCHATBOT.send_message(
                int(OWNER_ID),
                f"✅ **{RISHUCHATBOT.mention} successfully started**"
            )
        except Exception:
            LOGGER.warning("Owner has not started the bot yet")

        # Background tasks
        asyncio.create_task(restart_bots())
        asyncio.create_task(restart_idchatbots())
        await load_clone_owners()

        # Start userbot (ID chatbot)
        if config.STRING1:
            try:
                await userbot.start()
                LOGGER.info("ID Chatbot started")

                try:
                    await RISHUCHATBOT.send_message(
                        int(OWNER_ID),
                        "✅ **ID-Chatbot successfully started**"
                    )
                except Exception:
                    pass

            except Exception as ex:
                LOGGER.error(f"Failed to start ID chatbot: {ex}")

    except Exception as ex:
        LOGGER.critical(f"Bot startup failed: {ex}")
        return

    # -------------------- LOAD MODULES --------------------

    for module in ALL_MODULES:
        try:
            importlib.import_module(f"RISHUCHATBOT.modules.{module}")
            LOGGER.info(f"Loaded module: {module}")
        except Exception as ex:
            LOGGER.error(f"Failed to load module {module}: {ex}")

    # -------------------- BOT COMMANDS --------------------

    try:
        await RISHUCHATBOT.set_bot_commands(
            [
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Get help menu"),
                BotCommand("clone", "Create your own chatbot"),
                BotCommand("idclone", "Create ID chatbot"),
                BotCommand("cloned", "List of cloned bots"),
                BotCommand("ping", "Check bot status"),
                BotCommand("lang", "Set bot reply language"),
                BotCommand("chatlang", "Current chat language"),
                BotCommand("resetlang", "Reset language"),
                BotCommand("id", "Get user ID"),
                BotCommand("stats", "Bot statistics"),
                BotCommand("gcast", "Global broadcast"),
                BotCommand("chatbot", "Enable/Disable chatbot"),
                BotCommand("status", "Chatbot status"),
                BotCommand("shayri", "Random shayri"),
                BotCommand("ask", "Ask AI anything"),
            ]
        )
        LOGGER.info("Bot commands registered")
    except Exception as ex:
        LOGGER.error(f"Failed to set commands: {ex}")

    LOGGER.info(f"🤖 @{RISHUCHATBOT.username} is fully operational")
    await idle()


# -------------------- FLASK KEEP-ALIVE --------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running smoothly"


def run_flask():
    app.run(host="0.0.0.0", port=8000)


# -------------------- MAIN ENTRY --------------------

if __name__ == "__main__":
    LOGGER.info("Starting Flask keep-alive server")
    threading.Thread(target=run_flask, daemon=True).start()

    LOGGER.info("Starting Telegram bot")
    asyncio.run(start_bot())
