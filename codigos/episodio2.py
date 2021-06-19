from discord.ext import commands
from pymongo import MongoClient
import random
import discord

cluster = MongoClient("tu link de tu base de datos")
cluster_data = cluster["Discord"]["Bot"] #estos son en base a tu base de datos igualmente
client = commands.Bot(command_prefix="!")

token = "el token de tu bot"
@client.event
async def on_ready():
    print("bot cargado")

@client.command()
async def saludo(ctx):
    await ctx.send("Hola!")

@client.command()
async def abrir_cuenta(user):
    datos = cluster_data.find_one({"id": user.id})
    if datos == None:
        nom = user.name.replace(" ","")
        cuenta = {"id": user.id,"nombre": nom, "famorcoins": 200}
        cluster_data.insert_one(cuenta)
    else:
        return

@client.command()
async def trabajar(ctx):
    user = ctx.author
    await abrir_cuenta(user)
    datos = cluster_data.find_one({"id": user.id})
    famorcoins = datos["famorcoins"]
    recompensa = random.randint(200,1000)

    job0 = (f'Ayudaste a un empresario a evadir impuestos y te han recompensado con {recompensa} FamorCoins')
    job1 = (f'Declaraste impuestos de tu pc gamer y recuperaste {recompensa} FamorCoins')
    job2 = (f'Fuiste recepcionista de una empresa y te pagaron {recompensa} FamorCoins')
    job3 = (f'Fuiste maestro de preescolar y te pagaron {recompensa} FamorCoins')
    job4 = (f'Le hiciste un dibujo NSFW a un furro y te pago {recompensa} FamorCoins')
    job5 = (f'Hiciste una animacion y la subiste a Youtube, ganaste {recompensa} FamorCoins gracias a los anuncios')
    job6 = (f'Programaste un bot de Discord y te pagaron {recompensa} FamorCoins')
    job7 = (f'Hiciste un videojuego y ganaste {recompensa} FamorCoins de personas mayores')
    job8 = (f'Minaste criptomonedas durante 24 horas y ganaste {recompensa} FamorCoins')
    job9 = (f'Trabaste como albañil y ganaste {recompensa} FamorCoins')
    job10 = (f'Contruiste una casa en el centro de la ciudad y ganaste {recompensa} FamorCoins')
    job11 = (f'salvaste la vida de un enfermo y te pago {recompensa} FamorCoins')
    job12 = (f'un adolescente te pidio un condón y no hiciste nada incomodo así que te dio {recompensa} FamorCoins como propina')
    job13 = (f'Limpiaste el baño de una escuela pública y te pagaron  {recompensa} FamorCoins por las molestias')
    job14 = (f'fuiste un presidente corrupto durante 6 años y ganaste {recompensa} FamorCoins')
    trabajo = ([job0,job1,job2,job3,job4,job5,job6,job7,job8,job9,job10,job11,job12,job13,job14])
    msg = random.choice(trabajo)

    cluster_data.update_one({"id": user.id},{"$set":{"famorcoins": famorcoins + recompensa}})

    await salida(ctx,msg)
@client.command()
async def dinero(ctx):
    user = ctx.author
    datos = cluster_data.find_one({"id": user.id})
    famorcoins = datos["famorcoins"]
    msg = f"tienes {famorcoins} famorcoins"

    await salida(ctx,msg) 
@client.command()
async def salida(ctx,msg):
    author = ctx.author
    embed = discord.Embed(title = author.name,description = msg, color = 0x00ffff)
    await ctx.send(embed=embed)

client.run(token)

