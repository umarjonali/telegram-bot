from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Словарь для хранения данных пользователей
user_data = {}

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💕Бале", callback_data='bale')],
        [InlineKeyboardButton("😎Саволнома нашр мекунам", callback_data='publish')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Салом ба шумо! Саволнома маҳқул шуд?", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == 'bale':
        user_data[user_id] = {}  # Создание хранилища данных для пользователя
        await ask_question(query, context, "🔶Ном :")
    elif query.data == 'publish':
        await query.edit_message_text("Саволномаи худро фиристед!")

# Вопросы в нужной последовательности
questions = [
    "🔶Ном :",
    "🔶Сину сол :",
    "🔶Баландии қад:",
    "🔶Вазн :",
    "🔶Миллат :",
    "🔶Давлат/Шаҳ-д:",
    "🔶Шаҳр/ноҳия :",
    "🔶Ҳамсар :",
    "🔶Фарзанд :",
    "🔶Машғулият :",
    "🔶Маълумот :",
    "📄Каме дар бораи худ :",
    "🧕🏻🧔🏻Ҳамсар чи гуна бошад?",
    "📞Тelegram :",
    "📞WhatsApp :"
]

# Задаем следующий вопрос
async def ask_question(query, context, question):
    await query.edit_message_text(question)
    context.user_data['current_question'] = question

# Обработка ответов пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    answer = update.message.text

    if user_id not in user_data:
        await update.message.reply_text("Лутфан аввал бо фармони /start оғоз кунед.")
        return

    current_question = context.user_data.get('current_question')
    if current_question:
        user_data[user_id][current_question] = answer  # Сохраняем ответ

        # Определяем следующий вопрос
        current_index = questions.index(current_question)
        if current_index + 1 < len(questions):
            next_question = questions[current_index + 1]
            await update.message.reply_text(next_question)
            context.user_data['current_question'] = next_question
        else:
            # Когда все ответы получены — выводим их в одном сообщении
            summary = "📋 **Саволнома пурра шуд:**\n\n"
            for q in questions:
                summary += f"{q} {user_data[user_id].get(q, '❌')}\n"
            await update.message.reply_text(summary, parse_mode='Markdown')
            del user_data[user_id]  # Очищаем данные пользователя

# Основная функция
def main():
    app = ApplicationBuilder().token('6009441598:AAGqq5NI2uiMpmdJRQmmFrNu0YosHfSGnKw').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен и готов к работе.")
    app.run_polling()

if __name__ == '__main__':
    main()