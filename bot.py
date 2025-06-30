import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в зону отдыха Бриз! 🌊\n\n"
        "/info - Информация\n"
        "/cottages - Свободные коттеджи\n"
        "/contact - Контакты"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌴 Зона отдыха 'Бриз' на берегу Ташкентского моря:\n"
        "- 12 коттеджей\n"
        "- 12 номеров\n"
        "- 3-разовое питание\n"
        "- Топчаны у воды"
    )

async def cottages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Доступность коттеджей временно не отображается.")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Контакты:\n+998 90 123 45 67\n@breeze_admin\n📍 Ташкентское море"
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("cottages", cottages))
    app.add_handler(CommandHandler("contact", contact))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
