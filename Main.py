import sys
import os, subprocess
import Token
import asyncio
import logging
import discord
from discord.ext import commands
import DNDTracker
import ServerAge
import Help
import random
import math
import GameHandler
import SaveSystem
import requests

import calendar, datetime, time




# GLOBAL VARIABLES HERE
global Guild #The Discord server
global colors  # Excludes whites, blacks, and grays
global dndObject
colors = [discord.Colour.teal(), discord.Colour.dark_teal(),
          discord.Colour.green(), discord.Colour.dark_green(),
          discord.Colour.blue(), discord.Colour.dark_blue(),
          discord.Colour.purple(), discord.Colour.dark_purple(),
          discord.Colour.magenta(), discord.Colour.dark_magenta(),
          discord.Colour.gold(), discord.Colour.dark_gold(),
          discord.Colour.orange(), discord.Colour.dark_orange(),
          discord.Colour.red(), discord.Colour.dark_red()]
global AutoResponse

global voiceTotal
global voiceChannels
global voiceTextChannels
global voiceRoles
global voiceRequestChannel

global poolOfLifeTime
poolOfLifeTime = False

global helpMenu

global nextWipe
global smokeTime, smokeAmount, smokeMessageID, totalAmount, daysPassed

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
bot.remove_command('help')

def fileInitialize(file, With, times):
    if not os.path.exists(file):
        f = open(file, 'w')
        if times >= 1:
            f.write(With)
        for i in range(1, times):
            f.write("\n" + With)
        f.close()
def checkDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

        return False
    return True
async def addrole(member, roleID, reason):
    global Guild
    try:
        role = discord.utils.get(Guild.roles, id=roleID)
        if role == None:
            raise Exception.NoRole
        print("Trying to add " + role.name + " to " + member.name + ".")
        await asyncio.sleep(0.5)
        try:
            await member.add_roles(role, reason=reason)
        except discord.HTTPException:
            print("Failed to add role")
    except:
        print("Failed to get role on Add")
async def removerole(member, roleID, reason):
    global Guild
    try:
        role = discord.utils.get(Guild.roles, id=roleID)
        if role == None:
            raise Exception.NoRole
        print("Trying to remove " + role.name + " from " + member.name + ".")
        await asyncio.sleep(0.5)
        try:
            await member.remove_roles(role, reason=reason)
        except discord.HTTPException:
            print("Failed to remove role")
    except:
        print("Failed to get role on Remove")
def checkrole(member, role):
    global Guild
    try:
        member = userToMember(Guild, member)
        if isinstance(member, type(None)):
            return False
    except:
        return False
    rolelist = []
    for x in range(0, len(member.roles)):
        if isinstance(member.roles[x], int):
            rolelist.append(member.roles[x])
        else:
            rolelist.append(member.roles[x].id)

    if role in rolelist:
        return True
    return False
def userToMember(guild, user):
    return guild.get_member(user.id)
def getName(member):
    if type(member) == discord.Object:
        return "<Object Member>"
    elif type(member) != discord.member or member.nick == None:
        return member.name
    else:
        return member.nick
def getMember(memberSearch):
    global Guild
    memberSearch = memberSearch.lower()
    for memb in Guild.members:
        if getName(memb).lower() == memberSearch:
            return memb
        elif memb.name.lower() == memberSearch:
            return memb
    for memb in Guild.members:
        if memberSearch in getName(memb).lower():
            return memb
        elif memberSearch in memb.name.lower():
            return memb
    return None
async def delete_delay(message, time):
    await asyncio.sleep(time)
    await message.delete()
def UTC_time_to_epoch(timestamp):
    return calendar.timegm(timestamp.utctimetuple())
async def voice_update_message(VC_ID, TC_ID, Role, member, before, after):
    global Guild
    channel = Guild.get_channel(TC_ID)

    memberUpdateTTS = True
    muteTTS = True
    deafenTTS = True
    serverActivityTTS = True

    if VC_ID == 560805691955347456:  # Sleepy Peeps
        muteTTS = False
        deafenTTS = False
        serverActivityTTS = False

    if VC_ID == 544011038077747202:  # Music Room
        muteTTS = False
        deafenTTS = False

    if VC_ID == 563971598542176266:  # Twitch Room
        muteTTS = False

    if VC_ID == 571038636745818156:  # Theater
        memberUpdateTTS = False
        muteTTS = False
        deafenTTS = False
        serverActivityTTS = False

    if VC_ID == 583540070502498304:  # Lake
        memberUpdateTTS = False
        muteTTS = False
        deafenTTS = False
        serverActivityTTS = False

    if VC_ID == 546767608758927401:  # Game Chat
        muteTTS = False
        deafenTTS = False

    if ((before == None or before.channel == None or before.channel.id != VC_ID) and (
            after != None and after.channel != None and after.channel.id == VC_ID)):
        await addrole(member, Role, "Automatic VC Role Addition")
        await channel.send("<@" + str(member.id) + "> joined", tts=memberUpdateTTS)
        return
    if ((before != None and before.channel != None and before.channel.id == VC_ID) and (
            after == None or after.channel == None or after.channel.id != VC_ID)):
        await removerole(member, Role, "Automatic VC Role Removal")
        await channel.send(str(member.display_name) + " left", tts=memberUpdateTTS)
        return
    if after.channel != None and after.channel.id == VC_ID:
        if (not before.deaf and after.deaf):
            await channel.send(str(member.display_name) + " has been server deafened", tts=serverActivityTTS)
        elif (before.deaf and not after.deaf):
            await channel.send(str(member.display_name) + " is no longer server deafened", tts=serverActivityTTS)

        elif (not before.mute and after.mute):
            await channel.send(str(member.display_name) + " has been server muted", tts=serverActivityTTS)
        elif (before.mute and not after.mute):
            await channel.send(str(member.display_name) + " is no longer server muted", tts=serverActivityTTS)

        elif (not before.self_deaf and after.self_deaf):
            await channel.send(str(member.display_name) + " deafened", tts=deafenTTS)
        elif (before.self_deaf and not after.self_deaf):
            await channel.send(str(member.display_name) + " undeafened", tts=deafenTTS)

        elif (not before.self_mute and after.self_mute):
            await channel.send(str(member.display_name) + " muted", tts=muteTTS)
        elif (before.self_mute and not after.self_mute):
            await channel.send(str(member.display_name) + " unmuted", tts=muteTTS)

async def removeAllColors(member):
    if checkrole(member, 541787005630152714):
        await removerole(member, 541787005630152714, "Color Role Removal")
    if checkrole(member, 546993546259988490):
        await removerole(member, 546993546259988490, "Color Role Removal")
    if checkrole(member, 544011780243062803):
        await removerole(member, 544011780243062803, "Color Role Removal")
    if checkrole(member, 541787056410591328):
        await removerole(member, 541787056410591328, "Color Role Removal")
    if checkrole(member, 550101190579585024):
        await removerole(member, 550101190579585024, "Color Role Removal")
    if checkrole(member, 546761442053980160):
        await removerole(member, 546761442053980160, "Color Role Removal")
    if checkrole(member, 541787107354607617):
        await removerole(member, 541787107354607617, "Color Role Removal")
    if checkrole(member, 541787118398078993):
        await removerole(member, 541787118398078993, "Color Role Removal")
    if checkrole(member, 558188429398114304):
        await removerole(member, 558188429398114304, "Color Role Removal")
    if checkrole(member, 541787112815460364):
        await removerole(member, 541787112815460364, "Color Role Removal")
    if checkrole(member, 544365366374039572):
        await removerole(member, 544365366374039572, "Color Role Removal")
    if checkrole(member, 544009636723032074):
        await removerole(member, 544009636723032074, "Color Role Removal")
    if checkrole(member, 541787119144796170):
        await removerole(member, 541787119144796170, "Color Role Removal")
    if checkrole(member, 544203447831101442):
        await removerole(member, 544203447831101442, "Color Role Removal")
    if checkrole(member, 549403269710217216):
        await removerole(member, 549403269710217216, "Color Role Removal")
    if checkrole(member, 558100738861957134):
        await removerole(member, 558100738861957134, "Color Role Removal")
    if checkrole(member, 549381568511082498):
        await removerole(member, 549381568511082498, "Color Role Removal")
    if checkrole(member, 547984696324128787):
        await removerole(member, 547984696324128787, "Color Role Removal")
async def checkVoiceChannel():
    global Guild
    while True:
        await asyncio.sleep(600)
        print("Giving point to people in Voice Channels")
        for member in Guild.members:
            if (not member.bot) and member.voice != None:
                if member.voice.self_deaf:
                    pass
                elif member.voice.channel.id == 560805691955347456:  # Sleepy Peeps
                    sa = ServerAge.ActivityTracker(member.id)
                    sa.setPoints(sa.GetPoints + 5)
                elif member.voice.channel.id == 583540070502498304:  # The Lake
                    sa = ServerAge.ActivityTracker(member.id)
                    sa.setPoints(sa.GetPoints + 5)
                elif member.voice.self_mute:
                    sa = ServerAge.ActivityTracker(member.id)
                    sa.setPoints(sa.GetPoints + 10)
                else:
                    sa = ServerAge.ActivityTracker(member.id)
                    sa.setPoints(sa.GetPoints + 20)
def halfSum(amount, percent):
    if amount <= 0:
        return 0
    percent *= 0.5
    return percent + halfSum(amount - 1, percent)
async def checkTwitchChat():
    global Guild
    while True:
        await asyncio.sleep(5)

        checkDir("TwitchChatBot/Messages")
        filePath = "TwitchChatBot/Messages/unpostedMessages.txt"
        if not os.path.isfile(filePath):
            fileInitialize(filePath, "0", 40)
            '''
            0 Number of Unposted Messages
            1 Message 1
            2 Message 2
            3 ...
            '''

        lines = open(filePath).read().splitlines()

        channel = Guild.get_channel(563971681866088450)
        messages = []
        for i in range(int(lines[0])):
            messages.append(lines[i+1])

        lines[0] = "0"

        f = open(filePath, 'w')
        for i in range(len(lines)):
            f.write(lines[i] + "\n")
        f.close()


        for i in range(len(messages)):
            if messages[i][:3].lower() == "!sr":
                await channel.send("!play " + messages[i][4:])
            else:
                await channel.send(messages[i], tts=not any(x in messages[i].lower() for x in ['fuck', 'shit', 'cum ', 'com ', 'retard']))
async def randomizeUsername(member):
    username = random.choice(["Aaron", "A-2000", "Wondering Soul", "A-3013", "A-3015", "A-3016", "Charlie", "Noraa",
                              "A-0000", "A-0562", "A-1000", "A-1032", "A-1263", "Diugantu&167.24.582.1030",
                              "A-3006", "B-000", "B-001", "Amaranth Crystal", "C-001", "The Velociraptor",
                              "C-004", "C-005", "C-007", "C-008", "C-009", "C-016", "C-017", "C-018",
                              "C-022", "C-022-2", "C-024", "Carson", "George"])


    await member.edit(nick=username, reason="Aaron set it up")
