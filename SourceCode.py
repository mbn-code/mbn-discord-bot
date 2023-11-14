import discord
from discord.ext import commands

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_logging_channel(self, guild_id):
        # Get the logging channel for a specific guild
        return await self.bot.http.get_guild_data(guild_id)

    async def set_logging_channel(self, guild_id, channel_id):
        # Set the logging channel for a specific guild
        await self.bot.http.edit_guild_data(guild_id, {'logging_channel': channel_id})

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load the LoggingCog
bot.add_cog(LoggingCog(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    # Set up logging channel on startup for all servers
    for guild in bot.guilds:
        await find_and_set_logging_channel(guild)

@bot.event
async def on_message(message):
    # Your code for understanding what people are writing can go here
    # For example, you might want to analyze the message content or perform some action
    
    # Log the message content and author in the specified channel
    log_channel_id = await get_logging_channel(message.guild)
    if log_channel_id:
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(f'**Message from {message.author}:** {message.content}')
    
    await bot.process_commands(message)

async def find_and_set_logging_channel(guild):
    # Automatically search for and set up a logging channel
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
            if "logging" in channel.name.lower():
                # Check if the channel name contains "logging"
                await set_logging_channel(guild.id, channel.id)
                print(f'Logging channel set to #{channel.name} in {guild.name}')
                return

    # If no channel with "logging" in its name is found, prompt the user
    await prompt_user_for_logging_channel(guild)

async def prompt_user_for_logging_channel(guild):
    # Prompt the user to specify a logging channel
    await guild.owner.send("I couldn't find a channel with 'logging' in its name. Please specify a channel by name or ID.")

    def check(message):
        return message.author == guild.owner and message.guild == guild

    try:
        response = await bot.wait_for('message', check=check, timeout=60)
        # Attempt to convert the response to a channel ID
        channel_id = int(response.content)
        await set_logging_channel(guild.id, channel_id)
        print(f'Logging channel set to #{channel_id} in {guild.name}')
    except (ValueError, asyncio.TimeoutError):
        print(f'No valid channel ID provided. Logging channel not set in {guild.name}')

async def get_logging_channel(guild):
    # Get the logging channel for the server
    cog = bot.cogs.get('LoggingCog')
    if cog:
        return await cog.get_logging_channel(guild.id)
    return None

async def set_logging_channel(guild_id, channel_id):
    # Set the logging channel for the server
    cog = bot.cogs.get('LoggingCog')
    if cog:
        await cog.set_logging_channel(guild_id, channel_id)
    else:
        print("LoggingCog not found.")

@bot.event
async def on_command(ctx):
    # Log every command used with the bot
    log_channel_id = await get_logging_channel(ctx.guild)
    if log_channel_id:
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(f'**Command used by {ctx.author}:** {ctx.message.content}')

@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason=None):
    # Kick a member
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked.')
    else:
        await ctx.send('You do not have the required permissions to kick members.')

@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason=None):
    # Ban a member
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')
    else:
        await ctx.send('You do not have the required permissions to ban members.')

@bot.command(name='clear')
async def clear(ctx, amount: int = 1):
    # Clear a specified number of messages in a channel
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{amount} messages cleared.', delete_after=5)
    else:
        await ctx.send('You do not have the required permissions to manage messages.')

@bot.command(name='mute')
async def mute(ctx, member: discord.Member):
    # Mute a member
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not mute_role:
            # Create the 'Muted' role if it doesn't exist
            mute_role = await ctx.guild.create_role(name='Muted', reason='Mute command setup')
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        await member.add_roles(mute_role, reason='Muted by command')
        await ctx.send(f'{member.mention} has been muted.')
    else:
        await ctx.send('You do not have the required permissions to mute members.')

@bot.command(name='unmute')
async def unmute(ctx, member: discord.Member):
    # Unmute a member
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role, reason='Unmuted by command')
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send(f'{member.mention} is not muted.')
    else:
        await ctx.send('You do not have the required permissions to unmute members.')

@bot.command(name='serverid')
async def server_id(ctx):
    # Display the server ID
    await ctx.send(f'The ID of this server is: {ctx.guild.id}')

# Run the bot with your token
def read_token():
    # Read the bot token from the 'token.key' file
    with open('token.key', 'r') as file:
        return file.read().strip()

bot.run(read_token())
