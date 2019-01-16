#!/usr/bin/python
import discord
import asyncio
import urllib.request
import scraping
import datetime
import pytz
from random import randint
from bs4 import BeautifulSoup
from scraping import scraping
import time
import re
client = discord.Client()
voiceplayers = []
scraping = scraping()
hstimer = 0
list = []
async def loopR(client,list):
	await client.wait_until_ready()
	while not client.is_closed:
		start = time.time()
		listtmp = []
		listtmp.clear()
		breaki = ""
		try:
			with open('players.csv') as f:
				for line in f:
					var = await scraping.getPlayer(line)
					if var is not None:
						listtmp.append(var)
					else:
						print(var)
						breaki = None
						break
		except:
			print("lookingfailed")
			continue
		list.clear()
		list +=listtmp
		if breaki == "":
			list.sort(key=lambda x:x.rawxp,reverse=True)
			print("sorting")
		n = 1
		msg = ""
		tz = pytz.timezone('US/Eastern')
		prv = []
		if breaki =="":
			for i in list:
				if n==60:
					msg = msg+"**"+str(n)+".** "+i.name+" *"+format(i.rawxp,',d')+"*\n\n::"
				else:
					msg = msg+"**"+str(n)+".** "+i.name+" *"+format(i.rawxp,',d')+"*\n\n"
				n+=1
			msg = msg+"\n **Last updated:** "+str(datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))+" server time."
			
			if n < 60:
				ch = client.get_channel("487028563493650442") #getting messages
				mess = await client.get_message(ch,"512012058078871553")
				mess2 = await client.get_message(ch,"512012067033841686")
				await client.edit_message(mess2, ".")
				await client.edit_message(mess, msg)
			else:
				msgl = msg.split("::")
				try:
					ch = client.get_channel("487028563493650442") #getting messages
					mess = await client.get_message(ch,"512012058078871553")
					mess2 = await client.get_message(ch,"512012067033841686")
					await client.edit_message(mess, msgl[0])
					await client.edit_message(mess2, msgl[1])
				except:
					pass
			now = []
			n = 0
			for i in list:
				now.append(str(n+1)+";"+i.name)
				
				n+=1
			with open('previous.csv', 'r+') as f:
				for l in f:
					prv.append(l)
				f.seek(0)
				f.truncate()
				print("writing")
				for l in now:
					f.write(l+"\n")
			msg = ""
			newplayers = []
			removedplayers = []
			for s in prv:
				for l in now:
					reg = re.match(r'(.*);(.*)',s,re.M|re.I) #previous
					reg2 = re.match(r'(.*);(.*)',l,re.M|re.I) #new
					if reg.group(2) == reg2.group(2):
						if int(reg.group(1)) < int(reg2.group(1)):
							msg = msg+"\n**"+reg.group(2)+"** has fallen to "+reg2.group(1)
						elif int(reg.group(1)) > int(reg2.group(1)):
							msg = msg+"\n**"+reg.group(2)+"** has risen to "+reg2.group(1)
						else:
							continue
			else:
				if msg !="":
					try:
						await client.send_message(client.get_channel("487028563493650442"),msg)
					except:
						pass
				end = time.time()-start
				print(str(end))

		print("going to sleep")
		await asyncio.sleep(180)


@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name=';;skills to learn how to use skill calculator!'))
	for i in client.servers:
		for l in i.channels:
			print(l.name+" : "+l.id)

	print(discord.__version__)
	print("ready")

	
@client.event
async def on_member_join(member):
	role = discord.utils.get(member.server.roles,name="Recruit")
	await client.send_message(member,"""Please check out '#rules-and-ranks' We appreciate it.

We have a few benefits, which are exclusive only to our clan.

Firstly, completionists has appointed its very own events team. This team is in charge of sorting out events that will accomodate all members. Events are held weekly.

We also have a system called "clan bank," which is an account used to hold donated items from clan members. The items and cash are then distributed as rewards for events.

Donating to the clan bank account is not mandatory, but appreciated.

In addition, we have an experience tracker for clan members, located at; http://blissscrape.com/. This site converts all experienced gained to a 'prestige 0' rate to encourage fair competition. (Developed by Pyro)

Furthermore, we have our own calculator system for skilling, found in; '#bot-commands'. This will calculate amounts of supplies required for prestiging certain skills. (Developed by Kaolin)

One final thing, just enjoy your time with us and welcome to the completionist family.""")
	await client.add_roles(member, role)
