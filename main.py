from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest # Імпортуємо BadRequest для специфічної обробки помилок
import os

# Завантаження змінних оточення з .env файлу
load_dotenv()
TOKEN = os.getenv("TOKEN")

#-----------------------------------------------------------------------------------------------------------------------
# Список тем по математиці (29 тем)
mathematics_topics = [
    "Числа та дії з ними",
    "Раціональні числа",
    "Функції",
    "Лінійні рівняння та нерівності",
    "Квадратні рівняння",
    "Системи рівнянь",
    "Похідна та її застосування",
    "Елементи комбінаторики",
    "Тригонометрія",
    "Геометричні фігури",
    "Вектори",
    "Планіметрія",
    "Стереометрія",
    "Аналітична геометрія",
    "Прогресії",
    "Множини",
    "Статистика",
    "Теорія ймовірностей",
    "Логарифми",
    "Показникові функції",
    "Графіки функцій",
    "Похідна в деталях",
    "Інтеграли (базово)",
    "Рівняння з параметрами",
    "Симетрії та перетворення",
    "Рівняння кола, еліпса",
    "Неравенства з модулями",
    "Задачі на рух",
    "Комбінаторика в задачах",
]
#-----------------------------------------------------------------------------------------------------------------------
# Список тем з Української мови (додано для прикладу)
ukrainian_topics = [
    "Фонетика. Орфоепія. Графіка. Орфографія",
    "Лексикологія. Фразеологія",
    "Будова слова. Словотвір. Морфологія",
    "Синтаксис. Пунктуація",
    "Стилістика. Культура мовлення",
    "Текстологія",
    "Розвиток мовлення",
    "Засоби виразності мови"
]
#-----------------------------------------------------------------------------------------------------------------------
# Список тем з історії України (37 тем)
history_topics = [
    "Вступ до історії України",
    "Стародавня історія України",
    "Королівство Руське. Монгольська навала",
    "Руські князівства XIV–XVI ст. Кримське ханство",
    "Русь-Україна: виникнення Київської держави",
    "Русь-Україна: розквіт Київської держави",
    "Русь-Україна: культура IX–XIV століть",
    "Друга половина XVI – перша половина XVIII ст.",
    "Українські землі в Речі Посполитій (II пол. XVI ст.)",
    "Українські землі в Речі Посполитій (І пол. XVII ст.)",
    "Національно-визвольна війна середини XVII ст.",
    "Козацька держава (50–80-ті рр. XVII ст.)",
    "Українські землі к. XVII – І пол. XVIII ст.",
    "Українські землі в ІІ пол. XVIII ст.",
    "Кінець XVIII – XIX ст.",
    "Укр. землі в Рос. імперії (к. XVIII – І пол. XIX ст.)",
    "Укр. землі в Австр. імперії (к. XVIII – І пол. XIX ст.)",
    "Культура України (к. XVIII – І пол. XIX ст.)",
    "Укр. землі в Рос. імперії (ІІ пол. XIX ст.)",
    "Укр. землі в Австро-Угорщині (ІІ пол. XIX ст.)",
    "Культура України (ІІ пол. XIX – поч. XX ст.)",
    "Укр. землі в Рос. імперії (1900–1914 рр.)",
    "Укр. землі в Австро-Угорщині (1900–1914 рр.)",
    "Історія України ХХ – початку ХХІ ст.",
    "Україна в роки Першої світової війни",
    "Початок Української революції",
    "Гетьманат Павла Скоропадського",
    "Директорія УНР",
    "Комуністичний тоталітарний режим в Україні",
    "Більшовицький тоталітаризм в Україні",
    "Західна Україна в міжвоєнний період",
    "Початок Другої світової війни (1939–1941)",
    "Рух Опору (1941–1943)",
    "Визволення України (1943–1945)",
    "Повоєнні роки в Україні",
    "Десталінізація",
    "Криза радянської системи",
    "Незалежність України",
    "Становлення держави",
    "Нова Україна",
]
#-----------------------------------------------------------------------------------------------------------------------
ITEMS_PER_PAGE = 10
EMOJI_START = "📘 "
EMOJI_END = " ✨"

