import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Тексты
TEXTS = {
    "ru": {
        "main_menu": "Главное меню",
        "accommodation": "Размещение",
        "menu": "Меню",
        "contacts": "Контакты",
        "cottages": "Коттеджи",
        "standard": "Стандартные номера",
        "topchan": "Топчаны",
        "back": "Назад"
    },
    "uz": {
        "main_menu": "Asosiy menyu",
        "accommodation": "Yotoq joylar",
        "menu": "Taomlar menyusi",
        "contacts": "Kontaktlar",
        "cottages": "Kottejlar",
        "standard": "Oddiy xonalar",
        "topchan": "Topchanlar",
        "back": "Orqaga"
    }
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz")]
    ]
    await update.message.reply_text("Выберите язык / Tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

# Выбор языка
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    await location_menu_handler(update, context)

# Выбор размещения
async def location_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "ru")
    txt = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(txt["cottages"], callback_data="cottages")],
        [InlineKeyboardButton(txt["standard"], callback_data="standard")],
        [InlineKeyboardButton(txt["topchan"], callback_data="topchan")],
        [InlineKeyboardButton(txt["back"], callback_data=f"lang_{lang}")]
    ]
    await query.edit_message_text("🏡 " + txt["accommodation"], reply_markup=InlineKeyboardMarkup(keyboard))

# Главное меню
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = context.user_data.get("lang", "ru")
    txt = TEXTS[lang]

    if query.data == "accommodation":
        await location_menu_handler(update, context)
    elif query.data == "menu":
        await query.edit_message_text("📷 Фото меню будет добавлено позже.")
    elif query.data == "contacts":
        await query.edit_message_text("📞 +998 XX XXX-XX-XX\n📍 Ташкентское море, зона отдыха «Бриз»")
    elif query.data in ["cottages", "standard", "topchan"]:
        await query.edit_message_text("📷 Здесь будет информация и фото.")
    elif query.data.startswith("lang_"):
        await language_handler(update, context)

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(location_menu_handler, pattern="^(cottages|standard|topchan|lang_)$"))
    application.add_handler(CallbackQueryHandler(menu_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
