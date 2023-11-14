# Discord Bot

This Discord bot is designed to serve as a Logging, Moderating, Admin, and Tech Support bot for Discord servers. It includes features such as automatic logging, moderation commands (kick, ban, clear), mute/unmute functionality, and additional admin commands.

## Setup

1. **Prerequisites:**
   - Python 3.x installed
   - Discord.py library installed (`pip install discord.py`)
   - Create a Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a file named `token.key` and place your bot token inside

2. **Installation:**
   - Clone or download this repository to your local machine.

3. **Configuration:**
   - Open the `token.key` file and paste your Discord bot token.

4. **Running the Bot:**
   - Execute the bot script: `python YourBotScript.py`

## Commands

- `!kick @user [reason]`: Kick a member from the server.
- `!ban @user [reason]`: Ban a member from the server.
- `!clear [amount]`: Clear a specified number of messages in a channel.
- `!mute @user`: Mute a member.
- `!unmute @user`: Unmute a member.
- `!serverid`: Display the ID of the current server.

## Logging

The bot automatically logs messages and commands in a designated logging channel. If the bot cannot find a channel with "logging" in its name, it will prompt the server owner to specify a logging channel.

## Contributing

Feel free to contribute to the development of this bot by submitting pull requests or reporting issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
