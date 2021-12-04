import discord
from discord import Reaction
import asyncio
import time
import random
import discord.utils
import operator
from discord_components import DiscordComponents, Button, ButtonStyle, Interaction
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import unidecode

scope = ["https://spreadsheets.google.com/feeds",
'https://www.googleapis.com/auth/spreadsheets',
"https://www.googleapis.com/auth/drive.file",
"https://www.googleapis.com/auth/drive"]

creds=ServiceAccountCredentials.from_json_keyfile_name("cred.json",scope)

cli=gspread.authorize(creds)
sheet=cli.open("player_history").sheet1
sheetmod=cli.open("player_historymod").sheet1
sheetind=cli.open("indian_mod").sheet1
sheetindmod=cli.open("indian_mod_mod").sheet1
client= discord.Client()
DiscordComponents(client)
async def pagination(message,paginationList):
    
    current = 0
    
    mainMessage = await message.channel.send(
        "",
        embed = paginationList[current],
        components = [ 
            [
                Button(
                    label = "Prev",
                    id = "back",
                    style = ButtonStyle.red
                ),
                Button(
                    label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                    id = "cur",
                    style = ButtonStyle.grey,
                    disabled = True
                ),
                Button(
                    label = "Next",
                    id = "front",
                    style = ButtonStyle.red
                )
            ]
        ]
    )
    #Infinite loop
    while True:
        
        try:
            interaction = await client.wait_for(
                "button_click",
                check = lambda i: i.component.id in ["back", "front"], 
                timeout = 4.0 
            )
           
            if interaction.component.id == "back":
                current -= 1
            elif interaction.component.id == "front":
                current += 1
            
            if current == len(paginationList):
                current = 0
            elif current < 0:
                current = len(paginationList) - 1

            
            await interaction.respond(
                type = 7,
                embed = paginationList[current],
                components = [ 
                    [
                        Button(
                            label = "Prev",
                            id = "back",
                            style = ButtonStyle.red
                        ),
                        Button(
                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                            id = "cur",
                            style = ButtonStyle.grey,
                            disabled = True
                        ),
                        Button(
                            label = "Next",
                            id = "front",
                            style = ButtonStyle.red
                        )
                    ]
                ]
            )
        except asyncio.TimeoutError:
            await mainMessage.edit(
                components = [
                    [
                        Button(
                            label = "Prev",
                            id = "back",
                            style = ButtonStyle.red,
                            disabled = True
                        ),
                        Button(
                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                            id = "cur",
                            style = ButtonStyle.grey,
                            disabled = True
                        ),
                        Button(
                            label = "Next",
                            id = "front",
                            style = ButtonStyle.red,
                            disabled = True
                        )
                    ]
                ]
            )
            break
