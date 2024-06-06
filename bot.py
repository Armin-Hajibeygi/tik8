import logging
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from core import get_today_tasks, get_all_lessons
from const import TOKEN, ids
from messages import NO_ACCESS, START_MESSAGE

BOT_TOKEN: Final = TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def check_access(update: Update) -> bool:
    user_id = update.effective_user.id
    return user_id in ids


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = NO_ACCESS if not check_access(update) else START_MESSAGE
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
        worksheet_name = " ".join(context.args)
        response = get_today_tasks(update.effective_user.id, worksheet_name)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_to_message_id=update.effective_message.id,
        parse_mode="HTML",
    )


async def all_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update):
        response = NO_ACCESS
    else:
        response = get_all_lessons(update.effective_user.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_to_message_id=update.effective_message.id,
        parse_mode="HTML",
    )


async def sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = f"Dear {update.effective_user.first_name} \n"
    user_id = update.effective_user.id

    if user_id in ids:
        response += "You already have and account"
    else:
        response += f"Your code: <b><u>{user_id}</u></b> \n"
        response += f"Please give this code to the admin to finalize your sign up ^^"

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
    bot.add_handler(CommandHandler("lessons", all_lessons))
    bot.add_handler(CommandHandler("signup", sign_up))

    # start bot
    bot.run_polling()
