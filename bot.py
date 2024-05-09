from datetime import datetime
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from gsheet import Sheet
from const import TOKEN, ids, gsheet_name

BOT_TOKEN: Final = TOKEN
sheet = Sheet(gsheet_name)
sheet_df = sheet.df
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
        text = NO_ACCESS
    else:
        today = datetime.today().strftime("%d %b").lstrip("0").replace(" 0", " ")
        tasks = [
            f"Lesson <u>{index}</u> for the <u>{column}</u> time"
            for index, row in sheet.df.iterrows()
            for column in sheet.df.columns
            if row[column] == today
        ]
        text = "\n".join(tasks) if tasks else "You have no other tasks for today!"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
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
