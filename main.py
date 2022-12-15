import init_django_orm  # noqa: F401
import os
from datetime import datetime
from dotenv import load_dotenv

import csv

import telebot

from app.models import StartDate, Owner, Username


load_dotenv()

bot = telebot.TeleBot(os.environ.get("TOKEN"))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send in this chat .csv file with: date, name, username.")


@bot.message_handler(content_types=['document'])
def echo_all(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(file_name, "r") as file:
        csvreader = csv.reader(file)

        StartDate.objects.all().delete()
        Owner.objects.all().delete()
        Username.objects.all().delete()

        for i, row in enumerate(csvreader):
            if i != 0:
                info = row[0].split(";")
                StartDate.objects.create(date=datetime.strptime(info[0], "%d.%m.%Y").date())
                Owner.objects.create(name=info[1])
                Username.objects.create(username=info[2])

        bot.reply_to(message, "Done!")


bot.infinity_polling()
