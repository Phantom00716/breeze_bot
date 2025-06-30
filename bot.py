import os
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters

# Load configuration from .env file (bot token, admin ID, etc.)
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

# Enable logging for debugging (prints to console on server)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Text content for both languages: Russian (ru) and Uzbek (uz)
TEXTS = {
    'ru': {
        'main_menu': "Главное меню",
        'accommodation': "Размещение",
        'menu': "Меню",
        'contacts': "Контакты",
        'cottages': "Коттеджи",
        'standard': "Стандартные номера",
        'topchan': "Топчаны",
        '2p': "2-х местные",
        '4p': "4-х местные",
        '5p': "5-ти местные",
        'back': "Назад",
        'contact_info': "Контакты: +998 99 444 99 59",
        'menu_info': "Наше меню включает плов, шашлык, лагман и другие блюда.",  # placeholder menu description
        'desc_cottage_2': "Двухместный коттедж: уютный домик на 2 гостя.",
        'desc_cottage_4': "Четырехместный коттедж: комфортное размещение до 4 гостей.",
        'desc_cottage_5': "Пятиместный коттедж: просторное жилье для 5 гостей.",
        'desc_standard_2': "Стандартный номер на 2 человека с базовыми удобствами.",
        'desc_standard_4': "Стандартный номер на 4 человека с балконом.",
        'desc_standard_5': "Стандартный номер на 5 человек с дополнительным спальным местом.",
        'desc_topchan': "Топчан: традиционное место для отдыха на свежем воздухе.",
        'admin_panel': "Админ-панель",
        'admin_stats': "Статистика использования"
    },
    'uz': {
        'main_menu': "Bosh menyu",
        'accommodation': "Joylashtirish",
        'menu': "Menyu",
        'contacts': "Kontaktlar",
        'cottages': "Kottejlar",
        'standard': "Standart xonalar",
        'topchan': "Topchanlar",
        '2p': "2 kishilik",
        '4p': "4 kishilik",
        '5p': "5 kishilik",
        'back': "Ortga",
        'contact_info': "Kontakt: +998 99 444 99 59",
        'menu_info': "Bizning menyuda palov, shashlik, lag'mon va boshqa taomlar bor.",
        'desc_cottage_2': "2 kishilik kottej: 2 mehmon uchun qulay uy.",
        'desc_cottage_4': "4 kishilik kottej: 4 mehmon uchun shinam uy.",
        'desc_cottage_5': "5 kishilik kottej: 5 mehmon uchun keng uy.",
        'desc_standard_2': "2 kishilik standart xona, barcha qulayliklar bilan.",
        'desc_standard_4': "4 kishilik standart xona, balkoni bilan.",
        'desc_standard_5': "5 kishilik standart xona, qo'shimcha yotoqli.",
        'desc_topchan': "Topchan: ochiq havoda dam olish uchun an'anaviy joy.",
        'admin_panel': "Admin paneli",
        'admin_stats': "Foydalanish statistikasi"
    }
}

# Placeholder image URLs for each category (replace with actual image links or file IDs)
IMAGES = {
    'cottage_2': "https://via.placeholder.com/800x600.png?text=2+Person+Cottage",
    'cottage_4': "https://via.placeholder.com/800x600.png?text=4+Person+Cottage",
    'cottage_5': "https://via.placeholder.com/800x600.png?text=5+Person+Cottage",
    'standard_2': "https://via.placeholder.com/800x600.png?text=2+Person+Room",
    'standard_4': "https://via.placeholder.com/800x600.png?text=4+Person+Room",
    'standard_5': "https://via.placeholder.com/800x600.png?text=5+Person+Room",
    'topchan':    "https://via.placeholder.com/800x600.png?text=Topchan",
    'menu':       "https://via.placeholder.com/800x600.png?text=Food+Menu"
}

# Initialize usage counters (for admin statistics)
USAGE_STATS = {
    'cottage_2': 0, 'cottage_4': 0, 'cottage_5': 0,
    'standard_2': 0, 'standard_4': 0, 'standard_5': 0,
    'topchan': 0, 'menu': 0, 'contacts': 0
}

# Helper function: build main menu keyboard based on language and admin status
def get_main_menu_keyboard(lang: str, is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(TEXTS[lang]['accommodation'], callback_data='main_acc')],
        [InlineKeyboardButton(TEXTS[lang]['menu'], callback_data='main_food')],
        [InlineKeyboardButton(TEXTS[lang]['contacts'], callback_data='main_contacts')]
    ]
    if is_admin:  # add Admin Panel button for admin user
        buttons.append([InlineKeyboardButton(TEXTS[lang]['admin_panel'], callback_data='admin_panel')])
    return InlineKeyboardMarkup(buttons)