async def checkMinecraftChat():
    global Guild

    filePath = "../ScreenOutput/Minecraft.txt"

    currentLine = len(open(filePath).read().splitlines())
    while True:
        await asyncio.sleep(5)

        lines = open(filePath).read().splitlines()

        channel = Guild.get_channel(610686889040674836)

        while currentLine < len(lines):
            l = lines[currentLine]
            if "<" in l:
                await channel.send(l[l.find("<"):])
            elif "joined the game" in l:
                await channel.send(l[l.find("]:")+2:l.find(" joined")] + " joined the server")
            elif "left the game" in l:
                await channel.send(l[l.find("]:")+2:l.find(" left")] + " left the server")
            currentLine += 1

# DISCORD EVENTS ---------------------------------------------
@bot.event
async def on_ready():
    global dndObject
    global PABoard
    global Guild
    global AutoResponse
    global voiceTotal
    global voiceChannels
    global voiceTextChannels
    global voiceRoles
    global voiceRequestChannel
    global helpMenu
    global nextWipe
    global smokeTime, smokeAmount, smokeMessageID, totalAmount, daysPassed
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    Guild = bot.get_guild(537752716680888350)

    dndObject = [None, None, None]
    dndObject[0] = DNDTracker.DND(Guild, 0)
    dndObject[1] = DNDTracker.DND(Guild, 1)
    dndObject[2] = DNDTracker.DND(Guild, 2)

    checkDir("Personality")
    fileInitialize("Personality/Data.txt", "0", 1000)

    AutoResponse = int(open("Personality/Data.txt", encoding='utf-8').read().splitlines()[0])

    voiceTotal = 17
    #                Friend Den            Global Speaker        Roarin Space      Chit Chat
    voiceChannels = [565626436849893379, 565624762957824021, 563616007789346826, 560808536624594973,
                    # Global                   Gaming            Personal            Cadre
                   544010529518387203, 544010556433235971, 544010687358173194, 544010602788421632,
                    #Crazy Town             Music Room     Twitch Stream
                   544010882238251040, 544011038077747202, 563971598542176266,
                    # Sleepy Peeps             Lake
                   560805691955347456, 583540070502498304,
                    # Theater               Chill Zone         Game Chat           Outside of Game
                   571038636745818156, 563136668316729404, 546767608758927401, 548898527003017227]
    voiceTextChannels = [571039046063882270, 571039065646956554, 571038968133451879, 571038882351546369,
                         544012301158580256, 544012368087351307, 544012982716203018, 544013073560764436,
                         544013179521335321, 544013203646971914, 563971681866088450,
                         560825265434132490, 583540169072705537,
                         571038681348177921, 565570374083805195, 571039187877363754, 571039216935632897]
    voiceRoles = [ 571039356618276876, 571039357876699154, 571039351249698816, 571039348510687253,
                   544012503063986181, 544012559422980096, 544012584094007307, 544012629891350529,
                   544012712737243136, 544012739195174912, 563971722458693662,
                   560825387538710568, 583540213306097664,
                   571039342915485696, 565570442731978772, 571039360548339732, 571039362683502592]

    voiceRequestChannel = 537752716680888356

    lines = SaveSystem.Data("Smoke.txt").loadFile(5)
    smokeTime = int(lines[0])
    smokeAmount = int(lines[1])
    smokeMessageID = int(lines[2])
    totalAmount = int(lines[3])
    daysPassed = int(lines[4])

    helpMenu = [[0,  # Default
                 544013203646971914,  # VC_Music_Room
                 547862551208263680,  # Console
                 554430142655496202,  # Game Hub
                 563396120102043649,  # Amaranth Bank
                 563396267569578008,  # Battleship
                 554431462682656781,  # Dungeon Adventure
                 554431493770838026,  # Farm Simulator
                 554430280090386432,  # Guess the Number
                 554431521008779274,  # Jackpot
                 554430335442616359   # Tic-Tac-Toe
                ],
                [  # Commands
                    [  # Default
                        ["help", "[Command]", "[subCommand]"],
                        ["event", "{list}", "{when}", "{whenexact}", "{create}", "{destroy}", "{seteventchannel}", "{post}", "{preview}", "{addrole}", "{removerole}", "{settitle}", "{setdescription}", "{setreminder}", "{settime}", "{setvoice}", "{setduration}", "{setweekday}", "{setweeklyrepeat}"]
                    ], [  # VC_Music Room
                        ["ump"]
                    ], [  # Console
                        ["reboot"],
                        ["say", "<channel_id>", "<message>"]
                    ], [  # Game Hub
                        ["game", "{catalog}", "{donation}", "{checktime}", "{buy}", "{money}", "{give}"]
                    ], [  # Amaranth Bank
                        ["game", "{deposite}", "{withdraw}", "{getLoan}", "{payLoan}"]
                    ], [  # Battleship
                        ["game"]
                    ], [  # Dungeon Adventure
                        ["game"]
                    ], [  # Farm Simulator
                        ["game", "{buyLand}", "{buyCrop}", "{waterCrops}", "{sellCrops}"]
                    ], [  # Guess the Number
                        ["game", "<numberToGuess>"]
                    ], [  # Jackpot
                        ["game"]
                    ], [  # Tic-Tac-Toe
                        ["game", "{play}", "{place}"]
                    ]
                ],
                [  # Description
                    [  # Default
                        [  # Help
                            "Displays helpful information about commands",
                            "Type a command to get information about that commands",
                            "Used to get even more help on a specific command"
                        ],
                        [  # Event
                            "Allows users to schedule and modify events",
                            "!event list\n\nLists all active events, even if they have already passed",
                            "!event when <eventID>\n\nEvery event has an ID. This command will use that ID to tell you when that event is going to occur, rounded to the nearest relevant time unit.",
                            "!event whenexact <eventID>\n\nThis command will use the evnetID to tell you when that event is going to occur down to the second",
                            "!event create <time>\n\nCreates a new event. Time can have the following formats separated by the character ;\nMonth/Day/Year - Examples: 1/19/2020, 02/6/26, 03/05/2037\nHour:Minutes - Examples: 10:00, 15:23, 10:00am, 5:20pm\n\nExample together: 1/19/2020;10:00am",
                            "!event destroy <eventID>\n\nRemoves an event. Simple as that.",
                            "!event seteventchannel\n\nSets the current channel to be the event channel where events are posted.",
                            "!event post <eventID>\n\nPosts an event in the event channel, adding a reaction for people to mark if they are going",
                            "!event preview <eventID>\n\nPosts an event in the same channel. Similar to !event post, but does not trigger the event going live.",
                            "!event addrole <eventID> <roleID>\n\nAdds a role to mention when posting. These people are AUTOMATICALLY added to the list of people going.\n<roleID> can be the exact role ID, or a role mention.",
                            "!event removerole <eventID> <roleID>\n\nRemoves a role from the event.\n<roleID> can be the exact role ID, or a role mention.",
                            "!event settitle <eventID> <title...>\n\nAdds a title to the event. The title is every word after the event ID",
                            "!event setdescription <eventID> <description...>\n\nAdds a description to the event. The description is every word after the event ID",
                            "!event setreminder <eventID> <type> (type2) (type3)...\n\nSets which reminders to use. Put None for no reminders.\nAvailable Reminders: on, thirtyminutes, hour, day, week",
                            "!event settime <eventID> <time>\n\nLets to re-set the event time to a different time. See !help event create for more details on setting time.",
                            "!event setvoice <eventID> <voiceChannelID>\n\nThis ID will be used to create an invite for the channel which will be sent with reminders. To get the ID of a voice channel, turn on developer mode, and then right click on a voice channel and copy ID.",
                            "!event setduration <eventID> <duration>\n\nSets how long the event last. The event will not re-schedule automatically until the event is over.\n<duration> is in the format <time><unit>, separated by the character ;. Unides are d for days, h for hours, m for minutes and s for seconds.\nExample: 1h;2m, or 1d;2h;3m",
                            "!event setweekday <eventID> <day> <day2> <day3>...\n\nSets which day(s) of the week to repeat on. This CAN NOT work with setweeklyrepeat.\nExample: !event setweekday 1 monday tues friday sat",
                            "!event setweeklyrepeat <eventID> <repeatType>\n\nSets how to repeat weekly.\n<RepeatType> can be Weekly, Bi-Weekly, Tri-Weekly, Quad-Weekly, Monthly, Bi-Monthly, Tri-Monthly, Quad-Monthly, or Yearly"
                        ]
                    ], [  # VC_Music_Room
                        [  # UMP
                            "Upload a file to update the music bots playlist. You can use !pldump <youtubePlaylist> to get the file"
                        ]
                    ], [  # Console
                        [  # Restart
                            "Restarts the bot. It takes 5 seconds to reboot."
                        ],
                        [  # Say
                            "Makes the bot repeat what you say.",
                            "The channel to send the message too. You can get this by turning on Developer Mode and right clicking a channel, and then copying the ID.",
                            "The message to post. This can be any length and does not need to be in quotes. !say 123456789 Hello World."
                        ]
                    ], [  # Game Hub
                        [  # Game
                            "The game hub menu. Use this command to interact with every game type including the Game Hub.",
                            "!game catalog\nThis command lists every game and if you own them or not.",
                            "!game donation\nThis gives you 5 coins then puts you on a 1 day cooldown before you can use the command again.",
                            "!game checktime\nThis command tells you how long until you can claim the donation again. This is on a small cooldown.",
                            "!game buy <game>\nUsed to buy games, if you have enough money. This will give you a new role so you can access the games text channel.",
                            "!game money\nDisplays how much money you currently have.",
                            "!game give <amount> <player>\nGives a certain amount of money to the given player. <player> can be a mention or an ID."
                        ]
                    ], [  # Amaranth Bank
                        [  # Game
                            "Use this command to get general information about your account. Use the sub-commands to interact with the bank",
                            "!game deposit <amount>\nDeposits a certain amount of money in the bank, which will earn interest over time",
                            "!game withdrawl <amount>\nTakes out a certain amount of money held in your account. You can not withdraw if you take out more then you have or the bank does not have enough money.",
                            "!game getLoan <amount>\nThe bank will loan you money which you have to pay back eventually. The interest will go up each day until you run out of money.",
                            "!game payLoan <amount>\nPays back the loan to the bank."
                        ]
                    ], [  # Battleship
                        [  # Game
                            "Get general information on the game."
                        ]
                    ], [  # Dungeon Adventure
                        [  # Game
                            "Get general information on the game."
                        ]
                    ], [  # Farm Simulator
                        [  # Game
                            "Provides general information about your land and crops",
                            "",
                            "",
                            "",
                            ""
                        ]
                    ], [  # Guess the Number
                        [  # Game
                            "Guess the number to win the prize! It costs 5 coins to make a guess",
                            "The amount to guess! Pick a number, any number."
                        ]
                    ], [  # Jackpot
                        [  # Game
                            "Get general information on the game."
                        ]
                    ], [  # Tic-Tac-Toe
                        [  # Game
                            "Play a classic game of Tic-Tac-Toe. The goal is to get three in a row",
                            "!game play <mention>\nMention a player to invite them to play. It costs 10 coins each.",
                            "!game place <x> <y>\nThe position to place the piece on the board. X goes left to right, 1-3, and Y goes top to bottom, 1-3."
                        ]
                    ]
                ]
                ]

    nextWipe = int(SaveSystem.Data("MinecraftData.txt").loadFile(2)[0])
    if nextWipe <= 100:
        nextWipe = int(time.time())+2592000
        SaveSystem.Data("MinecraftData.txt").saveData([nextWipe, 0])

    bot.loop.create_task(checkVoiceChannel())
    bot.loop.create_task(checkTwitchChat())
    bot.loop.create_task(checkMinecraftChat())

