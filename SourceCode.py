from discord.ext.commands import bot
from discord.ext.commands.core import after_invoke
from discord.utils import get
from difflib import get_close_matches as gcm
from requests.api import request
from discord.ext import commands
import discord
import requests
import random
import time



roast_list = ("Mirrors can't talk. Lucky for you, they can't laugh eather","Hey, you have something on your chin...No, the 3rd one down","You're the reason the gene pool needs a lifegard","If i had a face like yours, i'd sue my parents","Your only chance of getting laid is to crawl up a chicken's butt and wait","Some day you'll go far.. and i hope you stay there","You must have been boren on a highway, becasue that's where most accidents happen","If laughter is the best medicaine, your face must be curing the world","I'm glad to see you're not letting your education get in the way og your ignorance","Is your ass jealous of the amount of shit that just came out of your mouth?","I'd agree with you but then we'd both be wrong","When i see your face there's not a thing I would change.. Other then the direction i walked in","If i had a dollar for every time you said something smart, i'd be broke","When you were born the doctor threw you out the window, and the window threw ou back","I love what you've done with your hair. How do you get it to come out of the nostrils like that?")
new = datetime.datetime.now()
intents = discord.Intents.default()
intents.members = intents.emojis = intents.messages = intents.messages = intents.guild_reactions = intents.voice_states = intents.presences = True
client = commands.Bot(command_prefix=';', intents = intents)
list_1 = ["yes","no", "maybe", "ask yourself","why do i have to anwser everything","mby, i don't know", "ask your mom","so you don't know youself?","stop asking all these questions","Ofcurse","what do you mean, NOO","yeah because... i don't know","Uhhhh Yeah!!","What did he sayyyyy","","","","","","yes 10000%"]
list_good = ["no that's awfullll!!", "Yeah, That's pretty good","that is extramly good"]

def checkInt(number):
    try: return int(number)
    except: return False


