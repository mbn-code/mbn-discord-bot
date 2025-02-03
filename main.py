import discord
from discord.ext import commands
import asyncio
import requests
from googlesearch import search 
import random
from discord.ext import tasks
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

user_credits = {}

# Remove hard-coded logging channel and use a dict for per-guild logging channel settings.
logging_channels = {}

MUTED_ROLE_NAME = 'Muted'

BOT_VERSION = "1.0.0"  # or update as needed

# New dictionaries for separate logging channels
general_logging_channels = {}
advanced_logging_channels = {}
mod_logging_channels = {}

# New helper functions for advanced logging
async def set_advanced_logging_channel(guild_id, channel_id):
    advanced_logging_channels[guild_id] = channel_id
    print(f"Set advanced logging channel for guild {guild_id} to {channel_id}")

async def get_advanced_logging_channel(guild):
    if guild is None:
        return None
    return advanced_logging_channels.get(guild.id)

async def prompt_user_for_advanced_logging_channel(guild):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_text_channel("advanced-logging", overwrites=overwrites)
    await set_advanced_logging_channel(guild.id, channel.id)
    await channel.send(f"Advanced logging channel created for {guild.name}.")
    print(f"Created advanced logging channel for {guild.name} with id {channel.id}")

# New helper functions for general logging
async def set_general_logging_channel(guild_id, channel_id):
    general_logging_channels[guild_id] = channel_id
    print(f"Set general logging channel for guild {guild_id} to {channel_id}")

async def get_general_logging_channel(guild):
    if guild is None:
        return None
    return general_logging_channels.get(guild.id)

async def prompt_user_for_general_logging_channel(guild):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_text_channel("general-logging", overwrites=overwrites)
    await set_general_logging_channel(guild.id, channel.id)
    await channel.send(f"General logging channel created for {guild.name}.")
    print(f"Created general logging channel for {guild.name} with id {channel.id}")

# New helper functions for moderator logging
async def set_mod_logging_channel(guild_id, channel_id):
    mod_logging_channels[guild_id] = channel_id
    print(f"Set moderator logging channel for guild {guild_id} to {channel_id}")

async def get_mod_logging_channel(guild):
    if guild is None:
        return None
    return mod_logging_channels.get(guild.id)

async def prompt_user_for_mod_logging_channel(guild):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_text_channel("moderator-logging", overwrites=overwrites)
    await set_mod_logging_channel(guild.id, channel.id)
    await channel.send(f"Moderator logging channel created for {guild.name}.")
    print(f"Created moderator logging channel for {guild.name} with id {channel.id}")

# Combined function to find or create all logging channels
async def find_and_set_all_logging_channels(guild):
    if guild is None:
        return
    adv_set = False
    gen_set = False
    mod_set = False
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
            name = channel.name.lower()
            if "advanced-logging" in name:
                await set_advanced_logging_channel(guild.id, channel.id)
                adv_set = True
                print(f"Advanced logging channel set to #{channel.name} in {guild.name}")
            elif "general-logging" in name:
                await set_general_logging_channel(guild.id, channel.id)
                gen_set = True
                print(f"General logging channel set to #{channel.name} in {guild.name}")
            elif "moderator-logging" in name:
                await set_mod_logging_channel(guild.id, channel.id)
                mod_set = True
                print(f"Moderator logging channel set to #{channel.name} in {guild.name}")
    if not adv_set:
        await prompt_user_for_advanced_logging_channel(guild)
    if not gen_set:
        await prompt_user_for_general_logging_channel(guild)
    if not mod_set:
        await prompt_user_for_mod_logging_channel(guild)

async def find_and_set_bot_channel(guild):
    # Search for a text channel with "bot" in its name; if exists, do nothing.
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) and "bot" in channel.name.lower() and channel.permissions_for(guild.me).send_messages:
            return  # Channel exists; skip creating a new one
    # Define permission overwrites: deny view for @everyone; allow for owner and bot.
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    # Create the bot channel with specified overwrites.
    bot_channel = await guild.create_text_channel("bot", overwrites=overwrites)
    await bot_channel.send(f"Bot version {BOT_VERSION} is online and ready in {guild.name}!")
    print(f"Created bot channel in guild {guild.name} with id {bot_channel.id}")