# @bot.event
# async def on_server_join(guild):


@bot.event
async def on_message(message):
    global AutoResponse
    global poolOfLifeTime
    global nextWipe

    print(message.author.name + ": " + message.content)
    await bot.process_commands(message)

    # Update Server Age Role                                                 Bot Playground            Spam
    try:
        if (not (message.author.bot)) and (not (message.channel.id in [541666013994024962, 544624213118681088])):
            serverAge = ServerAge.AgeTracker(message.author.id)
            serverAge.setTime(int(time.time() - UTC_time_to_epoch(message.author.joined_at)))
            #print("Join Time: " + str(int(time.time() - UTC_time_to_epoch(message.author.joined_at))))

            roles = message.author.roles
            for r in range(len(roles)):
                if not isinstance(roles[r], int):
                    roles[r] = roles[r].id

            if serverAge.needsRoleChange(roles):
                await removerole(message.author, serverAge.CurrentRole, "Auto Server Age Role Changer")
                serverAge.updateRole()
                await addrole(message.author, serverAge.CurrentRole, "Auto Server Age Role Changer")

            serverActivity = ServerAge.ActivityTracker(message.author.id)
            serverActivity.setPoints(serverActivity.GetPoints + 3 + int(len(message.content) / 10))

            if serverActivity.CurrentRole == 553046733941243916:  # Hibernating
                serverActivity.setPoints(50)

            if serverActivity.needsRoleChange(roles):
                await removerole(message.author, serverActivity.CurrentRole, "Auto Activity Role Changer")
                serverActivity.updateRole()
                await addrole(message.author, serverActivity.CurrentRole, "Auto Activity Role Changer")

    except:
        print("User was not member")



    globalActivityTracker = ServerAge.GlobalActivityTracker()
    if checkrole(message.author, 541665834695655454) and globalActivityTracker.NeedsDailyRefresh:
        poolOfLifeTime = True
        globalActivityTracker.setTime()
        for member in Guild.members:
            if not (member.bot):
                serverActivity = ServerAge.ActivityTracker(member.id)
                serverActivity.setPoints(int(serverActivity.GetPoints*(0.66 + 0.34 * halfSum(serverActivity.Multiplier, 1))))
                roles = member.roles
                for r in range(len(roles)):
                    if not isinstance(roles[r], int):
                        roles[r] = roles[r].id
                if serverActivity.needsRoleChange(roles):
                    await removerole(member, serverActivity.CurrentRole, "Auto Activity Role Changer")
                    serverActivity.updateRole()
                    await addrole(member, serverActivity.CurrentRole, "Auto Activity Role Changer")

                # Do Aaron's Games Amaranth Bank Stuff
                hub = GameHandler.GameHub(member.id)
                AB = GameHandler.AmaranthBank(member.id)
                returnVal = AB.checkLoan()
                if returnVal[0] == 1:
                    amountPaying = AB.LoanDue*0.05
                    returnVal = AB.payLoan(amountPaying)
                    await member.send("Loan payment increased by " + str(returnVal[2]) + "\nYou now owe " + str(returnVal[1]) + "\nPaying 5% automatically: "
                                      + str(amountPaying) + " coins\nYou now have " + str(hub.Money) + " coins")
                    if hub.Money < 0:
                        AB.setMoneyInBank(AB.getMoneyInBank() + AB.LoanDue)
                        hub.setMoney(hub.Money - AB.LoanDue)
                        await member.send("You ran out of money! You are now in-dept to the bank! You owe " + str(-hub.Money) + " coins!")

                elif returnVal[0] == 2:
                    await member.send("You owe " + str(returnVal[1]))

                if AB.Interest > 0:
                    await member.send(str(AB.Interest) + " coins where added to your bank from interest.")
                    hub.setMoney(hub.Money + AB.Interest)


    filePath = "Personality/Data.txt"
    lines = open(filePath, encoding='utf-8').read().splitlines()

    if int(time.time()) - 86400 > int(lines[2]):
        lines[2] = str(int(lines[2]) + 86400)

        for member in Guild.members:
            farm = GameHandler.FarmSimulator(member.id)
            for landID in range(farm.TotalLand):
                land = farm.getLand(landID)
                if land[2] < int(time.time()) - 172800:
                    land[2] += 86400
                    land[3] -= 1
                    if land[3] <= 0:
                        land[3] = 0
                        land[2] = 0
                        land[1] = 0
                        await member.send("Your crops on plot " + str(landID+1) + " died")
                    else:
                        await member.send("Your crops on plot " + str(landID+1) + " are looking dry")

                    farm.saveLand(landID, land)

    f = open(filePath, 'w')
    for i in range(len(lines)):
        f.write(lines[i] + "\n")
    f.close()

    if not message.author.bot:
        # Smoke

        lines = SaveSystem.Data("Smoke.txt").loadFile(5)
        smokeTime = int(lines[0])
        smokeAmount = int(lines[1])
        smokeMessageID = int(lines[2])
        totalAmount = int(lines[3])
        daysPassed = int(lines[4])

        if smokeTime < 100:
            smokeTime = datetime.datetime.now().timestamp()
            SaveSystem.Data("Smoke.txt").saveData([int(smokeTime), smokeAmount, smokeMessageID, totalAmount, daysPassed])
            smokeAmount = 0
            msg = await Guild.get_channel(674532364961185792).send("<@319876025410519041>, you have smoked 0 times today.")
            await msg.add_reaction("🚬")
            smokeMessageID = msg.id
            totalAmount = 0
            daysPassed = 1
            SaveSystem.Data("Smoke.txt").saveData([int(smokeTime), smokeAmount, smokeMessageID, totalAmount, daysPassed])

        if datetime.datetime.now().timestamp() > smokeTime + 86400:
            msg = await Guild.get_channel(674532364961185792).fetch_message(smokeMessageID)
            await msg.clear_reactions()
            average = "On average, in total, you have smoked " + str(totalAmount / daysPassed) + " cigarettes per day."
            await msg.edit(content="<@319876025410519041>, you smoked **" + str(smokeAmount) + "** today. In total, you have smoked ***" + str(totalAmount) + "*** cigarettes!\n" + average)

            smokeTime += 86400
            smokeAmount = 0
            daysPassed += 1
            msg = await Guild.get_channel(674532364961185792).send("<@319876025410519041>, you have smoked 0 times today.")
            smokeMessageID = msg.id
            await msg.add_reaction("🚬")
            SaveSystem.Data("Smoke.txt").saveData([smokeTime, smokeAmount, smokeMessageID, totalAmount, daysPassed])

        # Minecraft
        if message.channel.id == 610686889040674836:  # Game Chat
            msg = message.author.display_name + ": " + message.content
            os.system("screen -r Minecraft -p0 -X stuff '/say " + msg + "\015'")
        elif message.channel.id == 600094798971666434:  # Whitelist
            msg = message.content
            os.system("screen -r Minecraft -p0 -X stuff '/whitelist add " + msg + "\015'")
            await Guild.get_channel(563135983625699357).send("<@"+str(message.author.id)+">, your minecraft account, " + msg + ", was added to the whitelist. Server IP is " + open("MinecraftServerIP.txt").read().splitlines()[0])

        # Automatic Noraa Responses
        if AutoResponse == 1:
            m = message.content.lower()
            if "noraa" in m:
                if "hello" in m:
                    await message.channel.send("Hello, <@" + str(message.author.id) + ">!")
                elif "hate" in m:
                    if "you" in m:
                        await message.channel.send("That is not very nice!")
                    elif "myself" in m:
                        await message.channel.send("Sorry to hear that. Try to have better self esteem!")
                    else:
                        await message.channel.send("Stop being a hater :P")
                else:
                    randomMsg = random.randint(0, 6)
                    if randomMsg == 0:
                        await message.channel.send("What is it you are wanting?")
                    if randomMsg == 1:
                        await message.channel.send("What are you are wanting?")
                    if randomMsg == 2:
                        await message.channel.send("Excuse me? How can I help you?")
                    if randomMsg == 3:
                        await message.channel.send("What do you want?")
                    if randomMsg == 4:
                        await message.channel.send("I am sorry? I am not sure what you mean.")
                    if randomMsg == 5:
                        await message.channel.send("Hello there! How can I help?")
                    if randomMsg == 6:
                        await message.channel.send("What can I do for you?")

        # One Word Wonders
        if message.channel.id == 576876844075188226:
            if " " in message.content:
                msg = await message.channel.send("<@" + str(message.author.id) + ">, only send one word at a time!")
                await delete_delay(msg, 20)
                await delete_delay(message, 1)
            else:

                checkDir("OneWordWonders")
                fileInitialize("OneWordWonders/Users.txt", "0", 300)
                fileInitialize("OneWordWonders/Words.txt", "0", 300)
                fileInitialize("OneWordWonders/Last Poster.txt", "0", 10)

                if int(open("OneWordWonders/Last Poster.txt", encoding='utf-8').read().splitlines()[0]) == message.author.id:
                    msg = await message.channel.send("<@" + str(message.author.id) + ">, do not double post!")
                    await delete_delay(msg, 20)
                    await delete_delay(message, 1)
                elif int(open("OneWordWonders/Last Poster.txt", encoding='utf-8').read().splitlines()[1]) > int(time.time()) - 2:
                    msg = await message.channel.send("<@" + str(message.author.id) + ">, message posted to close time-wise to another users message")
                    await delete_delay(msg, 5)
                    await delete_delay(message, 1)
                elif message.content.lower() == "(period)" or message.content.lower() == "(exclaim)" or message.content.lower() == "(question)":

                    filePath = "OneWordWonders/Users.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    total = int(lines[0])
                    if not (message.author.display_name in lines[1:total + 1]):
                        lines[total + 1] = message.author.display_name
                        lines[0] = str(total + 1)

                        f = open(filePath, 'w')
                        for i in range(len(lines)):
                            f.write(lines[i] + "\n")
                        f.close()

                    filePath = "OneWordWonders/Words.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    total = int(lines[0])
                    lines[0] = "0"

                    messageStr = " ".join(lines[1:total+1])


                    f = open(filePath, 'w')
                    for i in range(len(lines)):
                        f.write(lines[i] + "\n")
                    f.close()

                    if message.content.lower() == "(period)":
                        messageStr += "."
                    if message.content.lower() == "(exclaim)":
                        messageStr += "!"
                    if message.content.lower() == "(question)":
                        messageStr += "?"


                    messageStr += " (Created by: "

                    filePath = "OneWordWonders/Users.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    total = int(lines[0])
                    lines[0] = "0"

                    messageStr += ", ".join(lines[1:total + 1]) + ")"

                    f = open(filePath, 'w')
                    for i in range(len(lines)):
                        f.write(lines[i] + "\n")
                    f.close()

                    filePath = "OneWordWonders/Last Poster.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    lines[0] = str(message.author.id)
                    lines[1] = str(int(time.time()))
                    f = open(filePath, 'w')
                    for i in range(len(lines)):
                        f.write(lines[i] + "\n")
                    f.close()

                    await Guild.get_channel(576883132205367297).send(messageStr)
                elif message.content.lower()[0] == "(":
                    msg = await message.channel.send("<@" + str(message.author.id) + ">, you may have mistyped. Use (period), (exclaim), or (question)!")
                    await delete_delay(msg, 20)
                    await delete_delay(message, 1)
                else:
                    filePath = "OneWordWonders/Users.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    total = int(lines[0])
                    if not (message.author.display_name in lines[1:total+1]):
                        lines[total+1] = message.author.display_name
                        lines[0] = str(total+1)

                        f = open(filePath, 'w')
                        for i in range(len(lines)):
                            f.write(lines[i] + "\n")
                        f.close()

                    filePath = "OneWordWonders/Words.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    total = int(lines[0])
                    lines[total+1] = message.content
                    lines[0] = str(total+1)

                    f = open(filePath, 'w')
                    for i in range(len(lines)):
                        f.write(lines[i] + "\n")
                    f.close()

                    filePath = "OneWordWonders/Last Poster.txt"
                    lines = open(filePath, encoding='utf-8').read().splitlines()
                    lines[0] = str(message.author.id)
                    lines[1] = str(int(time.time()))
                    f = open(filePath, 'w')
                    for i in range(len(lines)):
                        f.write(lines[i] + "\n")
                    f.close()

        # Add automatic reactions to messages in Suggestion Chat.
        if message.channel.id == 544622635926028301:
            try:
                await message.add_reaction("✅")
                await message.add_reaction("❌")
            except discord.Forbidden:
                print("Failed to add automatic reactions in the Suggestions Chat")

    if nextWipe <= int(time.time()):
        await Guild.get_channel(563135983625699357).send("<@&563135521484832783>, the wipe has begun!")
        os.system("screen -r Minecraft -p0 -X stuff '/say The wipe is happening now\015'")
        nextWipe = int(time.time()) + 2592000
        SaveSystem.Data("MinecraftData.txt").saveData([nextWipe, 0])

        os.system("screen -r Minecraft -p0 -x stuff 'stop'")
        await asyncio.sleep(5)
        os.system("screen -XS Minecraft exit")

        await asyncio.sleep(10)

        minecraftRegionDirectory = "/home/aaron/root/Minecraft/world/region"
        for filename in os.listdir(minecraftRegionDirectory):
            fileNameData = filename.split(".")
            try:
                xcord = int(fileNameData[1])
                ycord = int(fileNameData[2])
                if xcord >= 2 or xcord <= -2 or ycord >= 2 or ycord <= -2:
                    os.remove(minecraftRegionDirectory+filename)
            except:
                pass

        minecraftRegionDirectory = "/home/aaron/root/Minecraft/world/DIM/region"
        for filename in os.listdir(minecraftRegionDirectory):
            fileNameData = filename.split(".")
            try:
                xcord = int(fileNameData[1])
                ycord = int(fileNameData[2])
                if xcord >= 2 or xcord <= -2 or ycord >= 2 or ycord <= -2:
                    os.remove(minecraftRegionDirectory + filename)
            except:
                pass

        minecraftRegionDirectory = "/home/aaron/root/Minecraft/world/DIM-1/region"
        for filename in os.listdir(minecraftRegionDirectory):
            fileNameData = filename.split(".")
            try:
                xcord = int(fileNameData[1])
                ycord = int(fileNameData[2])
                if xcord >= 2 or xcord <= -2 or ycord >= 2 or ycord <= -2:
                    os.remove(minecraftRegionDirectory + filename)
            except:
                pass

        await asyncio.sleep(5)

        os.system("/home/aaron/root/bin/SC_Minecraft")


    elif nextWipe <= int(time.time()) + 3600 and int(SaveSystem.Data("MinecraftData.txt").loadFile()[1]) <= 1:
        await Guild.get_channel(563135983625699357).send("<@&563135521484832783>, the wipe will begin in one hour!")
        os.system("screen -r Minecraft -p0 -X stuff '/say The wipe will begin in one hour\015'")
        SaveSystem.Data("MinecraftData.txt").saveData([nextWipe, 2])
    elif nextWipe <= int(time.time()) + 86400 and int(SaveSystem.Data("MinecraftData.txt").loadFile()[1]) <= 0:
        await Guild.get_channel(563135983625699357).send("<@&563135521484832783>, the wipe will begin in one day!")
        os.system("screen -r Minecraft -p0 -X stuff '/say The wipe will begin in one day\015'")
        SaveSystem.Data("MinecraftData.txt").saveData([nextWipe, 1])


