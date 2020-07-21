import discord
import deposit
import get
import transaction
from output import OutputHandler as OutputHandler
#print(discord.__version__)  # check to make sure at least once you're on the right version!

token = open("token.txt", "r").read()  # I've opted to just save my token to a text file. 

client = discord.Client()  # starts the discord client.

COMMAND_HELP = {
  'deposit' : 'deposit <amt> [title]'
}

outputHandle = OutputHandler()

# def bot_print(msg):
#   print(msg)

def cmd_help(command):
  try:
    outputHandle.output(COMMAND_HELP[command])
  except:
    outputHandle.output(f"Error on {command}: command not found")

def parseMsg(message):
  msg = message.content.strip().lower()
  print('DEBUG:', msg, COMMAND_HELP.keys())
  if str(message.author) != 'FlyingPotato#1776':
    return 'auth problem'
  elif msg in COMMAND_HELP:
    # outputHandle.output(cmd_help(msg))
    return {
      'command' : msg,
      'error' : True
    }
  else:
    content = msg.split(' ', 1)
    # outputHandle.output(content)
    try:
      d = {
        'command' : content[0].lower(),
        'arguments' : content[1].lower(),
        'error' : False
      }
    except:
      return {
      'command' : msg,
      'error' : True
    }
    print('d: ', d)
    return d
    # except:
      # cmd_help(message.content)

def deposit_handler(args):
  arglist = args.split(' ')
  if len(arglist) == 1:
    title = 'Paycheck'
  else:
    title = arglist[1]
  try:
    amt = float(arglist[0])
  except:
    outputHandle.output(f'Unknown float amount: {amt}')
    # cmd_help('deposit')
    return 'ERROR'
  deposit.main(title, amt, outputHandle)

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.


@client.event
async def on_message(message):  # event that happens per any message.

    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    print(message.author)
    print(message.content.strip().lower())
    print(message.author == 'FlyingPotato#1776')
    print(message.content.strip().lower() == 'get')
    if str(message.author) == 'FlyingPotato#1776' and message.content.strip().lower() == 'get':
      get.main(outputHandle)
      print(f"Messaged Processed: {message.channel}: {message.author}: {message.author.name}: {message.content}")
      await message.channel.send(str(outputHandle))
    elif str(message.author) == 'FlyingPotato#1776' and message.content.strip().lower()[0] in '+-':
      transaction.main(message.content.strip(), outputHandle)
      await message.channel.send(str(outputHandle))
    else:
      if str(message.author) != "MONEY_APP#5784":
        data = parseMsg(message)
        print(f'data: {data}')
        if data == 'auth problem':
          print(f"Unauthorized User: {message.author}")
        elif data['error']:
          cmd_help(data['command'])
          await message.channel.send(str(outputHandle))
        else:
          # bot_print(f'processing: {data["command"]}')
          result = COMMANDS[data['command']](data['arguments'])
          if result == 'ERROR':
            # bot_print(f'help: {data["command"]}')
            cmd_help(data['command'])

          print(f"Messaged Processed: {message.channel}: {message.author}: {message.author.name}: {message.content}")
          await message.channel.send(str(outputHandle))

COMMANDS = {
  'deposit' : deposit_handler
}

client.run(token)  # recall my token was saved!