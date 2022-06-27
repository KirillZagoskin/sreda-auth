from users.services.telegram.app import bot

def launch_telegram_bot():
    '''Запуск телеграм бота'''
    bot.updater.start_polling()
    bot.updater.idle()