@bot.event
async def on_voice_state_update(member, voiceBefore, voiceAfter):
    global voiceTotal
    global voiceChannels
    global voiceTextChannels
    global voiceRoles

    if not member.bot:
        for i in range(0, voiceTotal):
            await voice_update_message(voiceChannels[i], voiceTextChannels[i], voiceRoles[i], member, voiceBefore, voiceAfter)

@bot.event
async def on_member_join(member):

    serverActivity = ServerAge.ActivityTracker(member.id)
    serverActivity.setPoints(200)

# @bot.event
# async def on_member_remove(member):

@bot.event
async def on_member_update(before, after):
    global Guild
    global poolOfLifeTime

    if after.display_name == "Aaron" and after.id != 110858000192798720:
        await after.edit(nick="<Errorous Username>")

    roleChangeChannel = Guild.get_channel(560598745520275496)
    autoRoleChangeChannel = Guild.get_channel(560601051858862081)
    diffRemove = list(set(before.roles).difference(set(after.roles)))
    if diffRemove != [] and after.id != "110858000192798720":
        for x in range(0, len(diffRemove)):  # Activity Roles
            id = diffRemove[x]
            if not isinstance(id, int):
                id = id.id
            if id in [553046733941243916, 553046774269345881, 553046856838676503,
                553046894578892860, 553046929349672962, 553046967098540051, 557774989713997835,
                557774991865806849, 557774990997717012, 557774987503861771, 557774988573409290,
                557303963800567829,  # Age Roles
                552960724243316737, 552960818262835201, 552960819298566357, 552960821009842184,
                552960822654271501, 552960825258803225, 552960826643054603, 552960828815704103,
                552960831281692717, 552960832628326401, 552960833982824538, 552960836021387274,
                552960837539594275, 552960839393607691, 552960840320548871, 552960842526621697,
                # Voice Channel
                544012503063986181, 544012559422980096, 544012584094007307, 544012629891350529,
                544012664293163009, 544012712737243136, 544012739195174912, 560825387538710568,
                563971722458693662, 565570442731978772,
                571039362683502592, 571039360548339732, 571039342915485696, 571039346468323339, # The new 8
                571039348510687253, 571039351249698816, 571039357876699154, 571039356618276876,
                583540213306097664,  # Lake
                583531700416675853,  # Squad
                #Streaming
                557322618873577515]:

                await autoRoleChangeChannel.send("Role " + str(diffRemove[x]) + " was removed from " + after.name + "!")
            break
    diffAdd = list(set(after.roles).difference(set(before.roles)))
    if diffAdd != [] and after.id != "110858000192798720":
        for x in range(0, len(diffAdd)):  # Activity Roles
            id = diffAdd[x]
            if not isinstance(id, int):
                id = id.id
            if id in [553046733941243916, 553046774269345881, 553046856838676503,
                # Age Roles
                552960724243316737, 552960818262835201, 552960819298566357, 552960821009842184,
                552960822654271501, 552960825258803225, 552960826643054603, 552960828815704103,
                552960831281692717, 552960832628326401, 552960833982824538, 552960836021387274,
                552960837539594275, 552960839393607691, 552960840320548871, 552960842526621697,
                # Voice Channel
                544012503063986181, 544012559422980096, 544012584094007307, 544012629891350529,
                544012664293163009, 544012712737243136, 544012739195174912, 560825387538710568,
                563971722458693662, 565570442731978772,
                571039362683502592, 571039360548339732, 571039342915485696, 571039346468323339,  # The new 8
                571039348510687253, 571039351249698816, 571039357876699154, 571039356618276876,
                583540213306097664,
                583531700416675853, # Squad
                #Streaming
                557322618873577515]:
                await autoRoleChangeChannel.send("Role " + str(diffAdd[x]) + " was added to " + after.name + "!")
                break

    if checkrole(after, 541665834695655454) and after != Guild.get_member(227948413235363841) and after != Guild.get_member(239542803057606667) and after != Guild.get_member(211669044732887041) \
            and after != Guild.get_member(239540936596520961):
        if (after.activity != None and str(after.activity.name).find('Overwatch') != -1) and not checkrole(after, 544642953746841600):
            await addrole(after, 544642953746841600, "Auto Overwatch Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays Overwatch ^ - ^")
        if (after.activity != None and str(after.activity.name).find('TF2') != -1) and not checkrole(after, 544642682421510176):
            await addrole(after, 544642682421510176, "Auto TF2 Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays TF2 ^ - ^")
        if (after.activity != None and str(after.activity.name).find('SCP') != -1) and not checkrole(after, 544642579745210377):
            await addrole(after, 544642579745210377, "Auto SCP Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays an SCP game ^ - ^")
        if (after.activity != None and str(after.activity.name).find('Minecraft') != -1) and not checkrole(after, 544642742165307401):
            await addrole(after, 544642742165307401, "Auto Minecraft Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays Minecraft ^ - ^")
        if (after.activity != None and str(after.activity.name).find('Project Amaranth') != -1) and not checkrole(after, 541718745224052736):
            await addrole(after, 541718745224052736, "Auto Project Amaranth Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays Project Amaranth ^ - ^")
        if (after.activity != None and str(after.activity.name).find('Rain World') != -1) and not checkrole(after, 556824719656222720):
            await addrole(after, 556824719656222720, "Auto Project Amaranth Game role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays Rain World ^ - ^")
        if (after.activity != None and str(after.activity.name).find('VRChat') != -1) and not checkrole(after, 541407696369483808):
            await addrole(after, 541407696369483808, "Auto VRChat role addition")
            await Guild.get_channel(659689542143574027).send("I have detected that " + after.display_name + " plays VRChat ^ - ^")
        if (not checkrole(after, 557322618873577515) and (after.activity != None and after.activity.type == discord.ActivityType.streaming)) and (not checkrole(after, 553046733941243916)):
            await addrole(after, 557322618873577515, "Auto Streaming role addition")
            try:
                game = " - " + after.activity.game
            except:
                game = ""
            msg = await Guild.get_channel(544284608704020492).send(after.display_name + " is streaming `" + after.activity.details + game + "`!\n" + after.activity.url)
            checkDir("Streamers")
            filePath = "Streamers/"+str(after.id)+".txt"
            fileInitialize(filePath, "0", 50)

            lines = open(filePath, encoding='utf-8').read().splitlines()

            lines[0] = str("1")
            lines[1] = str("0")
            lines[2] = str(msg.id)

            f = open(filePath, 'w')
            for i in range(len(lines)):
               f.write(lines[i] + "\n")
            f.close()

        if (checkrole(after, 557322618873577515) and (after.activity == None or after.activity.type != discord.ActivityType.streaming)):

            checkDir("Streamers")
            filePath = "Streamers/"+str(after.id)+".txt"
            fileInitialize(filePath, "0", 50)
            lines = open(filePath, encoding='utf-8').read().splitlines()

            if lines[0] == "1":
                lines[0] = "0"
                lines[1] = str(int(time.time() + 300))
            elif lines[0] == "0":
                if time.time() > int(lines[1]):
                    await removerole(after, 557322618873577515, "Auto Streaming role removal")
                    #await Guild.get_channel(544284608704020492).send(after.display_name + " is no longer streaming")
                    msg = await Guild.get_channel(544284608704020492).fetch_message(int(lines[2]))
                    await msg.edit(content=msg.content.replace(" is streaming `", " has stopped streaming. They were streaming `").replace("`!\n", "`\n<")+">")


            f = open(filePath, 'w')
            for i in range(len(lines)):
                f.write(lines[i] + "\n")
            f.close()
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
@bot.event
async def on_reaction_add(reaction, user):
    if user.id != 541665632106840074 and reaction.message.author.id == 541665632106840074:
        if reaction.emoji == "⬅":
            book = DNDTracker.Book("DND/Book/" + reaction.message.content.splitlines()[0] + ".txt")
            book.setPage(int(reaction.message.content.splitlines()[1]))
            book.flipPageReverse()
            msg = await reaction.message.channel.send(book.Name + "\n" + str(book.Page), file=discord.File(book.getPage(book.Page)))
            await reaction.message.delete()
            await msg.add_reaction("⬅")
            await msg.add_reaction("➡")

        elif reaction.emoji == "➡":
            book = DNDTracker.Book("DND/Book/" + reaction.message.content.splitlines()[0] + ".txt")
            book.setPage(int(reaction.message.content.splitlines()[1]))
            book.flipPage()
            msg = await reaction.message.channel.send(book.Name + "\n" + str(book.Page), file=discord.File(book.getPage(book.Page)))
            await reaction.message.delete()
            await msg.add_reaction("⬅")
            await msg.add_reaction("➡")


