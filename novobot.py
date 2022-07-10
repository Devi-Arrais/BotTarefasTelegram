import sqlite3
import telebot
from telebot import types
from toke import TOKEN

bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('Tarefas.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS atividades(data NOT NULL, tarefas NOT NULL);")

def ler_tarefa(dias, msg):
    n = 0
    tas = cur.execute(f"SELECT tarefas FROM atividades WHERE data='{dias} ';")
    todo = tas.fetchall()
    for n in range(len(todo)):
        divi = todo[n][0]
        bot.send_message(msg, f"{divi}")
        n += 1
    conn.commit()

def add(data, taf, msg, message):
    try:
        cur.execute(f"INSERT INTO atividades(data, tarefas) VALUES('{data}', '{taf}');")
        bot.reply_to(message, "Deu certo!")
    except:
        bot.send_message(msg, 'Aconteceu algo tente novamente')
    conn.commit()


def remover(data, msg, message):
    try:
        cur.execute(f"DELETE FROM atividades WHERE data='{data} ';")
        bot.reply_to(message, f"Removido as atividades do dia {data}")
        conn.commit()
    except:
        bot.send_message(msg, "Algo deu errado")

@bot.message_handler(commands=["hoje"])
def command_hoje(message):
    msg = message.chat.id
    bot.send_message(msg, "Procurando...")
    dia = message.text
    text = dia.split()
    dias = text[1]
    bot.send_message(msg, f"{dias}")
    ler_tarefa(dias, msg)

@bot.message_handler(commands=["add"])
def command_add(message):
    msg = message.chat.id
    msgs = message.text
    div = msgs.split(',')
    text = div[1]
    div2 = text.split("'")
    data = div2[0]
    taf = div2[1]
    add(data, taf, msg, message)

@bot.message_handler(commands=["remove"])
def command_remove(message):
    msg = message.chat.id
    mgs = message.text.split()
    data = mgs[1]
    remover(data, msg, message)


@bot.message_handler(commands=["help"])
def command_help(message):
    msg = message.chat.id
    bot.send_message(msg, "/remove \n/add \n/hoje")

bot.infinity_polling()
