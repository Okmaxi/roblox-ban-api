import discord
from discord.ext import commands
import requests

TOKEN = "MTQ5MDM1OTgwNTQ2OTEzNDkwOQ.GJbLCQ.bPZSy55TkBtCXyMf5XoLURTA1pPVrggoaiaSaE"
API_URL = "https://roblox-ban-api-hmxd.onrender.com"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔍 Obtener info Roblox
def get_roblox_user_info(user_id):
    try:
        user_res = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
        user_data = user_res.json()

        avatar_res = requests.get(
            f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false"
        )
        avatar_data = avatar_res.json()

        avatar_url = avatar_data["data"][0]["imageUrl"]

        return {
            "username": user_data.get("name", "Unknown"),
            "display": user_data.get("displayName", "Unknown"),
            "avatar": avatar_url
        }
    except:
        return {
            "username": "Unknown",
            "display": "Unknown",
            "avatar": None
        }

# 📜 Canal logs
def get_logs_channel(guild):
    return discord.utils.get(guild.text_channels, name="logs")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# 🔨 BAN
@bot.command()
async def gameban(ctx, user_id: int, *, reason=None):
    if not reason:
        await ctx.send("❌ Tenés que poner una razón", delete_after=3)
        return

    requests.post(f"{API_URL}/ban", json={"userId": user_id})

    # borrar comando (si puede)
    try:
        await ctx.message.delete()
    except:
        pass

    # mensaje limpio
    await ctx.send("✅ Task Done", delete_after=3)

    user = get_roblox_user_info(user_id)
    logs = get_logs_channel(ctx.guild)

    if logs:
        embed = discord.Embed(
            title="🚫 Player Banned",
            color=discord.Color.red()
        )

        embed.add_field(name="Display Name", value=user["display"], inline=True)
        embed.add_field(name="Username", value=user["username"], inline=True)
        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Admin", value=ctx.author.mention, inline=False)

        embed.set_thumbnail(url=user["avatar"])
        embed.set_footer(text=f"{ctx.author} • {ctx.message.created_at}")

        await logs.send(embed=embed)

# 🔓 UNBAN
@bot.command()
async def gameunban(ctx, user_id: int, *, reason=None):
    if not reason:
        await ctx.send("❌ Tenés que poner una razón", delete_after=3)
        return

    requests.post(f"{API_URL}/unban", json={"userId": user_id})

    try:
        await ctx.message.delete()
    except:
        pass

    await ctx.send("✅ Task Done", delete_after=3)

    user = get_roblox_user_info(user_id)
    logs = get_logs_channel(ctx.guild)

    if logs:
        embed = discord.Embed(
            title="✅ Player Unbanned",
            color=discord.Color.green()
        )

        embed.add_field(name="Display Name", value=user["display"], inline=True)
        embed.add_field(name="Username", value=user["username"], inline=True)
        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Admin", value=ctx.author.mention, inline=False)

        embed.set_thumbnail(url=user["avatar"])
        embed.set_footer(text=f"{ctx.author} • {ctx.message.created_at}")

        await logs.send(embed=embed)

# 👢 KICK
@bot.command()
async def gamekick(ctx, user_id: int, *, reason=None):
    if not reason:
        await ctx.send("❌ Tenés que poner una razón", delete_after=3)
        return

    requests.post(f"{API_URL}/kick", json={
        "userId": user_id,
        "reason": reason
    })

    try:
        await ctx.message.delete()
    except:
        pass

    await ctx.send("✅ Task Done", delete_after=3)

    user = get_roblox_user_info(user_id)
    logs = get_logs_channel(ctx.guild)

    if logs:
        embed = discord.Embed(
            title="👢 Player Kicked",
            color=discord.Color.orange()
        )

        embed.add_field(name="Display Name", value=user["display"], inline=True)
        embed.add_field(name="Username", value=user["username"], inline=True)
        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Admin", value=ctx.author.mention, inline=False)

        embed.set_thumbnail(url=user["avatar"])
        embed.set_footer(text=f"{ctx.author} • {ctx.message.created_at}")

        await logs.send(embed=embed)

bot.run(TOKEN)