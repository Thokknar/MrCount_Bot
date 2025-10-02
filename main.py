import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

file_path = "mrcount_data.json"
data = {'count':12000,
        'msg':'REMAINING...'
}

@bot.event
async def on_ready():
    print(f'We are ready to go in, {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send('Hello {}'.format(ctx.author.name))

# !set_count
@bot.command()
async def set_count(ctx,*,msg):
    data['count'] = int(msg)
    write_to_json()
    await ctx.send(str_count())

# !set_msg
@bot.command()
async def set_msg(ctx,*,msg):
    data['msg'] = msg
    write_to_json()
    await ctx.send(str_count())

# !count
@bot.command()
async def count(ctx):
    await ctx.send(str_count())

# !sub
@bot.command()
async def sub(ctx, *, msg):
    data['count'] = data['count'] - int(msg)
    write_to_json()
    await ctx.send(str_count())

# !add
@bot.command()
async def add(ctx, *, msg):
    data['count'] = data['count'] + int(msg)
    write_to_json()
    await ctx.send(str_count())

def str_count():
    return f"# {data['count']} {data['msg']}"

def write_to_json():
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
    else:
        write_to_json()

    bot.run(token, log_handler=handler, log_level=logging.DEBUG)