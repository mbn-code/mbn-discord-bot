import discord
from discord.ext import commands
import asyncio
import requests
from googlesearch import search 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

user_credits = {}

LOGGING_CHANNEL_ID = 798938315582734346
LOGGING_CHANNEL_NAME = 'logging'

MUTED_ROLE_NAME = 'Muted'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    # Set up logging channel on startup for all servers
    for guild in bot.guilds:
        await find_and_set_logging_channel(guild)

@bot.event
async def on_message(message):
    # Log all messages in the specified channel
    log_channel_id = await get_logging_channel(message.guild)
    if log_channel_id:
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            await log_channel.send(f'**Message from {message.author}:** {message.content}')
    
    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    # Log edited message content
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Edited message content - Before: {before.content}, After: {after.content}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_message_delete(message):
    # Log deleted message content
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Deleted message content: {message.content}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_reaction_add(reaction, user):
    # Log reacted message content
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Reaction added to message content: {reaction.message.content}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_reaction_remove(reaction, user):
    # Log removed reaction from message content
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Reaction removed from message content: {reaction.message.content}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_message(message):
    # Check if the message has a gif
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.gif'):
                # Send a request to the NSFW detection API
                response = requests.post('http://localhost:8000/predict', json={'url': attachment.url})
                is_nsfw = response.json()['is_nsfw']
                if is_nsfw:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, your message was deleted because it contained NSFW content.")
@bot.event
async def on_member_join(member):
    # Log member join
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member joined: {member.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_member_remove(member):
    # Log member leave
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member left: {member.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_member_update(before, after):
    # Log member update
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member update - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_join(guild):
    # Log when the bot joins a server
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Bot joined server: {guild.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_remove(guild):
    # Log when the bot is removed from a server
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Bot removed from server: {guild.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_update(before, after):
    # Log server update
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Server update - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_role_create(role):
    # Log created role in a server
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Role created in server: {role.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_role_delete(role):
    # Log deleted role in a server
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Role deleted in server: {role.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_guild_role_update(before, after):
    # Log updated role in a server
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Role update in server - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_member_ban(guild, user):
    # Log member ban
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member banned from server: {user.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_member_unban(guild, user):
    # Log member unban
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member unbanned from server: {user.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_voice_state_update(member, before, after):
    # Log voice state update
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Voice state update - Member: {member.name}, Before: {before.channel}, After: {after.channel}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_user_update(before, after):
    # Log user update
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"User update - Before: {before.name}, After: {after.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_member_presence_update(member, before, after):
    # Log member presence update
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Member presence update - Member: {member.name}, Before: {before.activities}, After: {after.activities}")
    else:
        print('Logging channel not found. Please check the channel ID.')

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
    # Log when the bot joins as an integration
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Bot joined as integration: {integration.name}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_raw_reaction_add(payload):
    # Log raw reaction add (includes raw data)
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Raw reaction added to message ID: {payload.message_id}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_raw_reaction_remove(payload):
    # Log raw reaction remove (includes raw data)
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Raw reaction removed from message ID: {payload.message_id}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_raw_message_delete(payload):
    # Log raw message delete (includes raw data)
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Raw message deleted from channel ID: {payload.channel_id}")
    else:
        print('Logging channel not found. Please check the channel ID.')

@bot.event
async def on_raw_bulk_message_delete(payload):
    # Log raw bulk message delete (includes raw data)
    logging_channel = bot.get_channel(LOGGING_CHANNEL_ID)
    if logging_channel:
        await logging_channel.send(f"Raw bulk message deleted from channel ID: {payload.channel_id}")
    else:
        print('Logging channel not found. Please check the channel ID.')



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
    # Define the roles that users can choose
    roles = {
        "🟠": 812469616226861057, # skid role 
        "👥": 798867993295716352, # member role
        "🟢": 800064598102376478,  # Greenhat
        "⚪": 808279662307704853,  # Whitehat
        "⚪": 800434462785667082,  # Greyhats
        "🔴": 891761997220294706,  # C language 
        "🔵": 800164451017949224,  # Programmer
        "🟡": 891761884494172220,  # Python
    }

    # Create an embed with role options
    embed = discord.Embed(
        title="Choose a Role",
        description="React with the emoji corresponding to the role you want.",
        color=discord.Color.blue()
    )

    for emoji, role_id in roles.items():
        role = ctx.guild.get_role(role_id)
        if role:
            embed.add_field(name=emoji, value=role.mention, inline=True)

    # Send the embed message only if at least one role is found
    if embed.fields:
        message = await ctx.send(embed=embed)
        
        # Add reactions to the message for each role
        for emoji in roles.keys():
            await message.add_reaction(emoji)

        # Define a check function for the wait_for reaction
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in roles

        try:
            # Wait for a reaction from the user
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

            # Get the selected role and add it to the user
            selected_role = roles[str(reaction.emoji)]
            role = ctx.guild.get_role(selected_role)
            
            if role:
                await ctx.author.add_roles(role)
                # Notify the user
                await ctx.send(f"You have been given the role: {role.name}")
            else:
                await ctx.send("Error: Role not found.")

            # Remove reactions from the message
            await message.clear_reactions()

        except asyncio.TimeoutError:
            # Handle timeout if no reaction is received within 60 seconds
            await ctx.send("Role selection timed out. Please try again.")
            await message.clear_reactions()
    else:
        await ctx.send("Error: No roles found.")

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

@bot.event
async def on_reaction_add(reaction, user):
    # Ignore reactions from the bot itself
    if user == bot.user:
        return

    # Check if the reacted message is a poll
    if isinstance(reaction.message.channel, discord.TextChannel):
        # Check if the reaction is an emoji number (1-9)
        if reaction.emoji in [f"{i}\u20e3" for i in range(1, 10)]:
            # Get the corresponding option index
            option_index = int(reaction.emoji[0]) - 1

            # Send a message indicating the user's vote
            await reaction.message.channel.send(f"{user.mention} voted for Option {option_index + 1}!")


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

# Run the bot with your token
def read_token():
    # Read the bot token from the 'token.key' file
    with open('token.key', 'r') as file:
        return file.read().strip()

bot.run(read_token())