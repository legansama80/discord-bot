import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import time
import sqlite3
import random
import smtplib

from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont

import os
from os import environ




#Davet Linki https://discord.com/api/oauth2/authorize?client_id=789072650622074900&permissions=8&scope=bot
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '!', intents = intents)

#On member join ve remove komutları için yukarıdakiler lazım


def registeration_code_creator():
    conn =sqlite3.connect(f"/{database}")
    c = conn.cursor()
    c.execute("SELECT COUNT (*) FROM customers")
    rowcount = c.fetchone()[0]

    for i in range(1,rowcount+1):
        number=random.randint(100000000,999999999)

        c.execute(f"""UPDATE customers SET registration_code = {number} WHERE rowid={i}""" )

        conn.commit()

    conn.close()


def email_sender():


    sender_email="zzwarningzz@gmail.com"

    password ="152433ali"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,password)
    conn =sqlite3.connect(f"/{database}")
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    items=c.fetchall()


    for item in items:
        rec_email=item[2]
        message=str(item[6])
        print(rec_email, message)

        server.sendmail(sender_email,rec_email,message)



@client.command(pass_context=True)
async def group_room(ctx,group,member):
    guild= discord.Guild
    guild=ctx.guild
    name= group+"_sohbet"
    print(name)
    channel = discord.utils.get(client.get_all_channels(), guild__name='Bilkent Münazara', name=name)
    print(bool(channel))
    if bool(channel)== True:
        await channel.set_permissions(member,view_channel=True)

    if bool(channel)==False:
        category= client.get_channel(792694410923737100)

        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False)
    }
        text_channel = await guild.create_text_channel(name,overwrites=overwrites,category=category)
        voice_channel = await guild.create_voice_channel(name,overwrites=overwrites,category=category)
        await text_channel.set_permissions(member,view_channel=True)
        await voice_channel.set_permissions(member,view_channel=True)



@client.command(pass_context=True)
async def school_room(ctx,uni,member):
    guild= discord.Guild
    guild=ctx.guild
    name=uni+"_sohbet"
    print(name)
    channel = discord.utils.get(client.get_all_channels(), guild__name='Bilkent Münazara', name=name)
    print(bool(channel))
    if bool(channel)== True:
        await channel.set_permissions(member,view_channel=True)

    if bool(channel)==False:
        category= client.get_channel(792702920142618625)

        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False)
    }

        text_channel = await guild.create_text_channel(name,overwrites=overwrites,category=category)
        voice_channel = await guild.create_voice_channel(name,overwrites=overwrites,category=category)
        await text_channel.set_permissions(member,view_channel=True)
        await voice_channel.set_permissions(member,view_channel=True)



@client.event
async def on_ready():
    print("bot hazır")


@client.command()
async def registration_table(ctx):
    channel= client.get_channel(ctx.channel)
    embed=discord.Embed(
    title="Münazara Kanalına Hoşgeldin",
    description="Lütfen turnuvaya kayıt olduğun mail adresini bana mesajın başına '!(ünlem işareti)' koyarak gönder, böylece seni kanala ekleyebilirim :).")
    colour=discord.Colour.blue()
    embed.set_footer(text="this is a footer")
    embed.set_image(url="https://cdn.discordapp.com/attachments/789203656003682334/789400387370876969/indir.jpg")
    embed.set_author(name="Münazara",
    icon_url="https://cdn.discordapp.com/attachments/789203656003682334/789400387370876969/indir.jpg")
    embed.add_field(name="Örnek",value="crazyboy_aykutfeatceza@hotmail.com",inline=True)
    welcome_message= await ctx.send(embed=embed)



"""
@client.event
async def on_member_join(member):
    channel= client.get_channel(789979085769539602)
    embed=discord.Embed(
    title="Münazara Kanalına Hoşgeldin",
    description="Lütfen turnuvaya kayıt olduğun mail adresini bana mesajın başına '!(ünlem işareti)' koyarak gönder, böylece seni kanala ekleyebilirim :).")
    colour=discord.Colour.blue()
    embed.set_footer(text="this is a footer")
    embed.set_image(url="https://cdn.discordapp.com/attachments/789203656003682334/789400387370876969/indir.jpg")
    embed.set_author(name=member,
    icon_url="https://cdn.discordapp.com/attachments/789203656003682334/789400387370876969/indir.jpg")
    embed.add_field(name="Örnek",value="crazyboy_aykutfeatceza@hotmail.com",inline=True)
    print(f"{member} suncuya katıldı")
    time.sleep(2)
    welcome_message= await channel.send(embed=embed)


   # await welcome_message.add_reaction("😡")
   # await welcome_message.add_reaction("😃")
"""


@client.command(pass_context=True)
async def register(ctx,code):
    member= ctx.author
    conn =sqlite3.connect(f"/{database}")
    c = conn.cursor()
    a=False
    c.execute("SELECT * FROM customers")
    items=c.fetchall()


    for item in items:

        nick= item[0]+" "+item[1]
        print(nick)
        if (item[6]== code and item[3]=="Jury"):
            await member.send("Kaydınız 'Jüri' olarak tamamlanmıştır")
            await member.add_roles(discord.utils.get(member.guild.roles,name="Jüri"))
            await member.edit(nick=nick)

            a=True
            break

        elif (item[6]== code and item[3]=="contestant"):
            await member.send("Kaydınız 'Yarışmacı' olarak tamamlanmıştır. ")
            await member.add_roles(discord.utils.get(member.guild.roles,name="Yarışmacı"))
            await member.edit(nick=nick)

            group=item[5]
            uni= item[4]
            await school_room(ctx,uni,member)
            await group_room(ctx,group,member)


            a=True
            break
    conn.close()

    if a == False:
        await ctx.author.send("Üzgünüm ama listede kaydınız bulunmamaktadır")



@client.command(pass_context = True)
async def clear(ctx, number):
    channel= ctx.channel
    number = int(number) #Converting the amount of messages to delete to an integer
    messages = await channel.history(limit=number).flatten()
    for b in messages: await b.delete()




@client.event
async def on_message(message):
    channel_welcome=client.get_channel(789979085769539602)

    if message.channel==channel_welcome:
        await message.delete()


    await client.process_commands(message)

#TKİNTER CODES

def get_database():
    global database
    database= filedialog.askopenfilename()
    print(database)
    my_label=Label(root,text="Dosya Yüklendi",font=tkFont.Font(family="Garamond",size=12)).place(x=290,y=115)


root=Tk()
fontStyle = tkFont.Font(family="Garamond", size=20)

program_title=Label(root,text="Münazara Bot",font=fontStyle)
program_title.place(x=320,y=0)


load_button=Button(root,text="Katılımcıları Yükle",command=get_database,font=fontStyle).place(x=50,y=100)

create_passwords_button=Button(root,text="Şifreleri Oluştur",font=fontStyle,command=registeration_code_creator)
create_passwords_button.place(x=50,y=250)

send_passwords_button=Button(root,text="Şifreleri Yolla",font=fontStyle,command=email_sender)
send_passwords_button.place(x=50,y=400)

run_bot_button=Button(root,text="Botu Çalıştır",font=fontStyle,command=root.destroy)
run_bot_button.place(x=580,y=480)

root.resizable(width=False, height=False)
root.minsize(width=800, height=600)
root.maxsize(width=800, height=600)
root.mainloop()





client.run("Nzg5MDcyNjUwNjIyMDc0OTAw.X9svLA.4Q5xJRl5MLaDmHoncGJL7okH20Y")
