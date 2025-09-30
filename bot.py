import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ваш реальный URL игры
WEB_APP_URL = "https://rob-209.github.io/tetris-bot/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в Тетрис", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎮 Добро пожаловать в Тетрис!\n\n"
        "Нажмите кнопку ниже чтобы начать играть прямо в Telegram!",
        reply_markup=reply_markup
    )

async def handle_web_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.web_app_data:
        score = update.message.web_app_data.data
        await update.message.reply_text(f"🎉 Ваш рекорд: {score} очков!")

def main():
    # Токен из переменных окружения
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не найден! Проверьте Environment Variables в Render")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app))
    
    # Запускаем бота (используем polling для Render)
    print("✅ Бот запущен на Render!")
    print("📱 Откройте Telegram и найдите своего бота")
    print("🚀 Отправьте /start для начала")
    
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
