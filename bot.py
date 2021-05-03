import discord
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import db

from urllib import parse, request
import re

from bot_token import get_token

firebase_admin.initialize_app(options={'databaseURL': 'https://vitask.firebaseio.com/'})

ref = db.reference('vitask')
tut_ref = ref.child('owasp')
new_ref = tut_ref.child('leaderboard')

bot = commands.Bot(command_prefix='!owasp ', description="The official OWASP VITCC Discord Bot.")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command(pass_context=True)
@commands.has_any_role("Board Member")
async def add_data(ctx, name, discord_name, rating=0, contributions=0):
    try:
        data = ref.child("owasp").child("leaderboard").get()
        count = 0
        for i in data:
            # Check if already added
            if(data[i]["Name"].casefold()==name.casefold() and data[i]["Discord"].casefold()==discord_name.casefold()):
                count += 1
                embed = discord.Embed(title=f"{ctx.guild.name}", description="User already exists.", color=discord.Color.blue())
                embed.add_field(name="Name", value=f"{data[i]['Name']}")
                embed.add_field(name="Discord Name", value=f"{data[i]['Discord']}")
                embed.add_field(name="Rating", value=f"{data[i]['Rating']}")
                embed.add_field(name="Contributions", value=f"{data[i]['Contributions']}")
                embed.set_thumbnail(url="https://owaspvit.com/assets/owasp-logo.png")
                
                await ctx.send(embed=embed)
         
        if(count==0):
            # Insert if not added already
            new_ref.push({
                'Rating': rating,
                'Name': name,
                'Discord': discord_name,
                'Contributions': contributions
            })
            embed = discord.Embed(title=f"{ctx.guild.name}", description="Added data to the OWASP Leaderboard.", color=discord.Color.blue())
            embed.add_field(name="Name", value=f"{name}")
            embed.add_field(name="Discord Name", value=f"{discord_name}")
            embed.add_field(name="Rating", value=f"{rating}")
            embed.add_field(name="Contributions", value=f"{contributions}")
            embed.set_thumbnail(url="https://owaspvit.com/assets/owasp-logo.png")

            await ctx.send(embed=embed)
        
    except Exception as e:
        print(e)
        
@bot.command(pass_context=True)
@commands.has_any_role("Board Member")
async def update_data(ctx, name, discord_name, rating=0, contributions=0):
    try:
        data = ref.child("owasp").child("leaderboard").get()
        count = 0
        for i in data:
            # Check if already added
            if(data[i]["Name"].casefold()==name.casefold() and data[i]["Discord"].casefold()==discord_name.casefold()):
                selector = ref.child("owasp").child("leaderboard").child(i)
                selector.update({
                    'Rating': rating,
                    'Name': name,
                    'Discord': discord_name,
                    'Contributions': contributions
                })
                embed = discord.Embed(title=f"{ctx.guild.name}", description="Updated data to the OWASP Leaderboard.", color=discord.Color.blue())
                embed.add_field(name="Name", value=f"{name}")
                embed.add_field(name="Discord Name", value=f"{discord_name}")
                embed.add_field(name="Rating", value=f"{rating}")
                embed.add_field(name="Contributions", value=f"{contributions}")
                embed.set_thumbnail(url="https://owaspvit.com/assets/owasp-logo.png")
                
                await ctx.send(embed=embed)
        
    except Exception as e:
        print(e)
        