@client.event
async def on_ready():
    sum=0
    for x in client.guilds:
        
        sum+=x.member_count
    activity = discord.Game(name=f"(&atlas) {sum} members, {len(client.guilds)} servers", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("logged in as {0.user}".format(client))
countries=[]
f=open("coun.txt","r")
for line in f.readlines():
    for i in range(len(line)):
        if line[i].isnumeric()==True:
            line=line[0:i-1]
            break
    countries.append(line.lower())
coun=countries
indians=[]
f1=open("indian_mod.txt","r",encoding="utf-8")
for line in f1.readlines():
    indians.append(unidecode.unidecode(line[0:len(line)-1].lower()))


flag=False
ongoing_chan=[]
curr_lb=[]
d1={}
flag=False
@client.event
async def on_message(message):
    global d1,flag
    flag=False
    # await lock.acquire()
    if message.author==client.user:
        return
    
    if message.content.lower()==("&atlas"):
        embed=discord.Embed(title="Atlast Bot", description="The ol' Atlas game where you have to name countries starting with the last letter of the country named by the previous player.\n currently two variants available, the normal atlas game and another variant of the same.\n\n List of currently available commands:\n&help : info regarding the first type\n\n&modhelp : info regarding the second variant (this one is better 😈)\n\n&start : starts the game with default rounds set to 2, otherwise type '&start' followed by the number of rounds to set the number of rounds.\n\n&modstart : starts the mod variant. set number of rounds the same way as above.\n\n&lb : displays all time leaderboard for the first variant.\n\n&modlb : displays all time leaderboard for the second variant.\n\nTo add it to your server click the below link:\nhttps://bit.ly/3nrTzYZ \nHope you enjoy 😊",color=discord.Color(0x1abc9c))
        await message.channel.send(embed=embed)
    if message.content.lower().startswith("&help"):
        embed=discord.Embed(title="About this game",description="Basically an atlas game where players have to name a place(country for now) starting with the last letter of the name of the place given by the previous player.\n use '&start' followed by number of rounds to start(0-99).",color=discord.Color(0x1abc9c))
        await message.channel.send(embed=embed)


    if message.content.lower().startswith("&modhelp") or message.content.lower().startswith("&mh"):
        embed=discord.Embed(title="About Atlas mod",description="Basically a variant of the normal atlas game. Here players have to name a place(country for now) starting with the letter thrown randomly by the bot, only catch being that the player who answers first gets the point.\n use '&modstart' followed by number of rounds to start(0-99).",color=discord.Color(0x1abc9c))
        await message.channel.send(embed=embed)

    if message.content.lower().startswith("&stop"):
        await message.channel.send("haha fuck you....game aint stopping!!! 😈")
        flag=True
        

    if message.content.lower().startswith("&start"):
        
        if message.channel in ongoing_chan:
            await message.channel.send("Already a running game!!")
            return
        else:
            ongoing_chan.append(message.channel)
            rounds=message.content[-2]
            rounds+=message.content[-1]
            if rounds[0].isalpha()==False and rounds[1].isalpha()==False:
                roundsnum=int(rounds)
            elif rounds[0].isalpha()==True and rounds[1].isalpha()==False:
                roundsnum=int(rounds[1])
            else:
                roundsnum=2
            coun=[]
            for co in countries:
                coun.append(co)

            
            embed1=discord.Embed(title="Welcome, react on this message to enter.",description="",color=discord.Color(0x2ecc71))
            mess="Welcome, react on this message to enter."
            mss=await message.channel.send(embed=embed1)
            reaction= await mss.add_reaction('✔')
            
            t=time.time()+ 5
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '✔'

            def stopcheck(reaction,user):
                return user==message.author and str(r1.emoji)== '❌'

            try:
                while time.time()<t:
                    reaction, user = await client.wait_for('reaction_add',timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('okk')

            if reaction==None:
                await message.channel.send("but no one reacted only 😢")
                ongoing_chan.remove(message.channel)
                # lock.release()
                return
            users = await reaction.users().flatten()
            j=len(users)
            for u in users:
                if u.id==829214415131115530:
                    users.remove(u)
            
            await message.channel.send("Are you ready.....")
            # if j==1:
            #     await message.channel.send("but no one reacted only 😢")
            #     return
            for u in users:
                    await message.channel.send("{}".format(u.mention))
            await message.channel.send('game starting.....')
            time.sleep(3)
            
            d={}
            for u in users:
                d[u]=0
            count=1
            
            
            def check1(m):
                return m.content.lower() in coun and m.channel==message.channel
            
            ######################################
            # f=flag
            # if f:
            #     return

            # def stopcheck(m):
            #     return m.content.lower()=="&stop" and m.author==message.author
            # if await client.wait_for('message',check=stopcheck):
            #     return
            ######################################
            
            rand=random.randint(0, 194)
            msg1=coun[rand]
            last_letter=msg1[0]
            for i in range(len(users)):
                def check1(m):
                    return m.content.lower() in coun and m.channel==message.channel and m.author==users[i%len(users)] and m.content[0].lower()==last_letter

                m1=await message.channel.send("{0} Name a country starting from '{1}'".format(users[i%len(users)].mention,last_letter))
                try:
                    msg= await client.wait_for('message',check=check1,timeout=20.0)
                    # emote=client.get_emoji(887436771971964928)
                    emoji = discord.utils.get(message.guild.emojis, name='siddhukek')
                    emoji2 = discord.utils.get(message.guild.emojis, name='big_brain')
                    if emoji:
                        await msg.add_reaction(emoji)
                    elif emoji2:
                        await msg.add_reaction(emoji2)
                    else:
                        await msg.add_reaction('✅')
                    # await msg.add_reaction("<siddhukek:887436771971964928>")
                    # await msg.add_reaction(emote)
                    await message.channel.send("CORRECT!!")
                    coun.remove(msg.content.lower())
                    d[users[i%len(users)]]+=1
                    await message.channel.send("{0} : {1}".format(users[i%len(users)],d[users[i%len(users)]]))
                    last_letter=msg.content[-1]
                    count=0
                    for pos in coun:
                        if last_letter != pos[0]:
                            count+=1
                    if count==len(coun):
                        await message.channel.send("No country left starting with '{}'".format(last_letter))
                        new_letterpos=random.randint(0, len(coun))
                        last_letter=coun[new_letterpos][0]

                except asyncio.TimeoutError:
                    await message.channel.send("TIMES UP!!")
            k=0
            k+=1
            # flag=False
            while k<roundsnum:
                for i in range(len(users)):
                    def check1(m):
                        return m.content.lower() in coun and m.channel==message.channel and m.author==users[i%len(users)] and m.content[0].lower()==last_letter
                    await message.channel.send("{0} Name a country starting from '{1}'".format(users[i%len(users)].mention,last_letter))
                    try:
                        msg= await client.wait_for('message',check=check1,timeout=20.0)
                        # emote=client.get_emoji(887436771971964928)
                        emoji = discord.utils.get(message.guild.emojis, name='siddhukek')
                        emoji2 = discord.utils.get(message.guild.emojis, name='big_brain')
                        if emoji:
                            await msg.add_reaction(emoji)
                        elif emoji2:
                            await msg.add_reaction(emoji2)
                        else:
                            await msg.add_reaction('✅')

                        # await msg.add_reaction("<siddhukek:887436771971964928>")
                        # await msg.add_reaction('<"siddhukek:887436771971964928')
                        coun.remove(msg.content.lower())
                        if len(coun)==0:
                            flag=True
                            break
                        await message.channel.send("CORRECT!!")
                        d[users[i%len(users)]]+=1
                        await message.channel.send("{0} : {1}".format(users[i%len(users)],d[users[i%len(users)]]))
                        last_letter=msg.content[-1]
                        count=0
                        for pos in coun:
                            if last_letter != pos[0]:
                                count+=1
                        if count==len(coun):
                            await message.channel.send("no country left starting with '{}'".format(last_letter))
                            new_letterpos=random.choice(coun)
                            last_letter=new_letterpos[0]
                    except asyncio.TimeoutError:
                        await message.channel.send("TIMES UP!!")
                if flag:
                    break
                k+=1
            

            dict(sorted(d.items(),key=lambda item:item[1],reverse=True))
            ds=dict(sorted(d.items(),key=operator.itemgetter(1),reverse=True))
            embed=discord.Embed(title="POINTS TABLE!!",description="",color=discord.Color(0xf1c40f))
            for key in ds.keys():
                embed.add_field(name=key,value=ds[key],inline=False)
            await message.channel.send(embed=embed)
            
            
            #storing playerdata
            
            for k in d.keys():
                cell=sheet.find(str(k))
                if cell==None:
                    sheet.append_row([str(k),d[k]])
                else:
                    sheet.update_cell(cell.row, cell.col + 1, d[k]+int(sheet.cell(cell.row, cell.col + 1).value))

            # f1=open("player_history.txt","a")
            # for li in d.keys():
            #     f1.write("{}/ {}\n".format(str(li),str(d[li])))
            ongoing_chan.remove(message.channel)
            return
        # d1=d
    if message.content.lower().startswith("&lb"):
        if message.channel in curr_lb:
            await message.channel.send("wait for a few seconds then try again.")
            return
        else:
            curr_lb.append(message.channel)
            embed3=discord.Embed(title="All Time Scoreboard",description="Page no. 1",color=discord.Color(0x1abc9c))
            d1={}
            
            sheetlist=sheet.get_all_values()
            for l in sheetlist:
                l[1]=int(l[1])
            sheetlist.sort(key=lambda x:x[1],reverse=True)
            for l in sheetlist:
                d1[l[0]]=l[1]
            print(d1)
            paginationList1=[]
            
            d2 = dict(sorted(d1.items(), key=operator.itemgetter(1),reverse=True))
            emcount=1
            for k in d2.keys():
                if emcount%5==1 and emcount!=1:
                    paginationList1.append(embed3)
                    embed3=discord.Embed(title="All Time Scoreboard",description=f"Page no. {int(emcount/5 + 1)}",color=discord.Color(0x1abc9c))
                embed3.add_field(name=f"{emcount}. {k}",value=d2[k],inline=False)
                emcount+=1
            paginationList1.append(embed3)
            await pagination(message,paginationList1)
            print(len(paginationList1))
            curr_lb.remove(message.channel) 
            return

    if message.content.lower().startswith("&modstart") or message.content.lower().startswith("&ms"):
        if message.channel in ongoing_chan:
            await message.channel.send("Already a running game!!")
            return
        else:
            ongoing_chan.append(message.channel)
            rounds=message.content[-2]
            rounds+=message.content[-1]
            if rounds[0].isalpha()==False and rounds[1].isalpha()==False:
                roundsnum=int(rounds)
            elif rounds[0].isalpha()==True and rounds[1].isalpha()==False:
                roundsnum=int(rounds[1])
            else:
                roundsnum=2
            coun1=[]
            for co in countries:
                coun1.append(co)

            embed1=discord.Embed(title="Welcome to Atlas Mod, react on this message to enter.",description="",color=discord.Color(0x2ecc71))
            mess="Welcome, react on this message to enter."
            mss=await message.channel.send(embed=embed1)
            reaction= await mss.add_reaction('✔')
            
            t=time.time()+ 5
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '✔'


            try:
                while time.time()<t:
                    reaction, user = await client.wait_for('reaction_add',timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('okk')

            if reaction==None:
                await message.channel.send("but no one reacted only 😢")
                ongoing_chan.remove(message.channel)
                return
            
            users = await reaction.users().flatten()
            j=len(users)
            for u in users:
                if u.id==829214415131115530:
                    users.remove(u)
            
            await message.channel.send("Are you ready.....")
            for u in users:
                    await message.channel.send("{}".format(u.mention))
            await message.channel.send('game starting.....')
            time.sleep(3)

            dmod={}
            for u in users:
                dmod[u]=0
            count=1
            

            

            rand=random.randint(0, 194)
            msg1=coun1[rand]
            last_letter=msg1[0]
            rd=0
            while(rd<roundsnum*len(dmod)):
                def check1(m):
                    return m.content.lower() in coun1 and m.channel==message.channel and m.content.lower()[0]==last_letter and m.author in dmod.keys()
                m2=await message.channel.send("Name a country starting with '{}'".format(last_letter))
                try:
                    me= await client.wait_for('message',check=check1,timeout=10.0)
                    emoji = discord.utils.get(message.guild.emojis, name='siddhukek')
                    emoji2 = discord.utils.get(message.guild.emojis, name='big_brain')
                    if emoji:
                        await me.add_reaction(emoji)
                    elif emoji2:
                        await me.add_reaction(emoji2)
                    else:
                        await me.add_reaction('✅')
                    
                    await message.channel.send(f"CORRECT {me.author.mention}!!")
                    coun1.remove(me.content.lower())
                    dmod[me.author]+=1
                    await message.channel.send("{0} : {1}".format(me.author,dmod[me.author]))
                    
                    new_letterpos=random.randint(1, len(coun1))
                    last_letter=coun1[new_letterpos-1][0]

                except asyncio.TimeoutError:
                    await message.channel.send("No points for anyone!!")

                rd+=1

            d4=dict( sorted(dmod.items(), key=operator.itemgetter(1),reverse=True))
            embed=discord.Embed(title="POINTS TABLE (MOD)!!",description="",color=discord.Color(0xf1c40f))
            for key in d4.keys():
                embed.add_field(name=key,value=d4[key],inline=False)
            await message.channel.send(embed=embed)

            for k in dmod.keys():
                cell=sheetmod.find(str(k))
                if cell==None:
                    sheetmod.append_row([str(k),dmod[k]])
                else:
                    sheetmod.update_cell(cell.row, cell.col + 1, dmod[k]+int(sheetmod.cell(cell.row, cell.col + 1).value))

           
            ongoing_chan.remove(message.channel)
            return

    if message.content.lower().startswith("&modlb"):
        if message.channel in curr_lb:
            await message.channel.send("wait for a few seconds then try again.")
            return
        else:
            curr_lb.append(message.channel)
            embed4=discord.Embed(title="All Time Scoreboard (Mod)",description="Page no. 1",color=discord.Color(0x1abc9c))
            d5={}
            
            sheetlist1=sheetmod.get_all_values()
            for l in sheetlist1:
                l[1]=int(l[1])
            
            sheetlist1.sort(key=lambda x:x[1],reverse=True)
            print(sheetlist1)
            for l in sheetlist1:
                d5[l[0]]=l[1]
            dict(sorted(d5.items(),key=lambda item:item[1],reverse=True))
            dm = dict( sorted(d5.items(), key=operator.itemgetter(1),reverse=True))
            print(dm)
            
            paginationList=[]
            
            emcount=1
            for k in dm.keys():
                if emcount%5==1 and emcount!=1:
                    paginationList.append(embed4)
                    embed4=discord.Embed(title="All Time Scoreboard (Mod)",description=f"Page no. {int(emcount/5 + 1)}",color=discord.Color(0x1abc9c))
                embed4.add_field(name=f"{emcount}. {k}",value=dm[k],inline=False)
                emcount+=1
            paginationList.append(embed4)
            await pagination(message,paginationList)
            print(len(paginationList))
            curr_lb.remove(message.channel)
          
            return


    if message.content.lower().startswith("&istart"):
        
        if message.channel in ongoing_chan:
            await message.channel.send("Already a running game!!")
            return
        else:
            ongoing_chan.append(message.channel)
            rounds=message.content[-2]
            rounds+=message.content[-1]
            if rounds[0].isalpha()==False and rounds[1].isalpha()==False:
                roundsnum=int(rounds)
            elif rounds[0].isalpha()==True and rounds[1].isalpha()==False:
                roundsnum=int(rounds[1])
            else:
                roundsnum=2
            inds=[]
            for co in indians:
                inds.append(co)

            
            embed1=discord.Embed(title="Welcome to Atlas(India), react on this message to enter.",description="",color=discord.Color(0x2ecc71))
            mess="Welcome, react on this message to enter."
            mss=await message.channel.send(embed=embed1)
            reaction= await mss.add_reaction('✔')
            
            t=time.time()+ 5
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '✔'

            def stopcheck(reaction,user):
                return user==message.author and str(r1.emoji)== '❌'

            try:
                while time.time()<t:
                    reaction, user = await client.wait_for('reaction_add',timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('okk')

            if reaction==None:
                await message.channel.send("but no one reacted only 😢")
                ongoing_chan.remove(message.channel)
                # lock.release()
                return
            users = await reaction.users().flatten()
            j=len(users)
            for u in users:
                if u.id==829214415131115530:
                    users.remove(u)
            
            await message.channel.send("Are you ready.....")
            # if j==1:
            #     await message.channel.send("but no one reacted only 😢")
            #     return
            for u in users:
                    await message.channel.send("{}".format(u.mention))
            await message.channel.send('game starting.....')
            time.sleep(3)
            
            d={}
            for u in users:
                d[u]=0
            count=1
            
            
            def check1(m):
                return m.content.lower() in inds and m.channel==message.channel
            
            
            rand=random.randint(0, 441)
            msg1=inds[rand]
            last_letter=msg1[0]
            
            k=0
            
            # flag=False
            while k<roundsnum:
                for i in range(len(users)):
                    def check1(m):
                        return m.content.lower() in inds and m.channel==message.channel and m.author==users[i%len(users)] and m.content[0].lower()==last_letter
                    await message.channel.send("{0} Name an indian place starting from '{1}'".format(users[i%len(users)].mention,last_letter))
                    try:
                        msg= await client.wait_for('message',check=check1,timeout=20.0)
                        # emote=client.get_emoji(887436771971964928)
                        emoji = discord.utils.get(message.guild.emojis, name='siddhukek')
                        emoji2 = discord.utils.get(message.guild.emojis, name='big_brain')
                        if emoji:
                            await msg.add_reaction(emoji)
                        elif emoji2:
                            await msg.add_reaction(emoji2)
                        else:
                            await msg.add_reaction('✅')

                        # await msg.add_reaction("<siddhukek:887436771971964928>")
                        # await msg.add_reaction('<"siddhukek:887436771971964928')
                        inds.remove(msg.content.lower())
                        if len(inds)==0:
                            flag=True
                            break
                        await message.channel.send("CORRECT!!")
                        d[users[i%len(users)]]+=1
                        await message.channel.send("{0} : {1}".format(users[i%len(users)],d[users[i%len(users)]]))
                        last_letter=msg.content[-1]
                        count=0
                        for pos in inds:
                            if last_letter != pos[0]:
                                count+=1
                        if count==len(inds):
                            await message.channel.send("no indian place left starting with '{}'".format(last_letter))
                            new_letterpos=random.choice(inds)
                            last_letter=new_letterpos[0]
                    except asyncio.TimeoutError:
                        await message.channel.send("TIMES UP!!")
                if flag:
                    break
                k+=1
            

            dict(sorted(d.items(),key=lambda item:item[1],reverse=True))
            ds=dict(sorted(d.items(),key=operator.itemgetter(1),reverse=True))
            embed=discord.Embed(title="POINTS TABLE(Indian)!!",description="",color=discord.Color(0xf1c40f))
            for key in ds.keys():
                embed.add_field(name=key,value=ds[key],inline=False)
            await message.channel.send(embed=embed)
            
            
            #storing playerdata
            
            for k in d.keys():
                cell=sheetind.find(str(k))
                if cell==None:
                    sheetind.append_row([str(k),d[k]])
                else:
                    sheetind.update_cell(cell.row, cell.col + 1, d[k]+int(sheetind.cell(cell.row, cell.col + 1).value))

            # f1=open("player_history.txt","a")
            # for li in d.keys():
            #     f1.write("{}/ {}\n".format(str(li),str(d[li])))
            ongoing_chan.remove(message.channel)
            return

    if message.content.lower().startswith("&ilb"):
        if message.channel in curr_lb:
            await message.channel.send("wait for a few seconds then try again.")
            return
        else:
            curr_lb.append(message.channel)
            embed3=discord.Embed(title="All Time Scoreboard(Indian)",description="Page no. 1",color=discord.Color(0x1abc9c))
            d1={}
            
            sheetlist=sheetind.get_all_values()
            for l in sheetlist:
                l[1]=int(l[1])
            sheetlist.sort(key=lambda x:x[1],reverse=True)
            for l in sheetlist:
                d1[l[0]]=l[1]
            print(d1)
            paginationList1=[]
            
            d2 = dict(sorted(d1.items(), key=operator.itemgetter(1),reverse=True))
            emcount=1
            for k in d2.keys():
                if emcount%5==1 and emcount!=1:
                    paginationList1.append(embed3)
                    embed3=discord.Embed(title="All Time Scoreboard(Indian)",description=f"Page no. {int(emcount/5 + 1)}",color=discord.Color(0x1abc9c))
                embed3.add_field(name=f"{emcount}. {k}",value=d2[k],inline=False)
                emcount+=1
            paginationList1.append(embed3)
            await pagination(message,paginationList1)
            print(len(paginationList1))
            curr_lb.remove(message.channel) 
            return

    if message.content.lower().startswith("&imodstart") or message.content.lower().startswith("&ims"):
        if message.channel in ongoing_chan:
            await message.channel.send("Already a running game!!")
            return
        else:
            ongoing_chan.append(message.channel)
            rounds=message.content[-2]
            rounds+=message.content[-1]
            if rounds[0].isalpha()==False and rounds[1].isalpha()==False:
                roundsnum=int(rounds)
            elif rounds[0].isalpha()==True and rounds[1].isalpha()==False:
                roundsnum=int(rounds[1])
            else:
                roundsnum=2
            ind=[]
            for co in indians:
                ind.append(co)

            embed1=discord.Embed(title="Welcome to Atlas Mod(India), react on this message to enter.",description="",color=discord.Color(0x2ecc71))
            mess="Welcome, react on this message to enter."
            mss=await message.channel.send(embed=embed1)
            reaction= await mss.add_reaction('✔')
            
            t=time.time()+ 5
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '✔'


            try:
                while time.time()<t:
                    reaction, user = await client.wait_for('reaction_add',timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('okk')

            if reaction==None:
                await message.channel.send("but no one reacted only 😢")
                ongoing_chan.remove(message.channel)
                return
            
            users = await reaction.users().flatten()
            j=len(users)
            for u in users:
                if u.id==829214415131115530:
                    users.remove(u)
            
            await message.channel.send("Are you ready.....")
            for u in users:
                    await message.channel.send("{}".format(u.mention))
            await message.channel.send('game starting.....')
            time.sleep(3)

            dmod={}
            for u in users:
                dmod[u]=0
            count=1
            

            

            rand=random.randint(0, 441)
            msg1=ind[rand]
            last_letter=msg1[0]
            rd=0
            while(rd<roundsnum*len(dmod)):
                def check1(m):
                    return m.content.lower() in ind and m.channel==message.channel and m.content.lower()[0]==last_letter and m.author in dmod.keys()
                m2=await message.channel.send("Name an indian place starting with '{}'".format(last_letter))
                try:
                    me= await client.wait_for('message',check=check1,timeout=10.0)
                    emoji = discord.utils.get(message.guild.emojis, name='siddhukek')
                    emoji2 = discord.utils.get(message.guild.emojis, name='big_brain')
                    if emoji:
                        await me.add_reaction(emoji)
                    elif emoji2:
                        await me.add_reaction(emoji2)
                    else:
                        await me.add_reaction('✅')
                    
                    await message.channel.send(f"CORRECT {me.author.mention}!!")
                    ind.remove(me.content.lower())
                    dmod[me.author]+=1
                    await message.channel.send("{0} : {1}".format(me.author,dmod[me.author]))
                    
                    new_letterpos=random.randint(1, len(ind))
                    last_letter=ind[new_letterpos-1][0]

                except asyncio.TimeoutError:
                    await message.channel.send("No points for anyone!!")

                rd+=1

            d4=dict( sorted(dmod.items(), key=operator.itemgetter(1),reverse=True))
            embed=discord.Embed(title="POINTS TABLE (MOD)(India)!!",description="",color=discord.Color(0xf1c40f))
            for key in d4.keys():
                embed.add_field(name=key,value=d4[key],inline=False)
            await message.channel.send(embed=embed)

            for k in dmod.keys():
                cell=sheetindmod.find(str(k))
                if cell==None:
                    sheetindmod.append_row([str(k),dmod[k]])
                else:
                    sheetindmod.update_cell(cell.row, cell.col + 1, dmod[k]+int(sheetindmod.cell(cell.row, cell.col + 1).value))

           
            ongoing_chan.remove(message.channel)
            return
    
    if message.content.lower().startswith("&imodlb") or message.content.lower()=='&imlb':
        if message.channel in curr_lb:
            await message.channel.send("wait for a few seconds then try again.")
            return
        else:
            curr_lb.append(message.channel)
            embed4=discord.Embed(title="All Time Scoreboard (Mod)(India)",description="Page no. 1",color=discord.Color(0x1abc9c))
            d5={}
            
            sheetlist1=sheetindmod.get_all_values()
            for l in sheetlist1:
                l[1]=int(l[1])
            
            sheetlist1.sort(key=lambda x:x[1],reverse=True)
            print(sheetlist1)
            for l in sheetlist1:
                d5[l[0]]=l[1]
            dict(sorted(d5.items(),key=lambda item:item[1],reverse=True))
            dm = dict( sorted(d5.items(), key=operator.itemgetter(1),reverse=True))
            print(dm)
            
            paginationList=[]
            
            emcount=1
            for k in dm.keys():
                if emcount%5==1 and emcount!=1:
                    paginationList.append(embed4)
                    embed4=discord.Embed(title="All Time Scoreboard (Mod)(India)",description=f"Page no. {int(emcount/5 + 1)}",color=discord.Color(0x1abc9c))
                embed4.add_field(name=f"{emcount}. {k}",value=dm[k],inline=False)
                emcount+=1
            paginationList.append(embed4)
            await pagination(message,paginationList)
            print(len(paginationList))
            curr_lb.remove(message.channel)
          
            return
    # lock.release() 
        

client.run('token🌚')        
