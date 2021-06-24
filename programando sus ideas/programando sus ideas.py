from discord.ext import commands
import discord
import random
import praw
import youtube_dl
token = "tu token del bot"#mira el episodio 1 de mi serie como crear un bot si no sabes como conseguirlo

reddit = praw.Reddit(client_id = "tu client de reddit",# si no sabes como hacerlo busca en youtube, yo no voy a hacer tutorial de esto pronto
                    client_secret = "tu client secret de reddit",
                    username = "tu usuario de reddit",
                    password = "tu contraseña de reddit",
                    user_agent = "cualquier cosa",
                    check_for_async=False)

client = commands.Bot(command_prefix = "*",)
@client.event
async def on_ready():
    discord.AllowedMentions.all 
    print('FamorTest listo')

@client.command(name = "meme",help = "envia un meme")
async def meme(ctx):
    subreddit = reddit.subreddit("SpanishMeme")#subreddit de donde sacar los memes
    memes = []
    top = subreddit.top(limit = 50)
    for submission in top:
        memes.append(submission)

    meme = random.choice(memes)
    nombre = meme.title
    imagen = meme.url

    embed = discord.Embed(title = nombre,color=0x00ffff)
    embed.set_image(url = imagen)
    embed.set_footer(text = "Memes provenientes de r/SpanishMeme")
    await ctx.send(embed=embed)
@client.command(name = "aww",help = "envia una imagen cute")
async def aww(ctx):
    subreddit = reddit.subreddit("aww")#subreddit de donde sacar los memes
    memes = []
    top = subreddit.top(limit = 50)
    for submission in top:
        memes.append(submission)

    meme = random.choice(memes)
    nombre = meme.title
    imagen = meme.url

    embed = discord.Embed(title = nombre,color=0x00ffff)
    embed.set_image(url = imagen)
    embed.set_footer(text = "imagenes provenientes de r/aww")
    await ctx.send(embed=embed)
    

#notificaciones de stream
@client.command()
async def stream(ctx,lugar):
    canal = client.get_channel(784218487940710413)
    if lugar == "1":
        await canal.send("@everyone Hola estoy en directo en Youtube ven a verme: https://www.youtube.com/channel/UCYHzFB7zN7xq4oPg7zXR-2w")
    elif lugar == "2":
        await canal.send("@everyone Hola estoy en directo en Twitch ven a verme: https://www.twitch.tv/famortech")
    elif lugar == "3":
        await canal.send("@everyone Hola estoy en directo en booyah ven a verme: (tu link super cool)")
    else:
        await ctx.send("opcion no valida")


#MUSICA
#todavia le faltan muchas cosas a este codigo no lo recomiendo
@client.command(name = "r")
async def play(ctx,url):
    if ctx.author.voice is None:
        await ctx.send("Unete a un canal de voz para empezar.")
        return
    vc = ctx.author.voice.channel
    try:
        await vc.connect()
    except:
        print("ya esta en el vc")
    ctx.voice_client.stop()
    YDL_OPTIONS = {'format': 'bestaudio','source_address': '0.0.0.0','post_processorss': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferedquality': '192'}]}
    FFMPEG_OPTIONS = {'options': '-vn'}
    voice_chat = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        webpage = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(source = webpage,**FFMPEG_OPTIONS)
        voice_chat.play(source)

@client.command(name = "d")
async def stop(ctx):
    voice_chat = ctx.voice_client
    await voice_chat.disconnect()
#no se si funcionen me dio floejra probarlos
@client.command(name = "p")
async def pause(ctx):
    voice_chat = ctx.voice_client
    await voice_chat.pause()
@client.command(name = "c")
async def resume(ctx):
    voice_chat = ctx.voice_client
    await voice_chat.resume()

client.run(rngmsg.token)   
