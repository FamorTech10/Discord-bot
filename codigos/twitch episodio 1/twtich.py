from twitchio.ext import commands

bot = commands.Bot(
    irc_token="tu token",# tu token, se obtiene con el link en la descripcion
    client_id="tu client id", #tu client id, se obtiene en twitch developers
    client_secret="tu client secret", #tu client secret, se obtiene en twitch developers
    prefix="!", #el prefix con el que contesta tu bot
    nick="bot", # el apodo de tu bot (no es visible)
    initial_channels=[""] #los canales donde va a estar activo el bot
)

@bot.event
async def event_ready():
    print("famorbot conectado")

@bot.command(name = "siguiendodesde")
async def followage(ctx):
    info = await bot.get_follow(from_id=ctx.author.id,to_id="tu id") #para tener tu id escribe !id desde tu cuenta donde vas a hacer directo
    follow_info = info["followed_at"]
    siguiendo_desde = (follow_info[:10])
    await ctx.send(f"{ctx.author.name} es seguidor desde {siguiendo_desde}")

@bot.command(name = "id")# lo puedes borrar despues de obtener tu id
async def id(ctx):
    print(ctx.author.id)

bot.run()