@bot.event
async def on_raw_reaction_add(payload):
    # Auto Roles
    member = Guild.get_member(payload.user_id)
    if payload.message_id == 558748934449922058:  # Red
        await removeAllColors(member)
        await addrole(member, 541787005630152714, "User requested role")
        await member.send("You are now Red! Huzzah!")
    if payload.message_id == 558749272976261120:  # Pink
        await removeAllColors(member)
        await addrole(member, 546993546259988490, "User requested role")
        await member.send("You are now Pink! Yes, you are beautiful!")
    if payload.message_id == 558749287945601026:  # Dark Red
        await removeAllColors(member)
        await addrole(member, 544011780243062803, "User requested role")
        await member.send("You are now Dark Red! Pretty cool, huh?")
    if payload.message_id == 558749329871863808:  # Orange
        await removeAllColors(member)
        await addrole(member, 541787056410591328, "User requested role")
        await member.send("You are now Orange! Now you can pretend to be an... orange!")
    if payload.message_id == 558749365896740878:  # Beige
        await removeAllColors(member)
        await addrole(member, 550101190579585024, "User requested role")
        await member.send("You are now Beige! Like... That is a color...")
    if payload.message_id == 558749379243278336:  # Yellow
        await removeAllColors(member)
        await addrole(member, 546761442053980160, "User requested role")
        await member.send("You are now Yellow! Bright like the sun!")
    if payload.message_id == 558749399145250826 or payload.message_id == 558779664395534346:  # Poop Yellow
        await removeAllColors(member)
        await addrole(member, 541787107354607617, "User requested role")
        await member.send("You are now Poop Yellow! Why did you choose this color?")
    if payload.message_id == 558749438659657748:  # Green
        await removeAllColors(member)
        await addrole(member, 541787118398078993, "User requested role")
        await member.send("You are now Green! Like the grass")
    if payload.message_id == 558749458238668825:  # Lt Blue
        await removeAllColors(member)
        await addrole(member, 558188429398114304, "User requested role")
        await member.send("You are now Light Blue! A pretty blue sky")
    if payload.message_id == 558749511929823233:  # Blue
        await removeAllColors(member)
        await addrole(member, 541787112815460364, "User requested role")
        await member.send("You are now Blue! My favorite color! Also, the color of Aaron's eyes.")
    if payload.message_id == 558749527415193672:  # Blue Blue
        await removeAllColors(member)
        await addrole(member, 544365366374039572, "User requested role")
        await member.send("You are now Blue Blue! Great! Now you hurt emerson's eyes!")
    if payload.message_id == 558749539897704468:  # Dark Blue
        await removeAllColors(member)
        await addrole(member, 544009636723032074, "User requested role")
        await member.send("You are now Dark Blue! How cool!")
    if payload.message_id == 558749595576958976:  # Purple
        await removeAllColors(member)
        await addrole(member, 541787119144796170, "User requested role")
        await member.send("You are now Purple! Beautiful!")
    if payload.message_id == 558749610223599626:  # Dark Purple
        await removeAllColors(member)
        await addrole(member, 544203447831101442, "User requested role")
        await member.send("You are now Dark Purple! Shadowy energy flows through you.")
    if payload.message_id == 558749652594458624:  # White
        await removeAllColors(member)
        await addrole(member, 549403269710217216, "User requested role")
        await member.send("You are now White! Yay white people!")
    if payload.message_id == 558749665882013706:  # Lt Gray
        await removeAllColors(member)
        await addrole(member, 558100738861957134, "User requested role")
        await member.send("You are now Light Gray! Amazing!")
    if payload.message_id == 558749678359937194:  # Gray
        await removeAllColors(member)
        await addrole(member, 549381568511082498, "User requested role")
        await member.send("You are now Gray! Your welcome...")
    if payload.message_id == 558749724920905746:  # Black
        await removeAllColors(member)
        await addrole(member, 547984696324128787, "User requested role")
        await member.send("You are now Black! Edge lord I see...")

    if payload.message_id == 558749792545669130:  # Youtuber
        if checkrole(member, 544624694607740968):
            await removerole(member, 544624694607740968, "User requested role removal")
            await member.send("You removed the Youtuber role!")
        else:
            await addrole(member, 544624694607740968, "User requested role addition")
            await member.send("You added the Youtuber role!")
    if payload.message_id == 558749802641358848:  # Twitch Streamer
        if checkrole(member, 544624779341070336):
            await removerole(member, 544624779341070336, "User requested role removal")
            await member.send("You removed the Twitch Streamer role!")
        else:
            await addrole(member, 544624779341070336, "User requested role addition")
            await member.send("You added the Twitch Streamer role!\nWhen you go live, you will be given a streaming role + a shout out in the Livestreams channel")
    if payload.message_id == 558749852977201163:  # VRChat
        if checkrole(member, 541407696369483808):
            await removerole(member, 541407696369483808, "User requested role removal")
            await member.send("You removed the VRChat role!")
        else:
            await addrole(member, 541407696369483808, "User requested role addition")
            await member.send("You added the VRChat role!\nAaron: Hope to see you in VRChat! My username is Aaron13ps")
    if payload.message_id == 558749863421149190:  # SCP - Universe
        if checkrole(member, 544642579745210377):
            await removerole(member, 544642579745210377, "User requested role removal")
            await member.send("You removed the SCP role!")
        else:
            await addrole(member, 544642579745210377, "User requested role addition")
            await member.send("Welcome, C-"+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+" to site-41 Containment Facility")
    if payload.message_id == 558749926822248448:  # Overwatch
        if checkrole(member, 544642953746841600):
            await removerole(member, 544642953746841600, "User requested role removal")
            await member.send("You removed the Overwatch role!")
        else:
            await addrole(member, 544642953746841600, "User requested role addition")
            await member.send("You are now a Hero of Overwatch!")
    if payload.message_id == 558749940617183233:  # Mercinary
        if checkrole(member, 544642682421510176):
            await removerole(member, 544642682421510176, "User requested role removal")
            await member.send("You removed the Mercenary role!")
        else:
            await addrole(member, 544642682421510176, "User requested role addition")
            await member.send("Announcer: Prepare to capture the control point!")
    if payload.message_id == 558749990739247105:  # Slug - Cat
        if checkrole(member, 556824719656222720):
            await removerole(member, 556824719656222720, "User requested role removal")
            await member.send("You removed the Slug-Cat role!")
        else:
            await addrole(member, 556824719656222720, "User requested role addition")
            await member.send("You are now a slug cat! ^ - ^")
    if payload.message_id == 558750004345438209:  # Minecraft
        if checkrole(member, 544642742165307401):
            await removerole(member, 544642742165307401, "User requested role removal")
            await member.send("You removed the Minecraft role!")
        else:
            await addrole(member, 544642742165307401, "User requested role addition")
            await member.send("You are now a child again...")
    if payload.message_id == 558750016630423552:  # Programmer
        if checkrole(member, 541494641761976323):
            await removerole(member, 541494641761976323, "User requested role removal")
            await member.send("You removed the Programmer role!")
        else:
            await addrole(member, 541494641761976323, "User requested role addition")
            await member.send("Welcome to an elite race of human beings")
    if payload.message_id == 558750072045830145:  # Digital Artist
        if checkrole(member, 541494757919162378):
            await removerole(member, 541494757919162378, "User requested role removal")
            await member.send("You removed the Digital Artist role!")
        else:
            await addrole(member, 541494757919162378, "User requested role addition")
            await member.send("You marked yourself as a Digital Artist")
    if payload.message_id == 558750082359492638:  # Physical Artist
        if checkrole(member, 541653277310451753):
            await removerole(member, 541653277310451753, "User requested role removal")
            await member.send("You removed the Physical Artist role!")
        else:
            await addrole(member, 541653277310451753, "User requested role addition")
            await member.send("You marked yourself as a Physical Artist!")
    if payload.message_id == 558750143760039956:  # Story Teller
        if checkrole(member, 556739772664774672):
            await removerole(member, 556739772664774672, "User requested role removal")
            await member.send("You removed the Story Teller role!")
        else:
            await addrole(member, 556739772664774672, "User requested role addition")
            await member.send("Welcome, story teller! I can't wait to hear what you come up with!")
    if payload.message_id == 558750200785797150:  # Musician
        if checkrole(member, 546993626274594836):
            await removerole(member, 546993626274594836, "User requested role removal")
            await member.send("You removed the Musician role!")
        else:
            await addrole(member, 546993626274594836, "User requested role addition")
            await member.send("Ah, welcome. I love music!")
    if payload.message_id == 558750208708706325:  # Project Amaranth
        if checkrole(member, 541718745224052736):
            await removerole(member, 541718745224052736, "User requested role removal")
            await member.send("You removed the Project Amaranth role! v - v")
        else:
            await addrole(member, 541718745224052736, "User requested role addition")
            await member.send("You added the Project Amaranth role! ^ - ^")
    if payload.message_id == 558750299058077696:  # DnD
        if checkrole(member, 546759015380680714):
            await removerole(member, 546759015380680714, "User requested role removal")
            await member.send("You removed the DnD role!")
        else:
            await addrole(member, 546759015380680714, "User requested role addition")
            await member.send("You added the DnD role!\nThere is an entire section for this!")
    if payload.message_id == 558750313071247390:  # RP
        if checkrole(member, 556824721208115201):
            await removerole(member, 556824721208115201, "User requested role removal")
            await member.send("You removed the RP role!")
        else:
            await addrole(member, 556824721208115201, "User requested role addition")
            await member.send("*The RP role was placed upon you*")
    if payload.message_id == 593321525558378497:  # Artificial Realms RPG
        if checkrole(member, 593320845485539350):
            await removerole(member, 593320845485539350, "User requested role removal")
            await member.send("You removed the Super Smash Bros role!")
        else:
            await addrole(member, 593320845485539350, "User requested role addition")
            await member.send("Let's get Smashin! My friend code is 0943-3398-1987 for smash ultimate.")
    if payload.message_id == 669786005133459477:  # Youtube Subscriber
        if checkrole(member, 669785526999580676):
            await removerole(member, 669785526999580676, "User requested role removal")
            await member.send("You removed the Youtube Subscriber role!")
        else:
            await addrole(member, 669785526999580676, "User requested role addition")
            await member.send("Thanks for Subscribing via Discord! All videos will be posted in the #videos channel.")


    if payload.message_id == 563407872755761175:
        # channel =  Guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(563407872755761175)
        # await message.clear_reactions()
        # await message.add_reaction("✅")
        hub = GameHandler.GameHub(member.id)
        if hub.Money >= 100 and not checkrole(member, 560601128253915154):
            hub.setMoney(hub.Money - 100)
            await addrole(member, 560601128253915154, "User bought it")

            await member.send("You now have the Hidden Role ^ - ^")
            msg = await Guild.get_channel(563407635093782539).send("<@"+str(member.id)+"> bought the Hidden Viewer tag!")
            await delete_delay(msg, 3600)

    if payload.message_id == 563408536999297037:
        # channel =  Guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(563407872755761175)
        # await message.clear_reactions()
        # await message.add_reaction("✅")
        hub = GameHandler.GameHub(member.id)
        if hub.Money >= 10:
            hub.setMoney(hub.Money - 10)
            at = ServerAge.ActivityTracker(member.id)
            at.setPoints(at.GetPoints + 100)
            msg = await Guild.get_channel(563407635093782539).send("<@"+str(member.id)+"> bought 100 activity points!")
            await delete_delay(msg, 3600)

    if payload.message_id == 563408746404118528:
        # channel =  Guild.get_channel(payload.channel_id)
        # message = await channel.fetch_message(563408536999297037)
        # await message.clear_reactions()
        # await message.add_reaction("✅")
        hub = GameHandler.GameHub(member.id)
        if hub.Money >= 100:
            hub.setMoney(hub.Money - 100)
            at = ServerAge.ActivityTracker(member.id)
            at.addMultiplicative()
            await member.send("You bought a dampener!\nDampener is now at level " + str(at.Multiplier) + " and lasts for " + str(at.StopTime - int(time.time())))
            msg = await Guild.get_channel(563407635093782539).send("<@"+str(member.id)+"> bought bought an Activity Decay Dampener! (x" + str(at.Multiplier) + ")")
            await delete_delay(msg, 3600)

    if payload.emoji.name == "deleteMessage":
        if member.id == 110858000192798720 or checkrole(member, 541691815997341696) or checkrole(member, 554828228460806144) or checkrole(member, 541691951377022996):
            msg = await Guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
            content = msg.content
            await Guild.get_channel(564958003368034365).send("<@"+str(member.id)+"> deleted a message in <#" + str(msg.channel.id) + "> by <@" + str(msg.author.id) + ">: ```" + content + "```")
            await msg.delete()

    lines = SaveSystem.Data("Smoke.txt").loadFile(5)
    smokeTime = int(lines[0])
    smokeAmount = int(lines[1])
    smokeMessageID = int(lines[2])
    totalAmount = int(lines[3])
    daysPassed = int(lines[4])

    if not member.bot and payload.message_id == smokeMessageID and payload.emoji.name == "🚬":
        smokeAmount += 1
        totalAmount += 1
        msg = await Guild.get_channel(674532364961185792).fetch_message(smokeMessageID)
        await msg.edit(content="<@319876025410519041>, you have smoked **" + str(smokeAmount) + "** times today" + ("!" if smokeAmount >= 4 else "."))
        SaveSystem.Data("Smoke.txt").saveData([int(smokeTime), smokeAmount, smokeMessageID, totalAmount, daysPassed])
        await msg.remove_reaction(payload.emoji, member)


