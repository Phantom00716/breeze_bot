import os from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes)

TOKEN = os.getenv("TELEGRAM_TOKEN")

Языковые тексты

LANG = { 'ru': { 'start': "Пожалуйста, выберите язык:", 'menu': "Главное меню:", 'rooms': "Выберите тип размещения:", 'cottages': "Выберите тип коттеджа:", 'standard_rooms': "Выберите тип стандартного номера:", 'topchans': "Топчаны: у воды, в тени, с навесом.", 'menu_info': "🍽 Меню кухни: Завтрак, обед, ужин. Натуральные продукты.", 'contacts': "📞 Контакты:\nТел: +998 99 444 99 59\nTelegram: @breeze_admin\nОплата: Click, Payme, наличными" }, 'uz': { 'start': "Iltimos, tilni tanlang:", 'menu': "Asosiy menyu:", 'rooms': "Joylashtirish turini tanlang:", 'cottages': "Kottej turini tanlang:", 'standard_rooms': "Standart xona turini tanlang:", 'topchans': "Topchanlar: suv bo‘yida, soyada, naves bilan.", 'menu_info': "🍽 Oshxona menyusi: Nonushta, tushlik, kechki ovqat. Tabiiy mahsulotlar.", 'contacts': "📞 Kontaktlar:\nTel: +998 99 444 99 59\nTelegram: @breeze_admin\nTo‘lov: Click, Payme, naqd" } }

user_language = {}

Генерация главного меню

def main_menu(lang): return InlineKeyboardMarkup([ [InlineKeyboardButton("🏠 Размещение" if lang == 'ru' else "🏠 Joylashtirish", callback_data='rooms')], [InlineKeyboardButton("🍽 Меню кухни" if lang == 'ru' else "🍽 Oshxona menyusi", callback_data='menu')], [InlineKeyboardButton("💵 Контакты/Оплата" if lang == 'ru' else "💵 Kontaktlar / To‘lov", callback_data='contacts')] ])

Команда /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [[ InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'), InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data='lang_uz') ]] await update.message.reply_text("Пожалуйста, выберите язык / Iltimos, tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

Обработка callback'ов

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()

user_id = query.from_user.id
data = query.data

if data.startswith('lang_'):
    lang = data.split('_')[1]
    user_language[user_id] = lang
    await query.edit_message_text(text=LANG[lang]['menu'], reply_markup=main_menu(lang))

elif data == 'rooms':
    lang = user_language.get(user_id, 'ru')
    keyboard = [[
        InlineKeyboardButton("🏡 Коттеджи" if lang == 'ru' else "🏡 Kottejlar", callback_data='cottages')],
        [InlineKeyboardButton("🚪 Стандартные номера" if lang == 'ru' else "🚪 Standart xonalar", callback_data='standard_rooms')],
        [InlineKeyboardButton("🛏 Топчаны" if lang == 'ru' else "🛏 Topchanlar", callback_data='topchans')]
    ]
    await query.edit_message_text(LANG[lang]['rooms'], reply_markup=InlineKeyboardMarkup(keyboard))

elif data in ['cottages', 'standard_rooms']:
    lang = user_language.get(user_id, 'ru')
    prefix = "Коттеджи" if data == 'cottages' else "Стандартные номера"
    uz_prefix = "Kottejlar" if data == 'cottages' else "Standart xonalar"
    keyboard = [[
        InlineKeyboardButton("2-местные" if lang == 'ru' else "2 o‘rinli", callback_data=f'{data}_2')],
        [InlineKeyboardButton("4-местные" if lang == 'ru' else "4 o‘rinli", callback_data=f'{data}_4')],
        [InlineKeyboardButton("5-местные" if lang == 'ru' else "5 o‘rinli", callback_data=f'{data}_5')]
    ]
    await query.edit_message_text((prefix if lang == 'ru' else uz_prefix), reply_markup=InlineKeyboardMarkup(keyboard))

elif data == 'topchans':
    lang = user_language.get(user_id, 'ru')
    await query.edit_message_text(LANG[lang]['topchans'])

elif data == 'menu':
    lang = user_language.get(user_id, 'ru')
    await query.edit_message_text(LANG[lang]['menu_info'])

elif data == 'contacts':
    lang = user_language.get(user_id, 'ru')
    await query.edit_message_text(LANG[lang]['contacts'])

async def main(): app = ApplicationBuilder().token(TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CallbackQueryHandler(callback_handler)) await app.run_polling()

if name == 'main': import asyncio asyncio.run(main())

