import datetime
from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord import app_commands
from responses import get_response
import random
import pytz
from datetime import datetime

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
SERVER_ID: Final[str] =os.getenv("GUILD_ID")
secret: Final[str] =os.getenv("SECRETS")

#intents

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

#bot setup

async def send_message(message: Message, user_message: str, username) -> None:
    if not user_message:
        print("Message was empty.")
        return
    try:
        responses: str = get_response(user_message, username)
        await message.channel.send(responses)
    except Exception as e:
        print(e)

#run bot
@client.event
async def on_ready() -> None:
    await tree.sync(guild=discord.Object(id=f"{SERVER_ID}"))
    await client.change_presence(activity=discord.Activity(name="over you...", type=3, ))
    print(f'{client.user} is now running')
#handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    if message.author == client.user:
        if user_message == "@here":
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
        return
    elif f"{secret}" in user_message:
        await message.delete()
        await message.author.kick(reason="HAHA GET TROLLED")
        print(f'{message.author} should be getting banned right about now')
        await message.channel.send(f"You see... {message.author} made a little oppsie. They belived typing that message could get someone banned, but instead, it bans them.")
        await message.channel.send("hehe")

    elif user_message == "!ssu":
        if f'{message.author}' == "yayblaze":
            await message.delete()
            embed = discord.Embed(title="Server Starting!", description="Join now!", colour=discord.Colour.green())
            embed.add_field(name="IP:",value="play.yayblazesmp.xyz", inline=False)
            embed.add_field(name="Version:", value="1.20.1", inline=False)
            embed.add_field(name="Mods:", value="Please visit #mods", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("You don't have permissions to do that. (L)")

    elif user_message == "!ssd":
        if f'{message.author}' == "yayblaze":
            await message.delete()
            embed = discord.Embed(title="Server Shutdown", description="The server is now shutdown. You will not be able to join.", colour=discord.Colour.red())
            embed.add_field(name="Want to play?", value="Contact YayBlaze if you want him to start the server.", inline=False)
            embed.add_field(name="", value="(unless it's an unreasonable time)", inline=True)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("You don't have permissions to do that. (L)")
    else:
        await send_message(message, user_message, username)


@tree.command(
    name="ping",
    description="Gives you the ping!",
    guild=discord.Object(id=f'{SERVER_ID}')
)
async def ping(interaction):
    bot_latency = round(client.latency*1000)
    await interaction.response.send_message(f"Pong! ... {bot_latency}ms")


@tree.command(
    name="roll",
    description="Rolls a 6-sided dice",
    guild=discord.Object(id=f"{SERVER_ID}")
)
async def roll(interation):
    await interation.response.send_message(f"You rolled: {random.randint(1, 6)}")



# class wyrbuttons(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#
#     @discord.ui.button(label="Option 2", style=discord.ButtonStyle.red)
#     async def op2(self, interation: discord.Interaction, button: discord.ui.Button):

@tree.command(
    name="wyr",
    description="Gives a 'would you rather' question people can vote on!",
    guild=discord.Object(id=f'{SERVER_ID}')
)
async def wyr(interation, option1: str, option2: str):
    embed = discord.Embed(title="Would you Rather",
                          description=f"{option1} or {option2}",
                          colour=discord.Colour.red())
    # embed.add_field(name="", value=f"Asked by {}")
    embed.timestamp = datetime.now()
    pst = pytz.timezone('US/Pacific')
    embed.set_footer(text=f"For legal reasons I must tell you what you choose will not actually happen")
    await interation.response.send_message("@here", embed=embed)
#main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