# Helper: build accommodation submenu keyboard (cottages, standard, topchan)
def get_accommodation_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(TEXTS[lang]['cottages'], callback_data='acc_cottages')],
        [InlineKeyboardButton(TEXTS[lang]['standard'], callback_data='acc_standard')],
        [InlineKeyboardButton(TEXTS[lang]['topchan'], callback_data='acc_topchan')],
        [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(buttons)

# Helper: build cottages sub-category keyboard (2, 4, 5 person cottages)
def get_cottages_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(TEXTS[lang]['2p'], callback_data='cottages_2')],
        [InlineKeyboardButton(TEXTS[lang]['4p'], callback_data='cottages_4')],
        [InlineKeyboardButton(TEXTS[lang]['5p'], callback_data='cottages_5')],
        [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_acc')]
    ]
    return InlineKeyboardMarkup(buttons)

# Helper: build standard rooms sub-category keyboard (2, 4, 5 person rooms)
def get_standard_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(TEXTS[lang]['2p'], callback_data='standard_2')],
        [InlineKeyboardButton(TEXTS[lang]['4p'], callback_data='standard_4')],
        [InlineKeyboardButton(TEXTS[lang]['5p'], callback_data='standard_5')],
        [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_acc')]
    ]
    return InlineKeyboardMarkup(buttons)

# /start command handler – prompts for language selection (private chat only)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Only respond in private chats to avoid group usage4
    if update.effective_chat.type != "private":
        await update.message.reply_text("I only work in private chats. Please message me one-on-one.")
        return
    # Send language selection message with inline buttons
    prompt = "Выберите язык / Tilni tanlang:"  # Show prompt in both languages
    keyboard = [[InlineKeyboardButton("Русский", callback_data="lang_ru"),
                 InlineKeyboardButton("O‘zbekcha", callback_data="lang_uz")]]
    await update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(keyboard))

# /admin command handler – shows stats (only for the admin user)
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if ADMIN_ID is None or user_id != ADMIN_ID:
        return  # ignore if not admin
    # Build usage statistics report
    stats = USAGE_STATS
    lines = [
        f"📊 {TEXTS['ru']['admin_stats']}:",
        f"Коттедж 2х: {stats['cottage_2']}",
        f"Коттедж 4х: {stats['cottage_4']}",
        f"Коттедж 5: {stats['cottage_5']}",
        f"Стандарт 2х: {stats['standard_2']}",
        f"Стандарт 4х: {stats['standard_4']}",
        f"Стандарт 5: {stats['standard_5']}",
        f"Топчаны: {stats['topchan']}",
        f"Меню (питание): {stats['menu']}",
        f"Контакты: {stats['contacts']}"
    ]
    await update.message.reply_text("\n".join(lines))

