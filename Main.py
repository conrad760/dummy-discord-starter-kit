import sys
import os, subprocess
import Token
import asyncio
import logging
import discord
from discord.ext import commands




# DISCORD CREATE EVENT ---------------------------------------------
# logging.basicConfig(level=logging.INFO)

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# discord.version_info
print(discord.__version__)
bot = commands.Bot(command_prefix='!', description='''Hello there ;)''')
#bot.remove_command('help')

# DISCORD EVENTS ---------------------------------------------
# @bot.event
# async def on_ready():
# @bot.event
# async def on_server_join(guild):


# @bot.event
# async def on_message(message):
    # await bot.process_commands(message)

#@bot.event
#async def on_voice_state_update(member, voiceBefore, voiceAfter):
#@bot.event
#async def on_member_join(member):

# @bot.event
# async def on_member_remove(member):

#@bot.event
#async def on_member_update(before, after):

# @bot.event
# async def on_channel_create(channel):
# @bot.event
# async def on_channel_delete(channel):
# @bot.event
# async def on_server_role_create(role):
# @bot.event
# async def on_server_role_delete(role):
# @bot.event
# async def on_server_role_update(before,after):
# @bot.event
# async def on_member_ban(member):
# @bot.event
# async def on_member_unban(guild,user):
# @bot.event
# async def on_reaction_add(reaction, user):
# @bot.event
# async def on_raw_reaction_add(payload):


# @bot.event
#@bot.command(pass_context = True)

Token.runBot(bot)


