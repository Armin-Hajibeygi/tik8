from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from core import get_today_tasks
from const import TOKEN, ids

BOT_TOKEN: Final = TOKEN
NO_ACCESS = "You don't have access to this bot."


def check_access(update: Update) -> bool:
    user_id = update.effective_user.id
    return user_id in ids


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        NO_ACCESS
        if not check_access(update)
        else "Hello, I'm Tik8 bot! Thanks for using me!"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def today_task_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not check_access(update):
        response = NO_ACCESS
    else:
        response = get_today_tasks(update.effective_user.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_to_message_id=update.effective_message.id,
        parse_mode="HTML",
    )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(CommandHandler("today", today_task_command_handler))

    # start bot
    bot.run_polling()
