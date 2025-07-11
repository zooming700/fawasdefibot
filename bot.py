import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Bot configuration - using your provided token
BOT_TOKEN = '7704608222:AAFTSJ4iCOUuB3--H3-hYOe9EW1idssYmuE'
CHANNEL_USERNAME = "@yourchannel"  # Change to your channel username
GROUP_USERNAME = "@yourgroup"      # Change to your group username

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Welcome {user.first_name} to our Airdrop Bot!\n\n"
        "To participate in the airdrop, please complete these simple steps:"
    )
    
    keyboard = [
        [InlineKeyboardButton("Step 1: Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Step 2: Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("✅ I've Joined Both", callback_data='joined')]
    ]
    
    update.message.reply_text(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'joined':
        query.edit_message_text(
            text="Great! Now please send us your Twitter username (without @)."
        )
        context.user_data['step'] = 'twitter'

def handle_message(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    
    if 'step' not in user_data:
        update.message.reply_text("Please start with /start first.")
        return
    
    if user_data['step'] == 'twitter':
        # Store Twitter handle (no validation)
        user_data['twitter'] = update.message.text
        user_data['step'] = 'wallet'
        update.message.reply_text(
            "Almost done! Please send your SOL wallet address now."
        )
    elif user_data['step'] == 'wallet':
        # Store wallet address (no validation)
        user_data['wallet'] = update.message.text
        user_data['step'] = 'complete'
        
        # Congratulatory message
        update.message.reply_text(
            "🎉 Congratulations!\n\n"
            "You've successfully completed all steps!\n"
            "10 SOL is on its way to your wallet!\n\n"
            "Note: This is a simulated airdrop for demonstration purposes."
        )
        
        # Optional: Print the submission to console
        print(f"New submission from @{update.effective_user.username}:")
        print(f"Twitter: {user_data['twitter']}")
        print(f"Wallet: {user_data['wallet']}\n")
        
        # Clear user data
        user_data.clear()

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
