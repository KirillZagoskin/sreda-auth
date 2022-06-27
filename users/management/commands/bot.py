from typing import Any

from django.core.management.base import BaseCommand

from users.services.telegram.main import launch_telegram_bot

class Command(BaseCommand):
    '''Команда для запуска телеграм бота'''
    help = 'Command for the telegram bot launch'

    def handle(self, *args: Any, **options: Any):
        '''Обработчик команды, который запускает бота'''
        launch_telegram_bot()