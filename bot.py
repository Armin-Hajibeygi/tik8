from typing import Final

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from const import TOKEN, ids

BOT_TOKEN: Final = TOKEN


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ids:
        text = "You don't have access to this bot."
    else:
        text = "Hello, I'm Tik8 bot! Thanks for using me!"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))

    # start bot
    bot.run_polling()