@bot.command(pass_context = True)
async def nothing(ctx):
    """Does Absolutely Nothing, trust me"""
    await ctx.message.delete()

@bot.command(pass_context = True)
async def dnd(ctx, *args):
    global Guild
    global dndObject
    if not(ctx.message.channel.category.id == 546759983191294012):
        msg = await ctx.channel.send("Please post all DND related messages in the DND chat")
        await delete_delay(ctx.message, 10)
        await msg.delete()
        return True

    switchCommand = ['s', 'switch', 'changecampaign', 'modifycampaign']

    if args[0].lower() in switchCommand:
        channel = ctx.channel
        author = ctx.author

        if len(args) < 2:
            msg = await channel.send("You are missing some arguments. Try `!dnd help switch`\nPlease provide the campaign to switch to")
            await delete_delay(msg, 10)
            return True

        checkDir("DND")
        checkDir("DND/CurrentGame")
        filePath = "DND/CurrentGame/" + str(author.id) + ".txt"
        if not os.path.isfile(filePath):
            fileInitialize(filePath, "0", 10)
            '''
            0 Game ID
            '''

        lines = open(filePath, encoding='utf-8').read().splitlines()

        campaign = int(args[1])
        if campaign >= 3 or campaign < 0:
            msg = await channel.send("Invalid Campaign")
            await delete_delay(msg, 10)
            return True

        lines[0] = str(campaign)

        campaignName = "Hoard of the Dragon Queen"
        if campaign == 1:
            campaignName = "Surviving the Biogrid"
        if campaign == 2:
            campaignName = "Side Quest"
        f = open(filePath, 'w')
        for i in range(len(lines)):
            f.write(lines[i] + "\n")
        f.close()

        msg = await channel.send("Switch to new campaign: " + campaignName)
        await delete_delay(msg, 10)
        return True

    checkDir("DND")
    checkDir("DND/CurrentGame")
    filePath = "DND/CurrentGame/" + str(ctx.author.id) + ".txt"
    if not os.path.isfile(filePath):
        fileInitialize(filePath, "0", 10)
        '''
        0 Game ID
        '''
    lines = open(filePath, encoding='utf-8').read().splitlines()
    campaign = int(lines[0])
    try:
        permissions = 0
        if checkrole(ctx.message.author, 546759015380680714):  # DND
            permissions = 1
        if checkrole(ctx.message.author, 546759734808674334):  # Spectator
            permissions = 2
        if checkrole(ctx.message.author, 546759670686285824):  # Player
            permissions = 3
        if checkrole(ctx.message.author, 547893849398312999):  # Player Area 1
            permissions = 10
        if checkrole(ctx.message.author, 547893960132132874):  # Player Area 2
            permissions = 11
        if checkrole(ctx.message.author, 547894061743341568):  # Player Area 3
            permissions = 12
        if checkrole(ctx.message.author, 547894116416094208):  # Player Area 4
            permissions = 13
        if checkrole(ctx.message.author, 546759592273772567):  # Dungeon Master
            permissions = 100
        if permissions <= 0:
            msg = await ctx.channel.send("You do not have permission to use this command")
            await delete_delay(ctx.message, 10)
            await msg.delete()
            return
        delete = await dndObject[campaign].passArguments(bot, ctx.message.author, ctx.channel, permissions, args, ctx.message.content)
        if delete:
            await ctx.message.delete()
    except:
        await ctx.channel.send("An unknown error occurred when calling that command")

