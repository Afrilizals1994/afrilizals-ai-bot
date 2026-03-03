import os
import telebot
from g4f.client import Client

# Initialize bot and G4F client
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = 8467632181

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

bot = telebot.TeleBot(TOKEN)
client = Client()

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """Handle /start and /help commands"""
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "❌ Akses ditolak. Bot ini hanya untuk pengguna tertentu.")
        return
    
    help_text = """
🤖 **Afrilizals AI Bot** - Powered by G4F
    
Perintah yang tersedia:
/start - Tampilkan menu ini
/help - Bantuan
/ask - Tanya pertanyaan ke AI
    
Cukup kirim pertanyaan Anda dan bot akan menjawab! 💬
    """
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['ask'])
def handle_ask(message):
    """Handle /ask command"""
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "❌ Akses ditolak.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "❌ Gunakan: /ask [pertanyaan Anda]")
        return
    
    question = args[1]
    process_question(message, question)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all other text messages"""
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "❌ Akses ditolak.")
        return
    
    process_question(message, message.text)

def process_question(message, question):
    """Process question and get response from G4F"""
    try:
        typing_message = bot.send_message(message.chat.id, "🤔 Sedang berpikir...")
        
        # Get response from G4F
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
        )
        
        answer = response.choices[0].message.content
        
        # Delete typing message
        bot.delete_message(message.chat.id, typing_message.message_id)
        
        # Send answer
        if len(answer) > 4096:
            # Split long messages
            for i in range(0, len(answer), 4096):
                bot.send_message(message.chat.id, answer[i:i+4096])
        else:
            bot.send_message(message.chat.id, answer)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")
        print(f"Error: {str(e)}")

def main():
    """Start the bot"""
    print("🚀 Bot sedang berjalan...")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n⛔ Bot dihentikan.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()