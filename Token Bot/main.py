import asyncio
import discord
import random
import time
import pymysql

#Global Vars
bottoken = ''
client = discord.Client()

#Functions waits for !token command, sends token and stores information 
@client.event
@asyncio.coroutine

def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    messagelog = open('message_log.txt','a')
    chatmessage = str(message.content)
    chatauthor = str(message.author)
    bottime = time.strftime('%m-%d-%Y %H:%M')
    chatlog = ('{} - "{}" {}\n').format(chatauthor,chatmessage,bottime)
    messagelog.write(chatlog)
    messagelog.close()

    if message.content.startswith('!token'):
        user_token = random.getrandbits(25)
        msg1 = 'Hello {0.author.mention}, your token is'.format(message)
        msg = '{} {}. Your token will expire in 5 minutes and is single use.'.format(msg1,user_token)
        
        yield from client.send_message(message.author, msg)
        
        bottime = time.strftime('%H:%M')
        log_output = ('token {} created for user {} at {}\n'.format(user_token,message.author,bottime))
        print (log_output)
        
        tokenlog = open('tokenlog.txt', 'a')
        tokenlog.write(log_output)
        tokenlog.close
        
        #Connect to MySQL data base
        config = {
            'user': 'root',
            'passwd':'RU1KCu#gKzb4ELS*h#Gfuj#aIXBLECUH0d@nOD4to',
            'host':'104.156.226.125',
            'port':3306,
            'db':'tokens'
        }
        conn = pymysql.connect(**config)
        cur = conn.cursor()
        print ('Connected to MySQL databse')
        
        number = int(user_token)
        string = str(message.author)
        
        #writes token to MySQL db
        print('Writing token to databse...')
        cur.execute("INSERT INTO token_entry VALUES(%s)", (int(number)))
        conn.commit()
        conn.close()
        print('Token added to data base')
        
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

    print('------')
    

client.run(bottoken)