@bot.command(pass_context = True)
async def say(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:
        await Guild.get_channel(int(args[0])).send(" ".join(args[1:]))

@bot.command(pass_context = True)
async def sayrepeat(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:
        for i in range(int(args[1])):
            await Guild.get_channel(int(args[0])).send(" ".join(args[2:]))

@bot.command(pass_context = True)
async def saytts(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:
        await Guild.get_channel(int(args[0])).send(" ".join(args[1:]), tts=True)

@bot.command(pass_context=True)
async def reboot(ctx):
    """Restarts the bot"""
    if ctx.message.author.id == 110858000192798720:
        await ctx.channel.send("Restarting")
        await bot.logout()

@bot.command(pass_context=True)
async def convertToBook(ctx):
    """Converts your text to book text"""
    Str = ctx.message.content[15:]
    newStr = ""
    backPos = 0
    frontPosPrev = 0
    frontPos = 0
    length = len(Str)
    while(frontPos < length):
        if Str[frontPos] == " ":
            if len(Str[backPos:frontPos]) > 43:
                newStr += Str[backPos:frontPosPrev] + "  ▌\n"
                frontPos = frontPosPrev + 1
                backPos = frontPos
            frontPosPrev = frontPos
        frontPos += 1
    newStr += Str[backPos:length-1] + "  ▌\n"

    await ctx.channel.send(newStr)

@bot.command(pass_context=True)
async def createvote(ctx, *args):
    if checkrole(ctx.author, 541665834695655454):  # Member
        if len(args) >= 1:
            msg = await ctx.channel.fetch_message(int(args[0]))
            try:
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                await ctx.message.delete()
            except discord.Forbidden:
                msg = await ctx.channel.send("Failed to add reaction. Forbidden.")
                await delete_delay(msg, 10)
                await ctx.message.delete()

@bot.command(pass_content=True)
async def game(ctx, *args):
    hub = GameHandler.GameHub(ctx.author.id)
    if ctx.channel.id == 554430142655496202:  # Game Hub
        if len(args) < 1 or args[0].lower() in ['c', 'cat', 'catalogue', 'catalog' 'catalogu', 'cataloge', 'game', 'gamelist', 'list', 'check']:
            await hub.showCatalogue(ctx.channel)
        elif args[0].lower() in ['d', 'cl', 'claim', 'clai', 'donation', 'don', 'donat', 'donate']:
            await hub.claim(ctx.channel)
        elif args[0].lower() in ['t', 'ti', 'time', 'check', 'timecheck', 'checktime', 'ch', 'left', 'timeleft']:
            await hub.timeCheck(ctx.channel)
        elif args[0].lower() in ['b', 'buy', 'get', 'buygame', 'getgame']:
            if len(args) < 2:
                await ctx.channel.send("Please provide the letter of the game you want to buy!\nExample: !game buy g")
            else:
                roleID = await hub.buy(ctx.channel, args[1])

                if roleID != -1:
                    await addrole(ctx.message.author, roleID, "User bought this game!")
        elif args[0].lower() in ['m', 'money', 'checkmoney', 'balance', 'coins']:
            await ctx.channel.send("You currently have " + str(hub.Money) + " coins!")
        elif args[0].lower() in ['g', 'give', 'giveto']:
            if int(args[1]) > 0:
                if len(ctx.message.mentions) == 1:
                    mentionID = (ctx.message.mentions[0]).id
                    if hub.giveMoney(int(args[1]), mentionID):
                        await ctx.channel.send("You gave " + args[1] + " coins to <@"+str(mentionID)+">")
                    else:
                        await ctx.channel.send("Action failed, not enough coins.")
                else:
                    if hub.giveMoney(int(args[1]), int(args[2])):
                        await ctx.channel.send("You gave " + args[1] + " coins to <@"+args[2]+">")
                    else:
                        await ctx.channel.send("Action failed, not enough coins.")
            else:
                await ctx.channel.send("Sorry, you can not steal from people anymore...")
    elif ctx.channel.id == 563396120102043649:  # Amaranth Bank
        AB = GameHandler.AmaranthBank(ctx.author.id)
        if len(args) < 1:
            await ctx.channel.send(AB.Summary)
        if len(args) >= 2:
            if args[0].lower() in ['deposit']:
                amount = int(args[1])
                if amount > hub.Money:
                    await ctx.channel.send("You do not have enough money!")
                else:
                    returnVal = AB.deposit(amount)
                    if returnVal == 0:
                        hub.setMoney(hub.Money - amount)
                        await ctx.channel.send("You deposited " + str(amount) + " coins!\nYou now have " + str(AB.Money) + " coins in the bank and have " + str(hub.Money) + " coins on you")
                    elif returnVal == 1:
                        await ctx.channel.send("You can not input number less than or equal to 0.")
                    elif returnVal == 2:
                        await ctx.channel.send("You have reached the max limit of amount of coins that can be stored in the bank!")
            if args[0].lower() in ['withdraw', 'withdrawal']:
                amount = int(args[1])
                if amount > AB.Money:
                    await ctx.channel.send("You do not have enough money in the bank!")
                else:
                    returnVal = AB.withdraw(amount)
                    if returnVal == 0:
                        hub.setMoney(hub.Money + amount)
                        await ctx.channel.send("You withdrew " + str(amount) + " coins!\nYou now have " + str(AB.Money) + " coins in the bank and have " + str(hub.Money) + " coins on you")
                    elif returnVal == 1:
                        await ctx.channel.send("You can not input number less than or equal to 0.")
                    elif returnVal == 2:
                        await ctx.channel.send("You can not withdraw more than you have in the bank.")
                    elif returnVal == 3:
                        await ctx.channel.send("Sorry, the bank does not have enough money to pay you")
            if args[0].lower() in ['loan', 'getloan']:
                amount = int(args[1])
                if amount > AB.getMoneyInBank():
                    await ctx.channel.send("The bank does not have enough money to loan you!")
                elif hub.Money <= 0:
                    await ctx.channel.send("Sorry, the bank does not trust you enough to give you money!")
                else:
                    returnVal = AB.getLoan(amount)
                    if returnVal == 0:
                        hub.setMoney(hub.Money + amount)
                        await ctx.channel.send("You got a loan of " + str(amount) + " coins!\nYou now owe " + str(AB.LoanDue) + " coins to the bank and have " + str(hub.Money) + " coins on you")
                    elif returnVal == 2:
                        await ctx.channel.send("You can not request less than or equal to 0 coins")

            if args[0].lower() in ['pay', 'payloan']:
                amount = int(args[1])
                if amount > AB.LoanDue:
                    await ctx.channel.send("You are overpaying!")
                elif hub.Money < amount:
                    await ctx.channel.send("Sorry, you do not have enough money!")
                else:
                    returnVal = AB.payLoan(amount)
                    if returnVal == 0:
                        hub.setMoney(hub.Money - amount)
                        await ctx.channel.send("You payed " + str(amount) + " coins towards your loan!\nYou now owe " + str(AB.LoanDue) + " coins to the bank and have " + str(hub.Money) + " coins on you")
                    elif returnVal == 2:
                        await ctx.channel.send("You can not pay less than or equal to 0 coins")

    elif ctx.channel.id == 554431493770838026:  # Farm Simulator
        farm = GameHandler.FarmSimulator(ctx.author.id)
        if len(args) < 1:
            await ctx.channel.send(farm.Summary)
        if len(args) >= 1:
            if args[0].lower() in ['land', 'buyland']:
                if hub.Money >= farm.LandCost:
                    farm.buyLand(farm.TotalLand, 1)
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you bought some basic land!")
                    hub.setMoney(hub.Money - farm.LandCost)
                else:
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you do not have enough money for that!")
        if len(args) >= 2:
            if args[0].lower() in ['crop', 'buycrop']:
                if int(args[1]) <= 0 or int(args[1]) > farm.TotalLand:
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you can not buy crops on land that does not exist!")
                elif hub.Money >= farm.CropCost:
                    farm.buyCrops(int(args[1])-1, 1)
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you bought some basic crops!")
                    hub.setMoney(hub.Money - farm.CropCost)
                else:
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you do not have enough money for that!")
            if args[0].lower() in ['water', 'watercrops']:
                if int(args[1]) <= 0 or int(args[1]) > farm.TotalLand:
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you can not water crops on land that does not exist!")
                elif hub.Money >= farm.WaterCost:
                    farm.waterCrops(int(args[1])-1)
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you watered your crops!")
                    hub.setMoney(hub.Money - farm.WaterCost)
                    land = farm.getLand(int(args[1])-1)
                    if land[3] >= 10:
                        await ctx.channel.send("<@" + str(ctx.author.id) + ">, your crops are glistening!")
                else:
                    await ctx.channel.send("<@"+str(ctx.author.id)+">, you do not have enough money for that!")
            if args[0].lower() in ['sell', 'sellcrops']:
                if int(args[1]) <= 0 or int(args[1]) > farm.TotalLand:
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you can not sell crops on land that does not exist!")
                elif hub.Money >= farm.WaterCost:
                    profit = farm.sellCrops(int(args[0])-1)
                    await ctx.channel.send("<@" + str(ctx.author.id) + ">, you sold crops for " + str(profit) + " coins!")
                    hub.setMoney(hub.Money + profit)
    elif ctx.channel.id == 554430280090386432:  # Guess the Number
        if hub.Money < 5:
            await ctx.channel.send("Sorry <@"+str(ctx.author.id)+">, you do not have 5 coins")
        else:
            hub.setMoney(hub.Money-5)
            guess = int(args[0])
            ggame = GameHandler.GuessTheNumber()
            messageToSend = ggame.makeGuess(guess)
            if len(messageToSend) > 20:
                hub.setMoney(hub.Money+55)
                messageToSend += "\nYou won 55 Coins!"
            await ctx.channel.send(messageToSend)
    elif ctx.channel.id == 554430335442616359:  # Tic-Tac-Toe
        ttt = GameHandler.TicTacToe(ctx.author.id)
        if len(args) == 2:
            if args[0].lower() in ["play", "invite", "start", "join"]:
                if hub.Money < 10:
                    await ctx.channel.send("Sorry <@" + str(ctx.author.id) + ">, you do not have 10 coins")
                else:
                    returnVal = ttt.startGame((ctx.message.mentions[0]).id)
                    if returnVal == 2:
                        hub.setMoney(hub.Money - 10)
                        await ctx.channel.send("Waiting for oponents response")
                    elif returnVal == 4:
                        await ctx.channel.send("You already sent a request!")
                    elif returnVal == 3:
                        hub.setMoney(hub.Money - 10)
                        await ctx.channel.send(ttt.Board)
        if len(args) == 3:
            if args[0].lower() in ["place"]:
                result = ttt.placePiece(int(args[1]), int(args[2]))
                if result == 3:
                    await ctx.channel.send("<@"+str(ctx.author.id)+"> wins!\nYou won 20 coins!")
                    hub.setMoney(hub.Money + 20)
                elif result == 4:
                    await ctx.channel.send("No one won!\nYou each get your 10 coins back.")
                    hub.setMoney(hub.Money + 10)
                    otherHub = GameHandler.GameHub(ttt.Opponent)
                    otherHub.setMoney(otherHub.Money + 10)
                elif result == 5:
                    await ctx.channel.send("It is not your turn")
                elif result == 6:
                    await ctx.channel.send("Other person has not confirmed!")
                else:
                    await ctx.channel.send(ttt.Board)
    else:
        msg = await ctx.channel.send("Please only post these in <#554430142655496202>")
        await delete_delay(ctx.message, 20)
        await delete_delay(msg, 1)

    serverMonetaryStatus = GameHandler.MonitaryTracker(ctx.author.id, hub.Money)
    roles = ctx.author.roles
    for r in range(len(roles)):
        if not isinstance(roles[r], int):
            roles[r] = roles[r].id
    if serverMonetaryStatus.needsRoleChange(roles):
        await removerole(ctx.author, serverMonetaryStatus.CurrentRole, "Auto Activity Role Changer")
        serverMonetaryStatus.updateRole()
        await addrole(ctx.author, serverMonetaryStatus.CurrentRole, "Auto Activity Role Changer")

@bot.command(pass_content=True)
async def getActivityPoints(ctx):
    serverActivity = ServerAge.ActivityTracker(ctx.author.id)
    await ctx.channel.send("Your current point value: " + str(serverActivity.GetPoints))

@bot.command(pass_content=True)
async def editAI(ctx, *args):
    if ctx.author.id == 110858000192798720:  # Aaron
        global AutoResponse
        filePath = "Personality/Data.txt"
        lines = open(filePath, encoding='utf-8').read().splitlines()

        if len(args) >= 2:
            if args[0].lower() in ["a", "auto", "autoresponse", "response"]:
                if args[1].lower() in ['1', 'one', 'on']:
                    lines[0] = "1"
                    AutoResponse = 1
                    await ctx.channel.send("Turned auto-resonses on")
                elif args[1].lower() in ['0', 'zero', 'off']:
                    lines[0] = "0"
                    AutoResponse = 0
                    await ctx.channel.send("Turned auto-responses off")

        f = open(filePath, 'w')
        for i in range(len(lines)):
            f.write(lines[i] + "\n")
        f.close()

@bot.command(pass_content=True)
async def hell(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:  # Aaron
        member = Guild.get_member(int(args[0]))
        await ctx.channel.send("<@" + str(member.id) + "> is now in hell")

        while(random.randint(0, 100) != 0):
            if random.randint(0, 3) == 0:
                channel = Guild.get_channel(544624213118681088)
                await channel.send("<@"+ str(member.id) + "> is currently in hell!")
            if random.randint(0, 3) == 0:
                channel = Guild.get_channel(544624213118681088)
                await channel.send("Welcome to hell, <@" + str(member.id) + "> ;)")
            if random.randint(0, 3) == 0:
                await member.send("You are in hell! Muwahahahaha")
            whichOne = random.randint(0, 10)
            voiceChannels = [563616007789346826, 560808536624594973, 544010529518387203, 544010556433235971, 544010687358173194,
                             544010602788421632, 544010854690193408, 544010882238251040, 544011038077747202, 563136668316729404, 546767608758927401,
                             548898527003017227]
            await member.move_to(Guild.get_channel(voiceChannels[whichOne]))
        channel = Guild.get_channel(544624213118681088)
        await channel.send("<@" + str(member.id) + "> is no longer in hell!")

@bot.command(pass_content=True)
async def halfsum(ctx, *args):
    await ctx.channel.send(str(halfSum(int(args[0]), 1)))

@bot.command(pass_content=True)
async def sayBigLetters(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:  # Aaron
        msg = " ".join(args[1:])
        newmsg = ""
        for c in range(len(msg)):
            if msg[c].lower() == 'a':
                newmsg += ":regional_indicator_a:"
            elif msg[c].lower() == 'b':
                newmsg += ":regional_indicator_b:"
            elif msg[c].lower() == 'c':
                newmsg += ":regional_indicator_c:"
            elif msg[c].lower() == 'd':
                newmsg += ":regional_indicator_d:"
            elif msg[c].lower() == 'e':
                newmsg += ":regional_indicator_e:"
            elif msg[c].lower() == 'f':
                newmsg += ":regional_indicator_f:"
            elif msg[c].lower() == 'g':
                newmsg += ":regional_indicator_g:"
            elif msg[c].lower() == 'h':
                newmsg += ":regional_indicator_h:"
            elif msg[c].lower() == 'i':
                newmsg += ":regional_indicator_i:"
            elif msg[c].lower() == 'j':
                newmsg += ":regional_indicator_j:"
            elif msg[c].lower() == 'k':
                newmsg += ":regional_indicator_k:"
            elif msg[c].lower() == 'l':
                newmsg += ":regional_indicator_l:"
            elif msg[c].lower() == 'm':
                newmsg += ":regional_indicator_m:"
            elif msg[c].lower() == 'n':
                newmsg += ":regional_indicator_n:"
            elif msg[c].lower() == 'o':
                newmsg += ":regional_indicator_o:"
            elif msg[c].lower() == 'p':
                newmsg += ":regional_indicator_p:"
            elif msg[c].lower() == 'q':
                newmsg += ":regional_indicator_q:"
            elif msg[c].lower() == 'r':
                newmsg += ":regional_indicator_r:"
            elif msg[c].lower() == 's':
                newmsg += ":regional_indicator_s:"
            elif msg[c].lower() == 't':
                newmsg += ":regional_indicator_t:"
            elif msg[c].lower() == 'u':
                newmsg += ":regional_indicator_u:"
            elif msg[c].lower() == 'v':
                newmsg += ":regional_indicator_v:"
            elif msg[c].lower() == 'w':
                newmsg += ":regional_indicator_w:"
            elif msg[c].lower() == 'x':
                newmsg += ":regional_indicator_x:"
            elif msg[c].lower() == 'y':
                newmsg += ":regional_indicator_y:"
            elif msg[c].lower() == '0':
                newmsg += ":zero:"
            elif msg[c].lower() == '1':
                newmsg += ":one:"
            elif msg[c].lower() == '2':
                newmsg += ":two:"
            elif msg[c].lower() == '3':
                newmsg += ":three:"
            elif msg[c].lower() == '4':
                newmsg += ":four:"
            elif msg[c].lower() == '5':
                newmsg += ":five:"
            elif msg[c].lower() == '6':
                newmsg += ":six:"
            elif msg[c].lower() == '7':
                newmsg += ":seven:"
            elif msg[c].lower() == '8':
                newmsg += ":eight:"
            elif msg[c].lower() == '9':
                newmsg += ":nine:"
            elif msg[c].lower() == ' ':
                newmsg += ":heavy_minus_sign:"
            elif msg[c].lower() == '!':
                newmsg += ":grey_exclamation:"
            elif msg[c].lower() == '?':
                newmsg += ":grey_question:"
            else:
                newmsg += msg[c]
        await Guild.get_channel(int(args[0])).send(newmsg)

@bot.command(pass_content=True)
async def joinvoice(ctx, *args):
    global Guild
    if len(args) <= 0:
        if ctx.channel.id == 571039046063882270:  # Friend Den
            await ctx.author.move_to(Guild.get_channel(565626436849893379))
        if ctx.channel.id == 571039065646956554:  # Global Speaker
            await ctx.author.move_to(Guild.get_channel(565624762957824021))
        if ctx.channel.id == 571038968133451879:  # Roarin Space
            await ctx.author.move_to(Guild.get_channel(563616007789346826))
        if ctx.channel.id == 571038882351546369:  # Hangout
            await ctx.author.move_to(Guild.get_channel(560808536624594973))
        if ctx.channel.id == 544012301158580256:  # General
            await ctx.author.move_to(Guild.get_channel(544010529518387203))
        if ctx.channel.id == 544012368087351307:  # General 2
            await ctx.author.move_to(Guild.get_channel(544010556433235971))
        if ctx.channel.id == 544012982716203018:  # Personal
            await ctx.author.move_to(Guild.get_channel(544010687358173194))
        if ctx.channel.id == 544013073560764436:  # Small
            await ctx.author.move_to(Guild.get_channel(544010602788421632))
        if ctx.channel.id == 544013160080736266:  # Medium
            await ctx.author.move_to(Guild.get_channel(544010854690193408))
        if ctx.channel.id == 544013179521335321:  # Large
            await ctx.author.move_to(Guild.get_channel(544010882238251040))
        if ctx.channel.id == 544013203646971914:  # Music Room
            await ctx.author.move_to(Guild.get_channel(544011038077747202))
        if ctx.channel.id == 563971681866088450:  # Twitch Stream
            await ctx.author.move_to(Guild.get_channel(563971598542176266))
        if ctx.channel.id == 560825265434132490:  # Sleepy Peeps
            await ctx.author.move_to(Guild.get_channel(560805691955347456))
        if ctx.channel.id == 571038806749478939:  # Besties
            await ctx.author.move_to(Guild.get_channel(566742920846114816))
        if ctx.channel.id == 571038681348177921:  # Theater
            await ctx.author.move_to(Guild.get_channel(571038636745818156))
        if ctx.channel.id == 565570374083805195:  # Chill Zone
            await ctx.author.move_to(Guild.get_channel(563136668316729404))
        if ctx.channel.id == 571039187877363754:  # Game Chat
            await ctx.author.move_to(Guild.get_channel(546767608758927401))
        if ctx.channel.id == 571039216935632897:  # Outside of Game
            await ctx.author.move_to(Guild.get_channel(548898527003017227))
    else:
        await ctx.author.move_to(Guild.get_channel(int(args[0])))

@bot.command(pass_content=True)
async def setMoney(ctx, *args):
    global Guild
    if ctx.author.id == 110858000192798720:  # Aaron
        hub = GameHandler.GameHub(int(args[0]))
        hub.setMoney(int(args[1]))
        await ctx.channel.send("Set <@" + str(args[0]) + ">'s account to " + str(args[1]) + " coins.")

@bot.command(pass_content=True)
async def videocall(ctx, *args):
    global Guild
    global voiceTotal
    global voiceChannels
    global voiceTextChannels
    global voiceRoles
    for i in range(0, voiceTotal):
        if ctx.channel.id == voiceTextChannels[i]:
            await ctx.channel.send("<@&" + str(voiceRoles[i]) + ">, click the following link to turn the current call into a video call:\n<https://www.discordapp.com/channels/537752716680888350/" + str(voiceChannels[i]) +">")

@bot.command(pass_content=True)
async def help(ctx, *args):
    # 0 = Channel (0 is every channel), 1 = [Command and Parameters], 2 = [Descriptions]
    global helpMenu

    await ctx.channel.send(Help.getContent(helpMenu, ctx.channel.id, ctx.channel.category_id, args))

@bot.command(pass_content=True)
async def ump(ctx, *args):
    try:
        fileURL = ctx.message.attachments[0].url
        print("File URL: " + str(fileURL))
        try:
            file = requests.get(fileURL)
            try:
                open("/home/aaron/root/MusicBot/config/autoplaylist.txt", 'w').write(str(file.content).replace("\\n","\n")[2:-1])
                await ctx.channel.send("Updated!")
            except:
                await ctx.channel.send("Error writing file")
        except:
            await ctx.channel.send("Error requesting file")
    except:
        await ctx.channel.send("Error processing file. File might not be found")


Token.runBot(bot)


























