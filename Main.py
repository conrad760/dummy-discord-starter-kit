import sys
import os
import subprocess
import Token
import asyncio
import logging
import discord
from discord.ext import commands


global Guild

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
# bot.remove_command('help')

# DISCORD EVENTS ---------------------------------------------
@bot.event
async def on_ready():
    global Guild

    Guild = bot.get_guild(455504369841078282)

# @bot.event
# async def on_server_join(guild):


@bot.event
async def on_message(message):
    await bot.process_commands(message)

# @bot.event
# async def on_voice_state_update(member, voiceBefore, voiceAfter):
# @bot.event
# async def on_member_join(member):

# @bot.event
# async def on_member_join(member):

# @bot.event
# async def on_member_remove(member):

# @bot.event
# async def on_member_update(before, after):

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

#@bot.command(pass_context = True)
# async def commandName(ctx, *args):

@bot.command(pass_context=True)
async def hello(ctx, *args):
    if len(args) == 0:
        await ctx.channel.send("Hello " + str(ctx.author.display_name))
    elif len(args) == 1:
        await ctx.channel.send("Hello " + args[0] + ctx.author.display_name)



@bot.command(pass_context=True)
async def ismyserver(ctx, *args):
    global Guild

    newGuild = ctx.guild

    if Guild == newGuild:
        await ctx.channel.send("Yes, this is your guild.\nIt's name is " + str(newGuild))
    else:
        await ctx.channel.send("No, this is not your guild.\nThis one is " + str(newGuild) + ", yours is " + str(Guild))
Token.runBot(bot)