@client.event
async def on_message(msg):    
    if msg.author != client.user:
        for word in ['fuck', "nigga","nigger","cum","shit","hussy","whore ","ugly","cunt","arsehole ","nig*er","nigge","fag","fucking","gay","retard","idiot","faggot","fag","bitch","Beeatch","stupid"]:
            if word in msg.content.lower():
                channel_log = get(msg.guild.text_channels, id=825087817054421002)
                await msg.channel.send(f"{msg.author} Please don't say another bad word")
                time.sleep(0.5)
                await msg.delete()
                return await channel_log.send(f"{msg.author} Said \"{msg.content}\" which includes the word '{word}'")
        for word in ['/do', '/are', "/is"]:
            if msg.content.lower().startswith(word):
                return await msg.channel.send(random.choice(list_1))
        if msg.content.lower() in ['hi', 'hello', 'hey', 'sup', 'wassup', 'ay up', 'hallo']:
            return await msg.channel.send(f"{random.choice(['hi', 'hello', 'hey', 'sup', 'wassup', 'ay up'])} {msg.author.mention}. Now have a good day")
            
        elif msg.content == '/rules':
            return await msg.channel.send(
"""```css
1 You can pretty much say anythign, just don't be dumb or ask for dumb shit Google is your best friend

2 And if you upload any files PLEASE leave a  https://www.hybrid-analysis.com/ scan

3 Always look on peoples roles in the Discord server.

4 Don't scam people

5 NO Sellling of anything in the server, everything should be free.

6 No talking shit in voice channels(because i don't wan't toxic vc) :HARD #MUTE.

7 No hacking your own community or anyone that are in this server(link, files, doxxing, ip, anything)

8 :DON*T CLICK LINKS FROM ANYONE

9 When joining a vc(voice call) you have to speak within 45 seconds or you get kicked to concentration camp role
If you come in ANY vc in the discord you have to eather stay active in the #voice-channel-chat or have to speak, its kinda sus just coming in and listening
```""")
        elif msg.content.lower() == "/help":
            return await msg.channel.send(
"""```tex
$ Indian Tech Support $
``````asciidoc
Welcome to /help for Indian  Tech Support
=============================================
- /help  : See the bot's help menu

- /how : If you write somethign and have "how" in it, it will ping me

- /do : do i....

- /whois : you can do a whois scan on a ip (not domains)

- /hey : Say hello to the bot and it will reply back

- hello   : You can also say 'hey' incase you hate 'hello' for some reason

- /rules : See the server's rules

- /gay : i am gay

- fbi: uhmm try it

- /roles : See the server's roles that is available 

- lucid : Is lucid crying

- /Ready : looks if the bot is ready/online

- /quack : This does whatever it does, just try it

- /idk : Will display a shrug

- /smile : Give you a smile :)

- /ddos : Says what a ddos attack is

- /syn

- /math (A,S,M,D) : you can only add with this command at the moment 

- /who made you? to check who the owner of the bot is

- /roast - this is kinda explanetory

- /ls - This give you brain dmg

- /joke - makes a joke

- /roast - roasts you

- /gender


            ADMIN/OWNER COMMANDS
=============================================

/mute @ reason

/kick @ reason

/ban @ reason

/unmute @ reason

/acm - Make an announcment

```""") 
        elif msg.content.lower() == "/roles":
            await msg.channel.send(
"""```css
The roles are level highest to lowest

BlackHat hacker

RedHat Hacker (1,2,3)

GreyHat Hacker

WhiteHat Hacker (1,2,3)

Suicide hacker (Not avalable)

GreenHat Hacker     

ScriptKiddie/New
```""")
        elif msg.content.lower() == "/who made you":
            id = (await client.application_info()).owner
            await msg.channel.send(id)
        elif msg.content.lower() == "/ooga":
            await msg.channel.send("booga")
        elif msg.content in ["greenhat", "green hat"]:
            member = msg.author
            role = get(msg.guild.roles, name="greenhat")
            await member.add_roles(role)
        elif msg.content in ["script kiddie", "scriptkiddie"]:
            member = msg.author
            role = get(msg.guild.roles, name="scriptkiddie/greenhat")
            await member.add_roles(role)
        elif msg.content.lower() == "gay":
            member = msg.author
            role = get(msg.guild.roles, name="gay")
            await member.add_roles(role)
        elif msg.content in ["/hey","/hello"]:
            await msg.channel.send(f"hello, {msg.author.mention}")
        elif msg.content.lower() == "/quack":
            return await msg.channel.send(f"quack u, {msg.author.mention}")
        elif msg.content.lower() == "cool":
            await msg.channel.send(f"no that's not cool, that's sick, {msg.author.mention}")
        elif msg.content.lower() in ["idk", "i don't know", "i dont know"]:
            await msg.channel.send("¯\_(ツ)_/¯")
        elif msg.content.lower() == "/smile":
            await msg.channel.send(":)")
        if msg.content.lower().startswith('/how'):
            await msg.channel.send(f'{msg.author.mention} asked "{msg.content}" <@632944826266025996> ' "," ' <@756004815569551372>' "," '<@779443011271917569>' "," '<@709590082192932875>')
        elif msg.content.lower() == "good":
            await msg.channel.send(random.choice(list_good))
        elif msg.content.lower()=="/die":
            await msg.channel.send("__**DEAD**__")
        elif msg.content.lower()=="/stop":
            await msg.channel.send("ok i will stop....")
        elif msg.content =="/redhat":
            await msg.channel.send("```css\nA red hat hacker could refer to someone who targets Linux systems. However, red hats have been characterized as vigilantes. ... Rather than hand a black hat over to the authorities, red hats will launch aggressive attacks against them to bring them down, often destroying the black hat's computer and resources.```")
        elif msg.content =="/Ready":
            await msg.channel.send("I Think i am fixed/ready to go? am i")
        elif msg.content.lower() == "/i am gay" or msg.content.lower() == "banned":
            await msg.channel.send("__**BANNED**__ '-' ")
        elif msg.content.lower() == "/lucid":
            await msg.channel.send("Is lucid crying?")
        elif msg.content.lower() == "/fbi":
            await msg.channel.send("https://www.youtube.com/watch?v=4wX2xBOuzRg")
        elif msg.content.lower() == "/ddos":
            await msg.channel.send(f"{msg.author.mention}\n```In computing, a denial-of-service attack is a cyber-attack in which the perpetrator seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to the Internet. Denial of service is typically accomplished by flooding the targeted machine or resource with superfluous requests in an attempt to overload systems and prevent some or all legitimate requests from being fulfilled```")
        elif msg.content.lower() == "/dns":
            await msg.channel.send(f"{msg.author.mention}```The Domain Name System is a hierarchical and decentralized naming system for computers, services, or other resources connected to the Internet or a private network. It associates various information with domain names assigned to each of the participating entities```")
        elif msg.content.lower() == "/tcp":
            await msg.channel.send(f"{msg.author.mention}```The Transmission Control Protocol is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol. Therefore, the entire suite is commonly referred to as TCP/IP.```")
        elif msg.content.lower() == "/udp":
            await msg.channel.send(f"{msg.author.mention}```In computer networking, the User Datagram Protocol is one of the core members of the Internet protocol suite. The protocol was designed by David P. Reed in 1980 and formally defined in RFC 768. With UDP, computer applications can send messages, in this case referred to as datagrams, to other hosts on an Internet Protocol network.```")
        elif msg.content.lower() == "/elf":
            await msg.channel.send(f"{msg.author.mention}```Elf is binary for Linux```")
        elif msg.content.lower() == "/ddos":
            await msg.channel.send(f"{msg.author.mention}\n```In computing, a distributed-denial-of-service attack is a cyber-attack in which the perpetrator seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to the Internet. Denial of service is typically accomplished by flooding the targeted machine or resource with superfluous requests in an attempt to overload systems and prevent some or all legitimate requests from being fulfilled```")
        elif gcm(msg.content.lower(), ["tech support", "help"]):
            await msg.channel.send("Did someone say my name?")
            msg1 = await client.wait_for('message', check=lambda m: m.author == msg.author)
            if msg1.content.lower() in ["yes"]:
                await msg.channel.send("ok, do you have a question? (Y/N)")
                msg2 = await client.wait_for('message', check=lambda m: m.author == msg.author)
                if msg2.content.lower() in ["y"]:
                    await msg.channel.send('<@632944826266025996>')
                else: await msg.channel.send("Ok! have a good day")

        elif msg.content.lower() == "/syn":
            await msg.channel.send("```css\nA SYN flood is a form of denial-of-service attack in which an attacker rapidly initiates a connection to a server without finalizing the connection. The server has to spend resources waiting for half-opened connections, which can consume enough resources to make the system unresponsive to legitimate traffic.```")

        elif msg.content.lower() == "/botnet":
            await msg.channel.send("```css \nA botnet is a number of Internet-connected devices, each of which is running one or more bots. Botnets can be used to perform Distributed Denial-of-Service (DDoS) attacks, steal data, send spam, and allow the attacker to access the device and its connection. The owner can control the botnet using command and control (C&C) software. The word 'botnet' is a portmanteau of the words 'robot' and 'network'. The term is usually used with a negative or malicious connotation.```")

        elif msg.content.lower() == "/time":
            await msg.channel.send(f"{msg.author} The time is : " + str(new) + "CET")
            
        await client.process_commands(msg)

    @client.command()
    async def whois(ctx, ip):
        if ip == None: return await ctx.send("Bruh, you didn't give an IP")
        req = requests.get(f'https://api.ipgeolocationapi.com/geolocate/{ip}').json()
        await ctx.send(
    f"""```autohotkey\n
    Details on IP
    =========================
    IP: {ip}
    Continent: {req['continent']}
    Country: {req['name']} ({req['gec']})
    Region: {req['region']}
    Sub-region: {req['subregion']}
    Offical language: {", ".join(req['languages_official'])}
    Languages spoken: {", ".join(req['languages_spoken'])}
    Currency: {req['currency_code']}
    Country Code: {req["country_code"]}
    national_destination_code_lengths: {req["national_destination_code_lengths"]}
    GeoLocation {req['geo']}
    Postal Code {req["postal_code"]}
    ```""")

