import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8730516887:AAFUyE1lgYN8bA9KhjxOJDpTk2e0QXe6RXA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က Group Management Bot ဖြစ်ပါတယ်။")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "📜 Group Rules\n\n"
        "1. No spam or links allowed.\n"
        "2. Respect all members.\n"
        "3. Violators will be banned."
    )
    await update.message.reply_text(rules_text)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            await update.message.reply_text(f"Welcome {member.full_name} to the group!")

async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat
    user_status = (await context.bot.get_chat_member(chat.id, user.id)).status
    
    if user_status in ["creator", "administrator"]:
        return

    try:
        await update.message.delete()
        await context.bot.send_message(
            chat_id=chat.id,
            text=f"⚠️ {user.full_name}, links are not allowed here!"
        )
    except Exception as e:
        print(f"Error: {e}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat

    user_status = (await context.bot.get_chat_member(chat.id, user.id)).status
    if user_status not in ["creator", "administrator"]:
        await update.message.reply_text("Only admins can use this command.")
        return

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(f"🚫 {target_user.full_name} has been banned.")
    else:
        await update.message.reply_text("Please reply to a user message with /ban")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.Entity("url") | filters.Entity("text_link"), handle_links))

    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()