#-----------------------------------------------------------------------------------------------------------------------
# Функція для повернення в головне меню
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Завжди відповідаємо на callback_query, щоб прибрати "годинник" з кнопки
    keyboard = [
        [InlineKeyboardButton("📚 Список предметів", callback_data='main_keyboard')],
        [InlineKeyboardButton("📚 Корисні файли", callback_data='KorFail')],
        [InlineKeyboardButton("📝 Практичні завдання", callback_data='PrZavd')],
        [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_command')],
        [InlineKeyboardButton("🛠️ Допомога", callback_data='help_command')]
    ]

    try:
        await query.edit_message_text(
            text="Повернення в головне меню.\n\nОберіть дію:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        # Ігноруємо помилку, якщо повідомлення не змінилось.
        pass

#-----------------------------------------------------------------------------------------------------------------------
# Функція для команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Список предметів", callback_data='main_keyboard')],
        [InlineKeyboardButton("📚 Корисні файли", callback_data='KorFail')],
        [InlineKeyboardButton("📝 Практичні завдання", callback_data='PrZavd')],
        [InlineKeyboardButton("ℹ️ Про бота", callback_data='about_command')],
        [InlineKeyboardButton("🛠️ Допомога", callback_data='help_command')]
    ]
    await update.message.reply_text(
        "Привіт! 👋 Цей бот допоможе тобі підготуватись до НМТ. Обирай предмет, проходь тести, слідкуй за прогресом — і впевнено йди до 200+ балів! 🚀📚✨.\n\nОберіть дію:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
#-----------------------------------------------------------------------------------------------------------------------
# Функція для команди "Про бота"
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
    ]
    try:
        await query.edit_message_text(
            "Привіт! Я — бот для підготовки до НМТ 📚🚀\n\n"
            "Ось що я вмію:\n"
            "- Допомагаю готуватися з різних предметів (математика, українська мова, історія)\n"
            "- Надсилаю корисні матеріали у форматі PDF\n"
            "- Проводжу тести для закріплення знань\n\n"
            "Якщо маєш питання або пропозиції — звертайся до розробника!\n\n"
            "Щасливої підготовки та високих балів! 🎉",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для команди "Допомога"
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
    ]
    try:
        await query.edit_message_text(
            "🛠️ Допомога\n\n"
            "Цей бот допоможе тобі підготуватися до НМТ. Ось як ним користуватися:\n"
            "- Обирай предмети зі списку.\n"
            "- Переглядай теми та матеріали.\n"
            "- Відповідай на тестові питання (планується).\n"
            "- Використовуй кнопки навігації для переходу між сторінками.\n\n"
            "Якщо виникають проблеми або є ідеї, пиши розробнику.\n\n"
            "Успіхів у підготовці! 🚀",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для додаткових матеріалів з математики
async def DovMat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_path = os.path.join("KorysniFaili", "Математика_Матеріали.pdf")
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
    ]
    try:
        with open(file_path, "rb") as file:
            # Відправляємо файл новим повідомленням з кнопкою
            await query.message.reply_document(file, filename="Математика_Матеріали.pdf")
            # Відправляємо окреме повідомлення з кнопкою повернення в меню
            # Якщо попереднє повідомлення було відредаговано, то краще відправляти нове.
            # Якщо ж ви хочете видалити попереднє і відправити нове, це інший підхід.
            # Наразі, просто відправляємо нове повідомлення з кнопкою.
            await query.message.reply_text("Файл для підготовки:", reply_markup=InlineKeyboardMarkup(keyboard))
    except FileNotFoundError:
        await query.message.reply_text("⚠️ Файл не знайдено.")
    except Exception as e:
        print(f"Помилка при відправці файлу: {e}")
        await query.message.reply_text("Виникла помилка при обробці файлу.")
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення корисних файлів
async def KorFail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📚 Додаткові матеріали з математики", callback_data='DovMat')],
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("➡️До списку предметів➡️", callback_data='main_keyboard')]
    ]
    try:
        await query.edit_message_text(
            "Ось всі корисні файли для підготовки🚀",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення практичних завданнь
async def PrZavd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📐Практичні завдання з математики", callback_data='PrZavdMathematics')],
        [InlineKeyboardButton("📖Практичні завдання з Української мови", callback_data='PrZavdUkrMova')],
        [InlineKeyboardButton("🏰 Практичні завдання з Історії України", callback_data='PrZavdHistory')],
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')]
    ]
    try:
        await query.edit_message_text(
            text="Оберіть предмет",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення практичних завданнь з математики
async def PrZavdMathematics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='PrZavd')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення практичних завданнь з Української мови
async def PrZavdUkrMova(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='PrZavd')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення практичних завданнь з Історії України
async def PrZavdHistory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='PrZavd')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для відображення головної клавіатури з предметами
async def main_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📐 Математика", callback_data='Mathematics')],
        [InlineKeyboardButton("📖 Українська мова", callback_data='UkrMova')],
        [InlineKeyboardButton("🏰 Історія України", callback_data='History')],
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')]
    ]
    try:
        await query.edit_message_text(
            text="Оберіть предмет для підготовки:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для пагінації тем з математики
async def Mathematics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    # Отримуємо номер сторінки з callback_data
    # Якщо callback_data - 'Mathematics', то це перша сторінка
    if "_" in data and data.split("_")[1].isdigit():
        page = int(data.split("_")[1])
    else:
        page = 1
    total_pages = (len(mathematics_topics) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if total_pages == 0 and len(mathematics_topics) > 0: # Для випадку, коли тем менше ніж ITEMS_PER_PAGE
        total_pages = 1
    elif len(mathematics_topics) == 0: # Якщо список тем порожній
        total_pages = 0
    # Забезпечуємо, що номер сторінки знаходиться в допустимих межах
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    elif total_pages == 0: # Якщо немає тем, то немає і сторінок
        page = 0
    keyboard = [
        [InlineKeyboardButton("⬅️До списку предметів⬅️", callback_data='main_keyboard')],
    ]
    if total_pages > 0: # Лише якщо є теми, додаємо кнопки тем
        start_index = (page - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        topics_on_page = mathematics_topics[start_index:end_index]
        for i, topic in enumerate(topics_on_page, start=start_index + 1):
            button_text = f"{EMOJI_START} Тема {i}. {topic} {EMOJI_END}"
            # Уникайте колізій callback_data: `mathematics_topic_{i}`
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"mathematics_topic_{i}")])
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"Mathematics_{page - 1}"))

    nav_buttons.append(InlineKeyboardButton("🏠 В головне меню", callback_data="main_menu"))

    if total_pages > 0 and page < total_pages: # Кнопка "Вперед" тільки якщо це не остання сторінка
        nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"Mathematics_{page + 1}"))

    if nav_buttons: # Додаємо рядок навігаційних кнопок, якщо вони є
        keyboard.append(nav_buttons)
    text_message = ""
    if total_pages > 0:
        text_message = f"📚 Сторінка {page} з {total_pages}\n\nОберіть тему для перегляду:"
    else:
        text_message = "Наразі немає тем з математики."

    try:
        await query.edit_message_text(
            text=text_message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass # Ігноруємо помилку, якщо повідомлення не змінилось
#-----------------------------------------------------------------------------------------------------------------------
# Функція для пагінації тем з Української мови
async def UkrMova(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if "_" in data and data.split("_")[1].isdigit():
        page = int(data.split("_")[1])
    else:
        page = 1
    total_pages = (len(ukrainian_topics) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if total_pages == 0 and len(ukrainian_topics) > 0:
        total_pages = 1
    elif len(ukrainian_topics) == 0:
        total_pages = 0
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    elif total_pages == 0:
        page = 0
    keyboard = [
        [InlineKeyboardButton("⬅️До списку предметів⬅️", callback_data='main_keyboard')],
    ]
    if total_pages > 0:
        start_index = (page - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        topics_on_page = ukrainian_topics[start_index:end_index]

        for i, topic in enumerate(topics_on_page, start=start_index + 1):
            button_text = f"{EMOJI_START} Тема {i}. {topic} {EMOJI_END}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"ukrainian_topic_{i}")])
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"UkrMova_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton("🏠 В головне меню", callback_data="main_menu"))
    if total_pages > 0 and page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"UkrMova_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)
    text_message = ""
    if total_pages > 0:
        text_message = f"📚 Сторінка {page} з {total_pages}\n\nОберіть тему для перегляду:"
    else:
        text_message = "Наразі немає тем з української мови."
    try:
        await query.edit_message_text(
            text=text_message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass # Ігноруємо помилку, якщо повідомлення не змінилось
#-----------------------------------------------------------------------------------------------------------------------
# Функція для розділу "Історія України"
async def History(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        # При натисканні "Список тем" завжди переходимо на першу сторінку
        [InlineKeyboardButton("📚 Список тем", callback_data='show_history_topics_1')],
        [InlineKeyboardButton("🧑‍🏫 Персоналії", callback_data='history_personalities')], # Ці кнопки поки не обробляються
        [InlineKeyboardButton("🏛️ Архітектура", callback_data='history_architecture')], # Ці кнопки поки не обробляються
        [InlineKeyboardButton("🎨 Мистецтво", callback_data='history_art')], # Ці кнопки поки не обробляються
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️До списку предметів⬅️", callback_data='main_keyboard')]
    ]
    try:
        await query.edit_message_text(
            text="Оберіть розділ з історії України:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass # Ігноруємо помилку, якщо повідомлення не змінилось
#-----------------------------------------------------------------------------------------------------------------------
# Функція для "Персоналії історія"
async def history_personalities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='History')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для "Архітектура історія"
async def history_architecture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='History')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для "Мистецтво історія"
async def history_art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🏠 У головне меню", callback_data='main_menu')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='History')],
    ]
    try:
        await query.edit_message_text(
            text="У розробці🛠️",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass
#-----------------------------------------------------------------------------------------------------------------------
# Функція для пагінації тем з історії України
async def show_history_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    # Очікуємо формат 'show_history_topics_X', де X - номер сторінки
    if "_" in data and data.split("_")[-1].isdigit(): # Використовуємо split("_")[-1] для надійності
        page = int(data.split("_")[-1])
    else:
        page = 1 # Якщо це перший виклик або формат не відповідає, починаємо з 1 сторінки
    total_pages = (len(history_topics) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    if total_pages == 0 and len(history_topics) > 0: # Для випадку, коли тем менше ніж ITEMS_PER_PAGE
        total_pages = 1
    elif len(history_topics) == 0: # Якщо список тем порожній
        total_pages = 0
    # Забезпечуємо, що номер сторінки знаходиться в допустимих межах
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    elif total_pages == 0: # Якщо немає тем, то немає і сторінок
        page = 0
    keyboard = []
    if total_pages > 0: # Лише якщо є теми, додаємо кнопки тем
        start_index = (page - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        topics_on_page = history_topics[start_index:end_index]
        for i, topic in enumerate(topics_on_page, start=start_index + 1):
            button_text = f"{EMOJI_START} Тема {i}. {topic} {EMOJI_END}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"history_topic_{i}")])
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"show_history_topics_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton("🏠 В головне меню", callback_data="main_menu"))
    if total_pages > 0 and page < total_pages: # Кнопка "Вперед" тільки якщо це не остання сторінка
        nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"show_history_topics_{page + 1}"))
    if nav_buttons: # Додаємо рядок навігаційних кнопок, якщо вони є
        keyboard.append(nav_buttons)
    text_message = ""
    if total_pages > 0:
        text_message = f"📚 Сторінка {page} з {total_pages}\n\nОберіть тему для перегляду:"
    else:
        text_message = "Наразі немає тем з історії України."
    try:
        await query.edit_message_text(
            text=text_message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except BadRequest:
        pass # Ігноруємо помилку, якщо повідомлення не змінилось
#-----------------------------------------------------------------------------------------------------------------------
# Точка входу в програму
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    # Реєстрація обробників команд
    app.add_handler(CommandHandler("start", start))
    # Реєстрація обробників callback-запитів
    app.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))
    app.add_handler(CallbackQueryHandler(main_keyboard, pattern='^main_keyboard$'))
    app.add_handler(CallbackQueryHandler(PrZavd, pattern='^PrZavd$'))
    app.add_handler(CallbackQueryHandler(KorFail, pattern='^KorFail$'))
    app.add_handler(CallbackQueryHandler(DovMat, pattern='^DovMat$'))
    app.add_handler(CallbackQueryHandler(about_command, pattern='^about_command$'))
    app.add_handler(CallbackQueryHandler(help_command, pattern='^help_command$'))
    app.add_handler(CallbackQueryHandler(history_architecture, pattern='^history_architecture$'))
    app.add_handler(CallbackQueryHandler(history_art, pattern='^history_art$'))
    app.add_handler(CallbackQueryHandler(history_personalities, pattern='^history_personalities$'))
    app.add_handler(CallbackQueryHandler(PrZavdMathematics, pattern='^PrZavdMathematics$'))
    app.add_handler(CallbackQueryHandler(PrZavdUkrMova, pattern='^PrZavdUkrMova$'))
    app.add_handler(CallbackQueryHandler(PrZavdHistory, pattern='^PrZavdHistory$'))
    # Обробники для пагінації предметів
    # Використовуємо r'^SubjectName(_\d+)?$' для обробки 'SubjectName' (1 сторінка) і 'SubjectName_X' (X сторінка)
    app.add_handler(CallbackQueryHandler(Mathematics, pattern=r'^Mathematics(_\d+)?$'))
    app.add_handler(CallbackQueryHandler(UkrMova, pattern=r'^UkrMova(_\d+)?$')) # Додано обробник для УкрМови
    app.add_handler(CallbackQueryHandler(History, pattern=r'^History$')) # Цей обробник веде в меню історії
    app.add_handler(CallbackQueryHandler(show_history_topics, pattern=r'^show_history_topics(_\d+)?$')) # Обробник для пагінації тем історії
    print("Бот запущено...")
    app.run_polling()
#-----------------------------------------------------------------------------------------------------------------------