@bot.command(pass_context=True)
@commands.has_any_role("Leaderboard")
async def contribution(ctx, name, discord_name, task):
    try:
        data = ref.child("owasp").child("leaderboard").get()
        count = 0
        for i in data:
            # Check if already added
            if(data[i]["Name"].casefold()==name.casefold() and data[i]["Discord"].casefold()==discord_name.casefold()):
                selector = ref.child("owasp").child("leaderboard").child(i).get()
                selector_update = ref.child("owasp").child("leaderboard").child(i)
                points = 0
                if(task.casefold()=="pull request".casefold()):
                    points = 20
                elif(task.casefold()=="blog".casefold()):
                    points = 5
                elif(task.casefold()=="sm posting".casefold()):
                    points = 20
                elif(task.casefold()=="weekly work".casefold()):
                    points = 5
                elif(task.casefold()=="idea".casefold()):
                    points = 3
                elif(task.casefold()=="brochure".casefold()):
                    points = 5
                elif(task.casefold()=="news".casefold()):
                    points = 5
                elif(task.casefold()=="demos".casefold()):
                    points = 20
                elif(task.casefold()=="oc volunteer".casefold()):
                    points = 30
                elif(task.casefold()=="oc assigned".casefold()):
                    points = 20
                elif(task.casefold()=="oc no work".casefold()):
                    points = -10
                elif(task.casefold()=="oc manager".casefold()):
                    points = 50
                elif(task.casefold()=="wtf".casefold()):
                    points = 50
                elif(task.casefold()=="discord".casefold()):
                    points = 10
                elif(task.casefold()=="marketing".casefold()):
                    points = 2
                elif(task.casefold()=="mini project".casefold()):
                    points = 100
                elif(task.casefold()=="complete project".casefold()):
                    points = 200
                elif(task.casefold()=="promotion medium".casefold()):
                    points = 25
                elif(task.casefold()=="promotion large".casefold()):
                    points = 50
        
                rating = selector["Rating"]+points
                contributions = selector["Contributions"]+1
                selector_update.update({
                    'Rating': rating,
                    'Name': name,
                    'Discord': discord_name,
                    'Contributions': contributions
                })
                embed = discord.Embed(title=f"{ctx.guild.name}", description="Added contribution to the OWASP Leaderboard.", color=discord.Color.blue())
                embed.add_field(name="Name", value=f"{name}")
                embed.add_field(name="Discord Name", value=f"{discord_name}")
                embed.add_field(name="Rating", value=f"{rating}")
                embed.add_field(name="Contributions", value=f"{contributions}")
                embed.set_thumbnail(url="https://owaspvit.com/assets/owasp-logo.png")
                
                await ctx.send(embed=embed)
        
    except Exception as e:
        print(e)
        
    
@bot.command()
async def fetch_data(ctx, name, discord_name):
    data = ref.child("owasp").child("leaderboard").get()
    for i in data:
        if(data[i]["Name"].casefold()==name.casefold() and data[i]["Discord"].casefold()==discord_name.casefold()):
            embed = discord.Embed(title=f"{ctx.guild.name}", description="Fetched OWASP Leaderboard profile.", color=discord.Color.blue())
            embed.add_field(name="Name", value=f"{data[i]['Name']}")
            embed.add_field(name="Discord Name", value=f"{data[i]['Discord']}")
            embed.add_field(name="Rating", value=f"{data[i]['Rating']}")
            embed.add_field(name="Contributions", value=f"{data[i]['Contributions']}")
            embed.set_thumbnail(url="https://owaspvit.com/assets/owasp-logo.png")

            await ctx.send(embed=embed)

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="OWASP Leaderboard"))
    print('OWASP VITCC Bot v1.0')


@bot.listen()
async def on_message(message):
    if "owasp github" in message.content.lower():
        await message.channel.send('Our GitHub is https://github.com/owaspvit')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp landlord" in message.content.lower():
        await message.channel.send('My landlord is https://github.com/apratimshukla6')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp mailman" in message.content.lower():
        await message.channel.send('My mailman is https://github.com/princesinghr1')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp plumber" in message.content.lower():
        await message.channel.send('My plumber is https://arnavtripathy98.medium.com/')
        await bot.process_commands(message)

@bot.listen()
async def on_message(message):
    if "owasp firefighter" in message.content.lower():
        await message.channel.send('My firefighter is https://medium.com/@lakshaybaheti1')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp carpenter" in message.content.lower():
        await message.channel.send('My carpenter is https://github.com/aakashratha1006')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp janitor" in message.content.lower():
        await message.channel.send('My janitor is https://github.com/MarkRaghav')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp electrician" in message.content.lower():
        await message.channel.send('My electrician is https://github.com/Swapnil0115')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp photographer" in message.content.lower():
        await message.channel.send('My photographer is https://github.com/ShubhamManna')
        await bot.process_commands(message)
        
@bot.listen()
async def on_message(message):
    if "owasp website" in message.content.lower():
        await message.channel.send('Our Website is https://owaspvit.com')
        await bot.process_commands(message)

bot.run(get_token())