@client.command()
async def roast(ctx): await ctx.send(requests.get(f"https://insult.mattbas.org/api/insult").text)

@client.command()
async def kick(ctx, member: discord.Member, *, reason):
    if ctx.author.id != 632944826266025996: return await ctx.send(f"{ctx.author}. You are not the owner :)")  
    await ctx.message.delete()
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked. ' + reason)
            
    # if ctx.author.id == 632944826266025996:
    #     await member.kick(reason=reason)
    #     await ctx.send(f'User {member} has been kicked. ' + reason)
    # else:
    #     await ctx.send(f"{ctx.author}. You are not the owner :)")        

@client.command()
async def ban(ctx, member: discord.Member, *, reason):
    if ctx.author.id != 632944826266025996:
        await ctx.message.add_reaction("🤔")
        return await ctx.send(f"{ctx.author}.\nYou are not the....\t owner :)") 
    await ctx.message.delete()
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned. ' + reason)

@client.command()
async def joke(ctx):
    req = requests.get(f"https://v2.jokeapi.dev/joke/Any").json()

    await ctx.send(f"{req['setup']}\n\n{req['delivery']}")

@client.command()
async def meme(ctx):
    req = requests.get(f"https://meme-api.herokuapp.com/gimme/1").json()

    await ctx.send(f"{req['postLink']}")

