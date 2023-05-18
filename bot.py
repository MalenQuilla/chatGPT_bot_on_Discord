import os
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

openai.api_key = os.getenv('OPENAPI')

bot = commands.Bot(command_prefix='da.', intents=intents)

model_engine = "gpt-3.5-turbo"

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

conversation_history = []

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    match message.content:
        case 'Dauto gay':
            print("Gay function called")
            await message.channel.send('Gay con mẹ mày béo')
        case '???':
            print("?? function called")
            await message.channel.send('Câm')
    if message.content == 'raise-exception':
        raise discord.DiscordException
    else:
        await bot.process_commands(message)


@bot.command()
async def ai(ctx, *, message):
    print(conversation_history)
    
    conversation_history.append({"role": "user", "content": message})

    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=conversation_history,
        max_tokens=1024,
    )
    
    response = "".join(choice["message"]["content"] for choice in completion["choices"])

    # Split the response into blocks based on the position of the last period or question mark
    blocks = []
    while len(response) > 1900:
        last_period = response[:1900].rfind(".")
        last_question_mark = response[:1900].rfind("?")
        if last_period == -1:
            last_index = last_question_mark
        elif last_question_mark == -1:
            last_index = last_period
        else:
            last_index = max(last_period, last_question_mark)
        blocks.append(response[:last_index+1])
        response = response[last_index+1:]

    blocks.append(response)
    for block in blocks:
        await ctx.send(f'```{block}```')

bot.run(TOKEN)