@client.event
async def on_message(message):
	skills = ('prayer', 'crafting', 'agility', 'herblore',
	'thieving','woodcutting','firemaking','fishing',
	'cooking','fletching','mining','smithing',
	'construction','hunter','runecrafting','summoning',
	'farming')
	
	if message.content.startswith(";;"):
		if " " in message.content:
			print(len(list))
			xp = 200000000
			msgcontent = message.content.split(" ",1)
			skill = msgcontent[0].replace(";", "")
			player = ""
			if "-n" in msgcontent[1]:
				try:
					info = msgcontent[1].split("-n")
					player = info[0].strip()
					content = info[1].strip()
					if ('m' in info[1] )or ('k' in info[1]):
						print("hi")
						content = re.sub(r"[k]","000",info[1], flags=re.IGNORECASE)
						content = re.sub(r"[m]","000000",content, flags=re.IGNORECASE)
					xp = int(content)
					if xp > 200000000:
						xp = 200000000
				except:
					pass
			else:
				player = msgcontent[1].strip()
				xp = 200000000
			for i in skills:
				if skill in skills:
					for l in list:
						if l.name == player:
							if l.returnSkill(skill)[1] > xp:
								print("ssss")
								xp = 200000000
							await client.send_message(client.get_channel("496381094283706388"), l.remainingxp(skill, xp))
							await client.delete_message(message)
							break
				break
	if message.content.startswith(";;worm"):
		await client.send_file(message.channel,'imgs/Grotworm.png')
		
		await client.send_file(message.channel,'imgs/wormception.png')
		await client.send_file(message.channel,'imgs/Diedtoworm.png')
	if message.content.startswith(";;noob"):
		await client.send_file(message.channel,'imgs/Noob.png')
	if message.content.startswith(";;totalxp"):
		total = 0
		if len(list) >= 86:
			for i in list:
				total += i.rawxp
			await client.send_message(client.get_channel("496381094283706388"), "Total Raw XP of all Completionist members: "+format(total,',d'))
	if message.content.startswith(";;skills"):
		msg = "Skills available\n```"
		for i in skills:
			msg += i+"\n"
		msg = msg+"```\nTo use type ;;(skill) (your in-game name) -n (xp amount)\nYou don't need to use xp amount for 200m calculations. You can use shortcuts m for millions and k for thousands,\n**Note:** Names are case-sensitive so always put capitalized letter first.\nExample: ;;prayer Kaolin -n 158m\nAlso if command doesn't work, it's because the list is updating"
		await client.send_message(client.get_channel("496381094283706388"),msg)
	if message.content.startswith(";;kaolin"):
		await client.send_message(message.channel, " *You are crazy.*\n\n~Con, 2018.")
	if message.content.startswith(";;petsim"):
		tags = message.content[len(';;petsim'):].strip()
		if tags == "":
			amount = 1250
		else:
			if int(tags) > 100000:
				amount = 1250
			else:
				amount = int(tags)
		i = 0
		while True:
			i+=1
			
			if randint(1,amount) == amount:
				break
		await client.send_message(message.channel, "your kc is "+str(i))
	if message.content.startswith(";;xpamounts"):
		msg = message.content.split(" ")
		if len(msg) >=2:
			if msg[1] in skills:
				for i in skills:
					if i == msg[1]:
						mess = "P0 amounts of xp from skill '"+i+"'\n"
						with open("skills/"+i+".csv","r") as f:
							for l in f:
								li = l.split(";")
								mess += li[0]+": "+format(int(li[1]),',d')+"\n"
						await client.send_message(client.get_channel("496381094283706388"), mess)
	if message.content.startswith(";;info"):
		await client.send_message(message.channel, "Bot created by Kaolin, tracks completionist clan members progress")
	if message.content.startswith(";;hsempty"):
		if message.author.id == "132166600513159168":
			msgc = message.content.split(" ")
			ins = int(msgc[1])
			await client.purge_from(client.get_channel("487028563493650442"),limit=ins)
			await client.delete_message(message)
	if message.content.startswith(";;chatwadmin"):
		if message.author.id == "132166600513159168":
			chn = client.get_channel("441269550705803284")
			msg = re.sub(";;chatwadmin","",message.content)
			await client.send_message(chn, msg)
			await client.delete_message(message)
	# if message.channel.id == "441269550705803284":
		# print(message.author.name+":"+message.content)
	if message.content.startswith(";;overlord"):
		if message.author.id == "132166600513159168":
			print("ur overlord")
		await client.delete_message(message)
	if message.content.startswith(";;alts"):
		msg = """
		**Completionist Alt accounts**

	```
	Kaolin, Kaolin jr
	Chizuru, Ru
	James, Blazing, Alone
	Mei, Harumin
	Hayley, Not George
	Con, Lantadyme
	Night, Risk
	Whatsoutside, Crimson
	Level, Up
	Pyro, Pax, Pryo
	Book, Table
	Friend, Death
	Gentle Guy, Tranquil Guy, Peaceful Guy
	Bruddah, Connie
	Final Baby, Ellen
	```
		"""
		await client.send_message(message.channel, msg)
client.loop.create_task(loopR(client,list))
client.run("#")