@client.command()
async def mute_help(ctx):
    await ctx.send("/mute, @person, reason, time")

@client.command()
async def mute(ctx, member: discord.Member, reason):
    if ctx.author.id != 632944826266025996: return await ctx.send(f"{ctx.author} You are not the owner :)")
    await ctx.message.add_reaction("🤔")
    role = get(ctx.guild.roles, id=812666054320586752) 
    await ctx.message.delete()
    await ctx.send("Muted beucase.. " + reason )
    await member.add_roles(role)

@client.command()
async def unmute(ctx, member: discord.Member, reason):
    if ctx.author.id != 632944826266025996:
        await ctx.message.add_reaction("🤔")
        return await ctx.send(f"{ctx.author} You are not the owner :)")
    role = get(ctx.guild.roles, id=806637490714312754)
    await ctx.message.delete()
    await ctx.send("Un-Muted beucase.. " + reason)
    await member.remove_roles(role)

@client.command()
async def math_A(ctx):
    await ctx.send('Enter first number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num1 = checkInt(answer.content)
    if not num1: return await ctx.send("You can't use string in math")
    await ctx.send('Enter second number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num2 = checkInt(answer.content)
    if not num2: return await ctx.send("You can't use string in math")
    await ctx.send(num1 + num2)
    #(A,S,M,D)

@client.command(case_insensitive=True)
async def math_S(ctx):
    await ctx.send('Enter first number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num1 = checkInt(answer.content)
    if not num1: return await ctx.send("You can't use string in math")
    await ctx.send('Enter second number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num2 = checkInt(answer.content)
    if not num2: return await ctx.send("You can't use string in math")
    await ctx.send(num1 - num2)

    @client.command(case_insensitive=True)
    async def math_M(ctx):
        await ctx.send('Enter first number: ')
        answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
        num1 = checkInt(answer.content)
        if not num1: return await ctx.send("You can't use string in math")
        await ctx.send('Enter second number: ')
        answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
        num2 = checkInt(answer.content)
        if not num2: return await ctx.send("You can't use string in math")
        await ctx.send(num1 * num2)

@client.command()
async def math_D(ctx):
    await ctx.send('Enter first number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num1 = checkInt(answer.content)
    if not num1: return await ctx.send("You can't use string in math")
    await ctx.send('Enter second number: ')
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    num2 = checkInt(answer.content)
    if not num2: return await ctx.send("You can't use string in math")
    await ctx.send(num1 / num2)
    
list_questions = { 1: "What does TCP stand for",2: "What does UDP stand for",3: "What does OTP stand for",4:"What does DNS stand for",5:"What is binary code called for linux?",6:"What does RAT stand for",7:"What does DDOS stand for",8:"What does DDNS stand for"}

list_questions_1 = random.choice(list_questions)

a_1 = "Transmission Control Protocol"
a_2 = "User Datagram Protocol" 
a_3 = "One Time Password" 
a_4 = "Domain Name System" 
a_5 = "ELF" 
a_6 = "Remote Access tool" 
a_7 = "Distributed Denial of service"
a_8 = "Dynamic Domain Name System"

@client.command()
async def quiz(ctx):
    anwser = a_1

    await ctx.send(f"Welcome {ctx.author} to the Indian Tech support quiz. This is randomized questions, so sometimes in it might pick twice\n good luck, have fun")
    await ctx.send("Are you ready (Y/N)")
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    await ctx.send(random.choice(list_questions))
    answer = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    if anwser == a_1.lower:
        await ctx.send ("That's right")
    else:
        await ctx.send ("Nope")

@client.command()
async def ls(ctx):
    await ctx.send("Desktop  Documents   Music   Public   Videos")

@client.command()
async def information(ctx):
    await ctx.send("```css\nHello welcome to information, please fill out the below\n```")
    await ctx.send("```fix\nWhat is your name; ```")
    anwser1 = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)    
    with open("logs.txt", "a"):
        print(anwser1)
    await ctx.send("```fix\nWhat is your age; ```")
    anwser2 = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)  
    with open("logs.txt", "a"):
        print(anwser2)

@client.command()
async def clear(ctx, amount=10):
    role = get(ctx.guild.roles, id=806637490714312754) 
    if ctx.author.id != 632944826266025996:
        return await ctx.send(f"{ctx.author} You are not the owner :)")
    role = get(ctx.guild.roles, id=806637490714312754)
    await ctx.channel.purge(limit=amount + 1)
    time.sleep(0.5)
    await ctx.send("```css\nI am done deleting " + str(amount) + " messeges```", delete_after = 3.5)

@client.command()
async def poop(ctx):
    await ctx.channel.send("""\n__**poop**__""")

@client.command()
async def acm(ctx, *, sentence):
    await ctx.message.delete()
    if ctx.author.id != 632944826266025996:
        return await ctx.send(f"{ctx.author} You are not the owner :)")
    role = get(ctx.guild.roles, id=806637490714312754)
    await ctx.send(sentence)

#in_a_loop = True
#@client.command()
#async def spam(ctx):
#   while in_a_loop:
#      await ctx.send("```css\n.```\n")

#@client.command()
#async def stopspam(ctx):
#   global in_a_loop
#  in_a_loop = False
# await ctx.message.delete()
    #await ctx.send("Spam stopped")
@client.command()
async def gender(ctx):
    await ctx.send("I am a robot, what do you expect")

#@client.command()
#async def dad(ctx, random):
# await ctx.send(random.choice(dad))
from textwrap import indent
from contextlib import redirect_stdout
from io import StringIO
from traceback import format_exc
@client.command(name='eval')
async def _eval(ctx, *, body = None):
    if ctx.author.id in (642791754160013312, 632944826266025996):
        env, error, stdout = { 'ctx': ctx, 'client': client, 'send': ctx.send }, None, StringIO()
        env.update(globals())
        body = '\n'.join(body.split('\n')[1:-1]) if body.startswith('```') and body.endswith('```') else body
        try: exec(f'async def func():\n{indent(body, "  ")}', env)
        except Exception as e: error = f'```autohotkey\n{e.__class__.__name__}: ' + str(e).replace("`", "\\`") + '\n```'
        else:
            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except: error = f'```autohotkey\n{stdout.getvalue()}{format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if ret is None and value: await ctx.send(value)
        if error:
            await ctx.send(error)
            return await ctx.message.add_reaction('❎')
        await ctx.message.add_reaction('✅')

@client.command()
async def info(ctx, member: discord.Member):
    member = ctx.author
    await ctx.send(
    f'''
    ID: {member.id}
    Activity: {member.activity}
    Joined on: {member.joined_at}
    Status: {member.status}
    Roles: {', '.join([role.name for role in member.roles[1:]]) if member.roles[1:] else None}
    In voice channel: {'Yes. ' + 'Voice Channel: ' + member.voice.channel.name if member.voice else 'Not in voice channel'}
    Top role: {member.top_role}
    Acquired roles: {', '.join([role.name for role in member.roles])}
    ''')

@client.command(name='members')
async def members(ctx):
    await ctx.send(ctx.guild.member_count)

@client.command()
async def roles(ctx):

    await ctx.send(", ".join([str(r.id) for r in ctx.guild.roles]))


client.run("")
