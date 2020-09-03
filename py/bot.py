#BOT CREATED BY NeKro
#Version 0.7.8

#######################################################################################################################################################################################################################################################################
Token="enter here the token of your bot"
#######################################################################################################################################################################################################################################################################

#START

import discord
from discord.ext import commands, tasks
import random
import youtube_dl
import asyncio




bot = commands.Bot(command_prefix = "!", description = "FREE ACCES IS THE KEY!")
musics = {}
ytdl = youtube_dl.YoutubeDL()
bot.remove_command('help')
bot.remove_command('start')




@bot.event
async def on_ready():
	print("Ready !")

#status

status = ["!help"]

@bot.event
async def on_ready():
	print("Ready !")
	changeStatus.start()

@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)


#WELCOME
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(746407943246708778)
    await channel.send(f'{member.mention} WELCOME!\nhave fun on this server :D')
#comands

###################################################
##########   HELP   ##############################
###################################################



#!help
@bot.command()
async def help(ctx):
	await ctx.send("**Wait,we work on it :wink: **")

#!invite
@bot.command()
async def invite(ctx):
	embed = discord.Embed(title="https://urlz.fr/dHe5", url = "https://urlz.fr/dHe5", description = "You can invite me with on your server with this link :D")
	embed.set_author(name="INVITATION")
	embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/746407135633473596/8a440678a9c87462d7c2a587b907ff15.png?size=64")
	await ctx.send(embed = embed)


###################################################
##########   FUN   ##############################
###################################################



#!credit

@bot.command()
async def credit(ctx):
	await ctx.send("**Creator :** @[TPB]NeKro#7781**\n\nDeveloper :** @[TPB]NeKro#7781 \n\n**Designer :** @[TPB]NeKro#7781")

#!serverInfo
@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"The server **{serverName}** have *{numberOfPerson}* members !  \nThis server have {numberOfTextChannels} text channel and {numberOfVoiceChannels} voc channel."
	await ctx.send(message)

#!say

@bot.command()
async def say (ctx, *texte):
	await ctx.send(" ".join(texte))

#!chinese
@bot.command()
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))


#!russian
@bot.command()
async def russian(ctx, *text):
	russianChar = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
	russianText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = russianChar[index]
				russianText.append(transformed)
			else:
				russianText.append(char)
		russianText.append(" ")
	await ctx.send("".join(russianText))


###################################################
##########   MUSIC   ##############################
###################################################

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

#!disc (disconnect)
@bot.command()
async def disc(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []



#!stop (pause)
@bot.command()
async def stop(ctx):
	client=ctx.guild.voice_client
	if not client.is_paused():
			client.pause()
	elif client.is_paused():
			client.resume()



		
#!skip
@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

#play music on youtube
def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

#!play
@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Now playing : {video.url}")
        play_song(client, musics[ctx.guild], video)



###################################################
##########   ADMIN   ##############################
###################################################

#!addrole "rolename"
@bot.command()
async def addrole(ctx, *rolenames):
    
    role =  discord.utils.get(ctx.author.guild.roles, name=rolenames[0])
    await ctx.author.add_roles(role)
    await ctx.send(f"{ctx.author} was given {role}")

#!removerole_rolename
@bot.command()
async def removerole(ctx, *rolenames):
    
    role =  discord.utils.get(ctx.author.guild.roles, name=rolenames[0])
    await ctx.author.remove_roles(role)
    await ctx.send(f"{ctx.author} was removed {role}")


#!clear

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()



#!purge
@bot.command()
@commands.has_permissions(manage_messages = True)

async def purge(ctx):
	messages = await ctx.channel.history(limit = 1000000).flatten()
	for message in messages:
		await message.delete()

#!kick
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	embed = discord.Embed(title = "**KICK**", url = "https://discord.gg/EN9sv4d")
	embed.set_thumbnail(url = "https://media1.tenor.com/images/25715a5aea4f0c70057ede6e05a6472d/tenor.gif?itemid=13461094")
	embed.add_field(name = "Kicked Member", value = user.name, inline = True)
	embed.add_field(name = "Reason", value = reason, inline = True)
	embed.add_field(name = "Moderator", value = ctx.author.name, inline = True)
	await ctx.send(embed = embed)

#!ban
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	embed = discord.Embed(title = "**BANNED**", description = " **ENJOY :wink: **", url = "https://discord.gg/EN9sv4d")
	embed.set_thumbnail(url = "https://media1.tenor.com/images/d856e0e0055af0d726ed9e472a3e9737/tenor.gif?itemid=8540509")
	embed.add_field(name = "Ban Member", value = user.name, inline = True)
	embed.add_field(name = "Reason", value = reason, inline = True)
	embed.add_field(name = "Moderator", value = ctx.author.name, inline = True)
	await ctx.send(embed = embed)

#!unban

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} is now  unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"The user {user} is not ban")

#!warn

























bot.run(Token)
