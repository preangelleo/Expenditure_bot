from Bot_messages import *


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    if message.from_user.id != TG_BOT_OWNER_ID: return await message.answer(NOT_OWNER_ALERT)
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n\n{WELCOME_FROM_TELEGRAM_BOT}")


@dp.message()
async def echo_handler(message: types.Message) -> None:

    if message.chat.id != TG_BOT_OWNER_ID: return
    
    try: await handel_telegram_message(message)
    except Exception as e: await message.answer(f"Failed...\n\n{e}")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # # INFO:aiogram.dispatcher:Run polling for bot @leowang_bot id=6134874649 - 'Leowang.net'
    set_commands()
    
    asyncio.run(main())