# CallbackQuery handler – handles all button presses from inline keyboards
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # acknowledge the callback (prevents loading animation)
    data = query.data
    user_id = query.from_user.id

    # If language selection was pressed
    if data == "lang_ru" or data == "lang_uz":
        # Save chosen language in user_data
        lang = 'ru' if data == "lang_ru" else 'uz'
        context.user_data['lang'] = lang
        # After language selection, display the main menu5
        await query.edit_message_text(
            text=TEXTS[lang]['main_menu'] + ":",
            reply_markup=get_main_menu_keyboard(lang, is_admin=(ADMIN_ID == user_id))
        )
        return

    # For all other callbacks, determine current language (default to Russian if not set)
    lang = context.user_data.get('lang', 'ru')

    # Main menu callbacks
    if data == "main_acc":
        # Show accommodation submenu (cottages, standard rooms, topchans)
        await query.edit_message_text(
            text=TEXTS[lang]['accommodation'] + ":",
            reply_markup=get_accommodation_keyboard(lang)
        )
    elif data == "main_food":
        # Show food menu: send menu photo and description
        USAGE_STATS['menu'] += 1  # increment menu view count
        # Remove main menu message to avoid duplicate keyboards
        await query.edit_message_text(text=TEXTS[lang]['menu_info'])
        # Send menu photo with caption and a Back button (to main menu)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=IMAGES['menu'],
            caption=TEXTS[lang]['menu_info'],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_main')]
            ])
        )
    elif data == "main_contacts":
        # Show contacts info (phone number)
        USAGE_STATS['contacts'] += 1
        await query.edit_message_text(text=TEXTS[lang]['contact_info'])
        # Send a separate message with a Back button to return to main menu
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=TEXTS[lang]['main_menu'] + ":",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_main')]
            ])
        )
    # Accommodation submenu callbacks
    elif data == "acc_cottages":
        # User chose "Cottages" – show cottage size options (2p, 4p, 5p)
        await query.edit_message_text(
            text=TEXTS[lang]['cottages'] + ":",
            reply_markup=get_cottages_keyboard(lang)
        )
    elif data == "acc_standard":
        # User chose "Standard Rooms" – show room size options
        await query.edit_message_text(
            text=TEXTS[lang]['standard'] + ":",
            reply_markup=get_standard_keyboard(lang)
        )
    elif data == "acc_topchan":
        # User chose "Topchans" – this is a final category with no subtypes
        USAGE_STATS['topchan'] += 1
        await query.edit_message_text(text=TEXTS[lang]['desc_topchan'])
        # Send topchan photo and description, with Back buttons (to accommodation menu and main menu)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=IMAGES['topchan'],
            caption=TEXTS[lang]['desc_topchan'],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_acc'),
                 InlineKeyboardButton(TEXTS[lang]['main_menu'], callback_data='back_main')]
            ])
        )
    # Final category selections (Cottages and Standard Rooms sub-categories)
    elif data.startswith("cottages_"):
        # User selected a specific cottage type (2p, 4p, or 5p)
        USAGE_STATS[data] += 1
        desc_key = 'desc_cottage_' + data.split("_")[1]  # e.g., "desc_cottage_2"
        description = TEXTS[lang].get(desc_key, "")
        # Remove the list message and send the cottage photo with description
        await query.edit_message_text(text=description)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=IMAGES.get(data),
            caption=description,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_cottages'),
                 InlineKeyboardButton(TEXTS[lang]['main_menu'], callback_data='back_main')]
            ])
        )
    elif data.startswith("standard_"):
        # User selected a specific standard room type (2p, 4p, or 5p)
        USAGE_STATS[data] += 1
        desc_key = 'desc_standard_' + data.split("_")[1]
        description = TEXTS[lang].get(desc_key, "")
        await query.edit_message_text(text=description)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=IMAGES.get(data),
            caption=description,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_standard'),
                 InlineKeyboardButton(TEXTS[lang]['main_menu'], callback_data='back_main')]
            ])
        )
    # Navigation "Back" buttons
    elif data == "back_main":
        # Go back to main menu (from any submenu or admin panel)
        await query.edit_message_text(
            text=TEXTS[lang]['main_menu'] + ":",
            reply_markup=get_main_menu_keyboard(lang, is_admin=(ADMIN_ID == user_id))
        )
    elif data == "back_acc":
        # Go back to accommodation main menu (from cottages/standard submenu)
        await query.edit_message_text(
            text=TEXTS[lang]['accommodation'] + ":",
            reply_markup=get_accommodation_keyboard(lang)
        )
    elif data == "back_cottages":
        # Go back to cottages list from a cottage detail
        await query.message.delete()  # remove the photo message
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=TEXTS[lang]['cottages'] + ":",
            reply_markup=get_cottages_keyboard(lang)
        )
    elif data == "back_standard":
        # Go back to standard rooms list from a room detail
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=TEXTS[lang]['standard'] + ":",
            reply_markup=get_standard_keyboard(lang)
        )
    elif data == "admin_panel":
        # Admin panel button pressed (only visible to admin)
        if ADMIN_ID is None or user_id != ADMIN_ID:
            return  # unauthorized, ignore
        stats = USAGE_STATS
        # Build admin stats message (in chosen language or default)
        stats_text = (
            f"{TEXTS[lang]['admin_stats']}:\n"
            f"Cottages 2p: {stats['cottage_2']}\n"
            f"Cottages 4p: {stats['cottage_4']}\n"
            f"Cottages 5p: {stats['cottage_5']}\n"
            f"Standard 2p: {stats['standard_2']}\n"
            f"Standard 4p: {stats['standard_4']}\n"
            f"Standard 5p: {stats['standard_5']}\n"
            f"Topchans: {stats['topchan']}\n"
            f"Menu views: {stats['menu']}\n"
            f"Contacts views: {stats['contacts']}"
        )
        # Edit the current message to show stats and a back button to main menu
        await query.edit_message_text(
            text=stats_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(TEXTS[lang]['back'], callback_data='back_main')]
            ])
        )

# Main function to set up the bot and start polling
async def main():
    # Create application and add handlers6
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("admin", admin_command, filters=filters.ChatType.PRIVATE))
    application.add_handler(CallbackQueryHandler(handle_callback))
    # Run the bot until manually stopped
    await application.run_polling()

# Entry point for running the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
