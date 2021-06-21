from discord.ext import commands
client = commands.Bot(command_prefix="!")
token = "tu token" #mira el episodio 1 si no sabes como conseguirlo

@client.event
async def on_ready():
    print("bot cargado")
@client.command()
async def saludo(ctx):
    await ctx.send("Hola!")
    
client.run(token)
