
import telebot
from telebot import types
from toke import TOKEN

bot = telebot.TeleBot(TOKEN)

def ler_tarefa(dias, msg):
    with open('Tarefas.txt', 'r') as taf:
        to = taf.readlines()
    for x in to:
        if dias in x:
            bot.send_message(msg, f"{x}")

def add(text, msg, message):
    try:
        with open('Tarefas.txt', 'a') as taf:
            taf.write(f"\n{text}")
        bot.reply_to(message, "Deu certo!")
    except:
        bot.send_message(msg, 'Aconteceu algo tente novamente')


def remover(data, msg, message):
    try:
        with open('Tarefas.txt', 'r') as ln:
            lines = ln.readlines()

            with open('Tarefas.txt', 'w') as lns:
                for line in lines:
                    if line.find(data) == -1:
                        lns.write(line)
        bot.reply_to(message, f"Removido as atividades do dia {data}")
    except:
        bot.send_message(msg, "Algo deu errado")

@bot.message_handler(commands=["hoje"])
def command_hoje(message):
    msg = message.chat.id
    bot.send_message(msg, "Cama")
    dia = message.text
    div = dia.split()
    dias = div[1]
    ler_tarefa(dias, msg)

@bot.message_handler(commands=["add"])
def command_add(message):
    msg = message.chat.id
    msgs = message.text
    div = msgs.split(',')
    text = div[1]
    add(text, msg, message)

@bot.message_handler(commands=["remove"])
def command_remove(message):
    msg = message.chat.id
    mgs = message.text
    div = mgs.split()
    data = div[1]
    remover(data, msg, message)


@bot.message_handler(commands=["help"])
def command_help(message):
    msg = message.chat.id
    bot.send_message(msg, "/remove \n/add \n/hoje")

bot.infinity_polling()