# New background task for rotating bot status
status_messages = [
    "Serving many guilds!",
    "Type !help for commands",
    "Keeping logs up-to-date",
    "Recording activity...",
    "Watching over the server"
]

@tasks.loop(minutes=10)
async def rotate_status():
    await bot.change_presence(activity=discord.Game(random.choice(status_messages)))

# New background task: GitHub Integration - post latest public event from 'mbn-code'
@tasks.loop(minutes=30)
async def github_integration():
    url = "https://api.github.com/users/mbn-code/events/public"
    try:
        response = requests.get(url)
        response.raise_for_status()
        events = response.json()
        if events:
            latest_event = events[0]
            event_type = latest_event.get("type", "Unknown")
            repo_name = latest_event.get("repo", {}).get("name", "Unknown")
            created_at = latest_event.get("created_at", "")
            description = f"{event_type} on {repo_name} at {created_at}"
            # For each guild, post/update in a "github-updates" channel
            for guild in bot.guilds:
                channel = discord.utils.get(guild.text_channels, name="github-updates")
                if not channel:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=True),
                        guild.owner: discord.PermissionOverwrite(view_channel=True),
                        guild.me: discord.PermissionOverwrite(view_channel=True)
                    }
                    channel = await guild.create_text_channel("github-updates", overwrites=overwrites)
                await channel.send(f"GitHub Update: {description}")
    except Exception as e:
        print(f"GitHub integration error: {e}")

