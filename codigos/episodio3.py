from discord.ext import commands
from pymongo import MongoClient
import random
import discord

cluster = MongoClient("tu base de datos") # mira el episodio 2 si no sabes como crear una
cluster_data = cluster["Discord"]["Bot"]#dependen de tu base de datos, mira el episodio 2 si no sabes como crear una
client = commands.Bot(command_prefix="!")

token = "tu token"#el token de tu bot, mira el episodio 1 si no sabes donde conseguirlo

roles = ["nivel2","nivel3","nivel5"]
niveles = [2,3,5]
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
        cuenta = {"id": user.id,"nombre": nom, "famorcoins": 200,"xp":100}
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
async def salida(ctx,msg):
    author = ctx.author
    embed = discord.Embed(title = author.name,description = msg, color = 0x00ffff)
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def actualizardatos(ctx):
    cluster_data.update_many({"xp":{"$exists": False}},{"$set":{"xp": 100}})

@client.listen()
async def on_message(ctx):
    user = ctx.author
    datos = cluster_data.find_one({"id": user.id})
    await abrir_cuenta(user)
    if not ctx.author.bot:
        xp = datos["xp"]
        cluster_data.update_one({"id": user.id},{"$set":{"xp": xp + 10}})

        nivel = 0
        while True:
            if xp < ((50*(nivel **2))+(20*(nivel-1))):
                break
            nivel += 1
        xp -= ((50*((nivel - 1)**2))+(50*(nivel-1)))
        if xp == 0:
            embed = discord.Embed(description = f"{user.mention} Subiste al nivel **{nivel}**!",color = 0x00008B)
            embed.set_thumbnail(url = user.avatar_url)
            await ctx.channel.send(embed = embed)

            for i in range(len(roles)):
                if nivel == niveles[i]:
                    await user.add_roles(discord.utils.get(user.guild.roles,name = roles[i]))
                    embed = discord.Embed(description = f"{user.mention} ganaste el rol **{roles[i]}**")
                    embed.set_thumbnail(url = user.avatar_url)
                    await ctx.channel.send(embed = embed)

@client.command()
async def estadisticas(ctx,usuario:discord.User = None):
    if usuario == None:
        usuario = ctx.author
    await abrir_cuenta(usuario)
    datos = cluster_data.find_one({"id": usuario.id})
    famorcoins = datos["famorcoins"]
    xp = datos["xp"]
    nivel = 0
    top = 0

    while True:
        if xp < ((50*(nivel **2))+(20*(nivel-1))):
            break
        nivel += 1
    xp -= ((50*((nivel - 1)**2))+(50*(nivel-1)))

    progreso = int(xp/((nivel*100)/10))
    tops = cluster_data.find().sort("famorcoins",-1)
    for x in tops:
        top += 1
        if datos["id"] == x["id"]:
            break
    embed = discord.Embed(tittle = f"estadisticas de {usuario.name}",color = 0x00008B)
    embed.add_field(name = "Nombre", value = usuario.mention,inline = True)
    embed.add_field(name = "XP", value = f"{xp}/{int(200*((1/2)*nivel))}",inline = True)
    embed.add_field(name = "Nivel", value = nivel,inline = True)
    embed.add_field(name = "FamorCoins", value = famorcoins,inline = True)
    embed.add_field(name = "Top", value = f"{top}/{ctx.guild.member_count}",inline = True)
    embed.add_field(name = "Progreso", value = progreso * ":blue_square:" + (10-progreso) * ":white_large_square:",inline = False)
    embed.set_thumbnail(url = usuario.avatar_url)
    await ctx.send(embed = embed)
client.run(token)

