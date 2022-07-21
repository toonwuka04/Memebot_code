import os
from discord.ext import commands
import requests
import json
import random
import yoda
import discord
import requests



token = os.getenv('TOKEN')
dalletoken = os.getenv('dalletoken')

bot = commands.Bot(command_prefix="$")



@bot.listen()
async def on_ready():
    print(f'Connected to Discord as {bot.user}!')

@bot.listen()
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content == "Hello MemeSoundbot!":
    await message.channel.send("whats upp!")

@bot.command(name="e", help="Echoes provided text back to the channel")
async def echo(ctx, *arg):
  await ctx.send(" ".join(arg))


#for x in os.listdir("audio"):
#  print(x)
#  filex = discord.File(open(x, "rb"))

@bot.command(name="meme", help="Echoes provided text back to the channel")
async def memesound(ctx, *arg):
  #print("hi")
  randmeme = random.choice(os.listdir("audio"))
  filex = discord.File(open("audio/" + randmeme, "rb"))  
  await ctx.send(file=filex)


def get_quotes():
  response = requests.get("https://zenquotes.io/api/quotes")
  quotes = json.loads(response.text)
  return quotes


quotes = get_quotes()

def get_yodaized_quote():
  quote = random.choice(quotes)
  yodafied_quote = yoda.translate(quote['q'])
  quote = f"Yoda-{quote['a']} said, \"{yodafied_quote}\""
  return(quote)
  
def get_quote():
  quote = random.choice(quotes)
  quote = f"{quote['a']} said, \"{quote['q']}\""
  return(quote)

@bot.command(name="inspire", help="Send an inspirational quote to the channel")
async def inspire(ctx, *args):
  await ctx.send(get_quote())

@bot.command(name="yoda", help="Send an inspirational quote to the channel")
async def yodaized_quote(ctx, *args):
  await ctx.send(get_yodaized_quote())


@bot.command(name="display", help="Send prompt")
async def display_image(ctx, *args):
  empty_string = ""
  for wrd in args:
    empty_string = empty_string + wrd + " "

  print(empty_string)
    
  r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': empty_string,
    },
    headers={'api-key': dalletoken}
  )
  #print(args)
  print(r.json()["output_url"])
  
  await ctx.send(r.json()["output_url"])



bot.run(token)