# New background task: Server Dashboard - post server statistics periodically
@tasks.loop(hours=1)
async def update_server_dashboard():
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="dashboard")
        if not channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=True),
                guild.owner: discord.PermissionOverwrite(view_channel=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            channel = await guild.create_text_channel("dashboard", overwrites=overwrites)
        embed = discord.Embed(title=f"{guild.name} Dashboard", color=discord.Color.blue())
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Total Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
        embed.set_footer(text=f"Dashboard updated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
        await channel.send(embed=embed)

# New background task: Event Reminder - periodically send a community reminder
@tasks.loop(hours=6)
async def event_reminders():
    reminder_message = "Remember to check out our scheduled events and engage with the community!"
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="announcements")
        if channel:
            await channel.send(reminder_message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    # Set up logging channel on startup for all servers
    for guild in bot.guilds:
        await find_and_set_all_logging_channels(guild)
        await find_and_set_bot_channel(guild)
    rotate_status.start()
    github_integration.start()       # start GitHub integration
    update_server_dashboard.start()  # start dashboard updates
    event_reminders.start()          # start event reminders
    for guild in bot.guilds:
        welcome = discord.utils.get(guild.text_channels, name="welcome")
        if not welcome:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=True),
                guild.owner: discord.PermissionOverwrite(view_channel=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            welcome = await guild.create_text_channel("welcome", overwrites=overwrites)
        print(f"Welcome channel for {guild.name}: {welcome.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Skip logging for DMs (where guild is None)
    if message.guild is None:
        await bot.process_commands(message)
        return
    
    # NSFW attachment check for gif files
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.gif'):
                pass  # Added to prevent empty block error

    # Log the message in the specified logging channel
    adv_channel = bot.get_channel(await get_advanced_logging_channel(message.guild))
    if adv_channel:
        await adv_channel.send(f"[ADVANCED] MsgID {message.id} | Author: {message.author} | Channel: {message.channel.name} | Content: {message.content}")

    gen_channel = bot.get_channel(await get_general_logging_channel(message.guild))
    if gen_channel:
        await gen_channel.send(f"Message from {message.author}: {message.content}")

    mod_channel = bot.get_channel(await get_mod_logging_channel(message.guild))
    if mod_channel:
        await mod_channel.send(f"{message.author} sent a message.")

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    channel_id = await get_logging_channel(before.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Edited message content - Before: {before.content}, After: {after.content}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_message_delete(message):
    channel_id = await get_logging_channel(message.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Deleted message content: {message.content}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    # Handle poll vote if a number emoji (1️⃣ to 9️⃣) is used
    if reaction.emoji in [f"{i}\u20e3" for i in range(1, 10)]:
        option_index = int(reaction.emoji[0]) - 1
        await reaction.message.channel.send(f"{user.mention} voted for Option {option_index + 1}!")
    else:
        guild = reaction.message.guild
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Reaction added to message content: {reaction.message.content}")
        else:
            print('Logging channel not set for this server.')

@bot.event
async def on_reaction_remove(reaction, user):
    guild = reaction.message.guild
    channel_id = await get_logging_channel(guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Reaction removed from message content: {reaction.message.content}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_member_join(member):
    channel_id = await get_logging_channel(member.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member joined: {member.name}")
    else:
        print('Logging channel not set for this server.')
    # Auto assign a "Member" role
    default_role = discord.utils.get(member.guild.roles, name="Member")
    if not default_role:
        default_role = await member.guild.create_role(name="Member")
    await member.add_roles(default_role)
    # Send welcome message to the welcome channel if it exists
    welcome = discord.utils.get(member.guild.text_channels, name="welcome")
    if welcome:
        await welcome.send(f"Welcome {member.mention} to {member.guild.name}! Enjoy your stay.")
    # Send a direct message to the new member
    try:
        await member.send(f"Hi {member.name}, welcome to {member.guild.name}!")
    except Exception:
        pass

@bot.event
async def on_member_remove(member):
    channel_id = await get_logging_channel(member.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member left: {member.name}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_member_update(before, after):
    channel_id = await get_logging_channel(before.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member update - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_guild_join(guild):
    await find_and_set_logging_channel(guild)
    channel_id = await get_logging_channel(guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Bot joined server: {guild.name}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_guild_remove(guild):
    # Optionally remove the logging channel setting
    logging_channels.pop(guild.id, None)
    print(f"Removed logging channel setting for server: {guild.name}")

@bot.event
async def on_guild_update(before, after):
    channel_id = await get_logging_channel(before)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Server update - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not set for this server.')

@bot.event
async def on_guild_role_create(role):
    channel_id = await get_logging_channel(role.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Role created in server: {role.name}")
    else:
        print('Logging channel not found for guild: ', role.guild.name)

@bot.event
async def on_guild_role_delete(role):
    # Use per-guild logging channel instead of LOGGING_CHANNEL_ID
    channel_id = await get_logging_channel(role.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Role deleted in server: {role.name}")
    else:
        print('Logging channel not found for guild: ', role.guild.name)

@bot.event
async def on_guild_role_update(before, after):
    channel_id = await get_logging_channel(before.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Role update in server - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not found for guild: ', before.guild.name)

@bot.event
async def on_member_ban(guild, user):
    channel_id = await get_logging_channel(guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member banned from server: {user.name}")
    else:
        print('Logging channel not found for guild: ', guild.name)

@bot.event
async def on_member_unban(guild, user):
    channel_id = await get_logging_channel(guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member unbanned from server: {user.name}")
    else:
        print('Logging channel not found for guild: ', guild.name)

@bot.event
async def on_voice_state_update(member, before, after):
    channel_id = await get_logging_channel(member.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Voice state update - Member: {member.name}, Before: {before.channel}, After: {after.channel}")
    else:
        print('Logging channel not found for guild: ', member.guild.name)

@bot.event
async def on_user_update(before, after):
    # For each guild in which the user is a member, log the update
    for guild in bot.guilds:
        if guild.get_member(before.id):
            channel_id = await get_logging_channel(guild)
            if channel_id:
                logging_channel = bot.get_channel(channel_id)
                if logging_channel:
                    await logging_channel.send(f"User update in {guild.name} - Before: {before.name}, After: {after.name}")

@bot.event
async def on_member_presence_update(member, before, after):
    channel_id = await get_logging_channel(member.guild)
    if channel_id:
        logging_channel = bot.get_channel(channel_id)
        if logging_channel:
            await logging_channel.send(f"Member presence update - Member: {member.name}, Before: {before.activities}, After: {after.activities}")
    else:
        print('Logging channel not found for guild: ', member.guild.name)

#@bot.event
#async def on_typing(channel, user, when):
#    # Log typing event
#    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
#    if logging_channel:
#        await logging_channel.send(f"User typing in channel: {user.name}, Channel: {channel.name}")
#    else:
#        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_integration_join(integration):
    guild = bot.get_guild(integration.guild_id)
    if guild:
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Bot joined as integration in {guild.name}: {integration.name}")
        else:
            print('Logging channel not found for guild: ', guild.name)
    else:
        print('Guild not found for integration: ', integration.name)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id:
        guild = bot.get_guild(payload.guild_id)
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Raw reaction added to message ID: {payload.message_id}")
        else:
            print('Logging channel not set for guild id:', payload.guild_id)
    else:
        print('Raw reaction add: payload has no guild_id.')

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id:
        guild = bot.get_guild(payload.guild_id)
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Raw reaction removed from message ID: {payload.message_id}")
        else:
            print('Logging channel not set for guild id:', payload.guild_id)
    else:
        print('Raw reaction remove: payload has no guild_id.')

@bot.event
async def on_raw_message_delete(payload):
    if payload.guild_id:
        guild = bot.get_guild(payload.guild_id)
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Raw message deleted from channel ID: {payload.channel_id}")
        else:
            print('Logging channel not set for guild id:', payload.guild_id)
    else:
        print('Raw message delete: payload has no guild_id.')

@bot.event
async def on_raw_bulk_message_delete(payload):
    if payload.guild_id:
        guild = bot.get_guild(payload.guild_id)
        channel_id = await get_logging_channel(guild)
        if channel_id:
            logging_channel = bot.get_channel(channel_id)
            if logging_channel:
                await logging_channel.send(f"Raw bulk message deleted from channel ID: {payload.channel_id}")
        else:
            print('Logging channel not set for guild id:', payload.guild_id)
    else:
        print('Raw bulk message delete: payload has no guild_id.')



async def find_and_set_logging_channel(guild):
    # Skip if no guild object is provided (e.g., DM channels)
    if guild is None:
        return
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
            if "logging" in channel.name.lower():
                await set_logging_channel(guild.id, channel.id)
                print(f'Logging channel set to #{channel.name} in {guild.name}')
                return
    await prompt_user_for_logging_channel(guild)

async def prompt_user_for_logging_channel(guild):
    # Define permission overwrites: deny view for @everyone; allow for owner and bot.
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.owner: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    # Create a new text channel named "logging" with specified overwrites.
    channel = await guild.create_text_channel("logging", overwrites=overwrites)
    await set_logging_channel(guild.id, channel.id)
    await channel.send(f"Successfully created logging channel for {guild.name} ready to log")
    print(f"Created logging channel for guild {guild.name} with id {channel.id}")

async def get_logging_channel(guild):
    if guild is None:
        return None
    return logging_channels.get(guild.id)

async def set_logging_channel(guild_id, channel_id):
    logging_channels[guild_id] = channel_id
    print(f"Set logging channel for guild {guild_id} to {channel_id}")


@bot.command(name='mute')
async def mute(ctx, member: discord.Member, *, reason=None):
    # Mute a member
    mute_role = discord.utils.get(ctx.guild.roles, name=MUTED_ROLE_NAME)
    if not mute_role:
        # Create the 'Muted' role if it doesn't exist
        mute_role = await ctx.guild.create_role(name=MUTED_ROLE_NAME, reason='Mute command setup')
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} has been muted.')

@bot.command(name='unmute')
async def unmute(ctx, member: discord.Member):
    # Unmute a member
    mute_role = discord.utils.get(ctx.guild.roles, name=MUTED_ROLE_NAME)
    if mute_role and mute_role in member.roles:
        await member.remove_roles(mute_role, reason='Unmuted by command')
        await ctx.send(f'{member.mention} has been unmuted.')
    else:
        await ctx.send(f'{member.mention} is not muted.')

@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason=None):
    # Ban a member
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

@bot.command(name='timeout')
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    # Temporarily mute a member (timeout)
    mute_role = discord.utils.get(ctx.guild.roles, name=MUTED_ROLE_NAME)
    if not mute_role:
        # Create the 'Muted' role if it doesn't exist
        mute_role = await ctx.guild.create_role(name=MUTED_ROLE_NAME, reason='Timeout command setup')
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} has been timed out for {duration} seconds.')

    # Remove the mute role after the specified duration
    await asyncio.sleep(duration)
    await member.remove_roles(mute_role, reason='Timeout duration expired')
    await ctx.send(f'{member.mention} has been unmuted after the timeout period.')

@bot.command()
async def clear(ctx, amount: int):
    # Check if the user has the manage_messages permission
    if ctx.author.guild_permissions.manage_messages:
        # Delete messages, including the command message
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages cleared by {ctx.author.mention}.", delete_after=5)
    else:
        await ctx.send("You don't have the required permissions to use this command.")


@bot.command()
async def role(ctx):
    # Update roles to map emoji to a tuple (role_id, role_name)
    roles = {
        "🟠": (812469616226861057, "Skid role"),
        "👥": (798867993295716352, "Member role"),
        "🟢": (800064598102376478, "Greenhat"),
        "⚪": (808279662307704853, "Whitehat"),
        "⚫": (800434462785667082, "Greyhats"),
        "🔴": (891761997220294706, "C language"),
        "🔵": (800164451017949224, "Programmer"),
        "🟡": (891761884494172220, "Python"),
        "🇮🇳": (None, "Indian Tech Support"),  # new role
        "📱": (None, "APP"),                    # new role
    }

    embed = discord.Embed(
        title="Choose a Role",
        description="React with the emoji corresponding to the role you want.",
        color=discord.Color.blue()
    )

    # For each emoji, try to fetch the role; if not found, create it.
    for emoji, (role_id, role_name) in roles.items():
        role_obj = None
        if role_id:
            role_obj = ctx.guild.get_role(role_id)
        if not role_obj:
            role_obj = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role_obj:
            role_obj = await ctx.guild.create_role(name=role_name)
        embed.add_field(name=emoji, value=role_obj.mention, inline=True)

    if not embed.fields:
        await ctx.send("Error: No roles found.")
        return

    message = await ctx.send(embed=embed)
    for emoji in roles.keys():
        await message.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in roles

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        selected = roles[str(reaction.emoji)]
        role_obj = None
        if selected[0]:
            role_obj = ctx.guild.get_role(selected[0])
        if not role_obj:
            role_obj = discord.utils.get(ctx.guild.roles, name=selected[1])
        if role_obj:
            await ctx.author.add_roles(role_obj)
            await ctx.send(f"You have been given the role: {role_obj.name}")
        else:
            await ctx.send("Error: Role not found.")
        await message.clear_reactions()
    except asyncio.TimeoutError:
        await ctx.send("Role selection timed out. Please try again.")
        await message.clear_reactions()

@bot.command()
async def post(ctx):
    # Check if the user has posted a valid message
    valid_post = validate_post(ctx.message.content)

    if valid_post:
        # Assign credits to the user
        user_id = str(ctx.author.id)
        user_credits[user_id] = user_credits.get(user_id, 0) + 1

        await ctx.send(f"Thanks for your post, {ctx.author.mention}! You earned 1 credit.")
    else:
        await ctx.send(f"Sorry, {ctx.author.mention}, your post is not valid. Please try again with a valid post.")

@bot.command()
async def credits(ctx):
    # Check the user's credits
    user_id = str(ctx.author.id)
    credits = user_credits.get(user_id, 0)

    await ctx.send(f"{ctx.author.mention}, you have {credits} credits.")

@bot.command()
async def buy_role(ctx, role_name, cost):
    # Check if the user has enough credits to buy the role
    user_id = str(ctx.author.id)
    credits = user_credits.get(user_id, 0)

    try:
        cost = int(cost)
        if credits >= cost:
            # Assign the role to the user
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                await ctx.author.add_roles(role)
                user_credits[user_id] -= cost
                await ctx.send(f"Congratulations, {ctx.author.mention}! You bought the {role_name} role for {cost} credits.")
            else:
                await ctx.send(f"Error: Role not found.")
        else:
            await ctx.send(f"Sorry, {ctx.author.mention}, you don't have enough credits to buy the {role_name} role.")
    except ValueError:
        await ctx.send("Error: Please provide a valid cost as an integer.")

def validate_post(content):
    # Always return True, making every post valid
    return True


@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 2 or len(options) > 10:
        await ctx.send("Please provide at least 2 and at most 10 options for the poll.")
        return

    # Create poll embed
    embed = discord.Embed(title=question, color=discord.Color.blue())

    for index, option in enumerate(options, start=1):
        embed.add_field(name=f"Option {index}", value=option, inline=False)

    embed.set_footer(text=f"Poll created by {ctx.author.display_name}")

    # Send poll message
    poll_message = await ctx.send(embed=embed)

    # Add reactions for voting
    for emoji, _ in zip(range(1, len(options) + 1), options):
        await poll_message.add_reaction(f"{emoji}\u20e3")  # Adding emoji numbers 1-9

@bot.command()
async def weather(ctx, city):
    base_url = "https://www.metaweather.com/api/location/search/"
    params = {"query": city}

    try:
        response = requests.get(base_url, params=params)
        locations = response.json()

        if not locations:
            await ctx.send("City not found.")
            return

        woeid = locations[0]["woeid"]
        weather_url = f"https://www.metaweather.com/api/location/{woeid}/"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        temperature = weather_data["consolidated_weather"][0]["the_temp"]
        description = weather_data["consolidated_weather"][0]["weather_state_name"]
        
        await ctx.send(f"The weather in {city} is {temperature:.2f}°C with {description}.")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while fetching the weather.")


@bot.command(name='warn')
async def warn(ctx, member: discord.Member, *, reason=None):
    # Warn a member
    # Note: You can implement a more sophisticated warning system if needed
    await ctx.send(f'{member.mention}, you have been warned for: {reason}')

@bot.command(name='purge')
async def purge(ctx, limit: int):
    # Purge messages
    await ctx.channel.purge(limit=limit)
    await ctx.send(f'{limit} messages have been deleted.')

@bot.command(name='purgeuser')
async def purgeuser(ctx, member: discord.Member):
    # Purge messages from a specific user
    await ctx.channel.purge(limit=None, check=lambda m: m.author == member)
    await ctx.send(f'{member.mention}\'s messages have been deleted.')


@bot.command()
async def userinfo(ctx, user: discord.User = None):
    # If no user is specified, default to the command author
    user = user or ctx.author

    # Create an embed with user information
    embed = discord.Embed(title="User Information", color=discord.Color.blue())
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(user, 'joined_at') else "N/A", inline=True)

    # Send the embed message
    await ctx.send(embed=embed)

# Replace with the ID of the support channel where tickets will be sent
SUPPORT_CHANNEL_ID = 1174453854247604326

@bot.command()
async def ticket(ctx, *args):
    # Combine the arguments into a single string
    ticket_content = ' '.join(args)

    # Get the support channel
    support_channel = bot.get_channel(SUPPORT_CHANNEL_ID)

    if support_channel:
        # Create an embed with ticket information
        embed = discord.Embed(title="New Support Ticket", color=discord.Color.gold())
        embed.add_field(name="User", value=ctx.author.mention, inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        embed.add_field(name="Ticket Content", value=ticket_content, inline=False)

        # Send the embed message to the support channel
        await support_channel.send(embed=embed)

        await ctx.send(f"Your support ticket has been submitted. Support will assist you soon.")
    else:
        await ctx.send("Error: Support channel not found. Please contact the server administrator.")



@bot.command(brief="Fetch information about a specific CVE entry.")
async def cve(ctx, cve_id):
    # Construct the URL for the NVD API
    api_url = f"https://services.nvd.nist.gov/rest/json/cve/{cve_id}"

    try:
        # Send a request to the NVD API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Print the entire API response
        print(response.json())

        # Parse the JSON response
        cve_info = response.json()

        # Check if the response contains CVE information
        if 'result' in cve_info and 'CVE_Items' in cve_info['result']:
            # Extract relevant information
            cve_item = cve_info['result']['CVE_Items'][0]['cve']
            cve_description = cve_item['description']['description_data'][0]['value']

            # Create an embed with CVE information
            embed = discord.Embed(title=f"CVE Information: {cve_id}", color=discord.Color.gold())
            embed.add_field(name="Description", value=cve_description, inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

            # Send the embed message
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No information found for CVE ID: {cve_id}")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            await ctx.send(f"No information found for CVE ID: {cve_id}")
            await ctx.send(f"Error fetching CVE information: {http_err}")
        else:
            await ctx.send(f"Error fetching CVE information: {http_err}")

@bot.command(brief="Search Stack Overflow for a programming question.")
async def stackoverflow(ctx, *question):
    question = ' '.join(question)
    try:
        # Use the googlesearch library to search Stack Overflow
        results = list(search(f"{question} site:stackoverflow.com"))

        if results:
            # Display the first Stack Overflow result in a Discord message
            await ctx.send(f"Stack Overflow result for '{question}':\n{results[0]}")
        else:
            await ctx.send(f"No Stack Overflow results found for '{question}'")

    except Exception as e:
        await ctx.send(f"Error searching Stack Overflow: {e}")

@bot.command(brief="Search GitHub for a repository and display the one with the most stars.")
async def github(ctx, *repository_name):
    repository_name = ' '.join(repository_name)
    try:
        # Construct the URL for the GitHub search API
        github_api_url = f"https://api.github.com/search/repositories?q={repository_name}&sort=stars&order=desc"

        # Send a request to the GitHub API
        response = requests.get(github_api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        github_results = response.json()

        # Check if there are any search results
        if 'items' in github_results and github_results['items']:
            # Extract information about the repository with the most stars
            top_repo = github_results['items'][0]
            repo_name = top_repo['name']
            repo_url = top_repo['html_url']
            stars = top_repo['stargazers_count']

            # Display information about the top repository in a Discord message
            await ctx.send(f"Top GitHub repository for '{repository_name}':\n"
                           f"Name: {repo_name}\nStars: {stars}\nURL: {repo_url}")
        else:
            await ctx.send(f"No GitHub repositories found for '{repository_name}'")

    except requests.exceptions.HTTPError as http_err:
        await ctx.send(f"Error fetching GitHub repository information: {http_err}")

@bot.command(brief="Show available commands and their parameters.")
async def commands(ctx):
    # Create an embed with the command list and parameters
    embed = discord.Embed(title="Available Commands", color=discord.Color.green())

    for command in bot.commands:
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        params = ' '.join([f"<{param}>" for param in command.clean_params.keys()])
        command_info = f"**{command.name} {params}** - {command.brief}"
        embed.add_field(name=command.name, value=command_info, inline=False)

    # Use the display_name attribute from the Member object
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")

    # Send the embed message
    await ctx.send(embed=embed)

# Disable the default help command if needed
bot.remove_command('help')

@bot.command(name='help')
async def help_command(ctx, category: str = None):
    if category is None:
        response = ("Usage: !help <category>\n"
                    "Available categories: moderation, fun, utility, information, misc")
    else:
        cat = category.lower()
        if cat == "moderation":
            response = ("Moderation commands:\n"
                        " - mute\n - unmute\n - ban\n - timeout\n - purge\n - purgeuser\n - warn")
        elif cat == "fun":
            response = ("Fun commands:\n"
                        " - poll\n - role")
        elif cat == "utility":
            response = ("Utility commands:\n"
                        " - weather\n - ticket\n - credits\n - buy_role")
        elif cat == "information":
            response = ("Information commands:\n"
                        " - userinfo\n - cve\n - stackoverflow\n - github")
        elif cat == "misc":
            response = ("Misc commands:\n"
                        " - post\n - commands")
        else:
            response = ("Unknown category. Available categories: moderation, fun, utility, information, misc")
    await ctx.send(response)

# New suggestion command for automatic suggestion posting with reactions
@bot.command(brief="Submit a suggestion for the server.")
async def suggest(ctx, *, suggestion: str):
    suggestions_channel = discord.utils.get(ctx.guild.text_channels, name="suggestions")
    if not suggestions_channel:
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.owner: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        suggestions_channel = await ctx.guild.create_text_channel("suggestions", overwrites=overwrites)
    embed = discord.Embed(title="New Suggestion", description=suggestion, color=discord.Color.blurple())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    message = await suggestions_channel.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    await ctx.send(f"Suggestion submitted in {suggestions_channel.mention}.")

@bot.command(brief="Display information about the server.")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.purple())
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Owner", value=str(guild.owner), inline=True)
    embed.add_field(name="Region", value=str(guild.region) if hasattr(guild, 'region') else "N/A", inline=True)
    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

# Run the bot with your token
def read_token():
    # Read the bot token from the 'token.key' file
    with open('token.key', 'r') as file:
        return file.read().strip()

bot.run(read_token())