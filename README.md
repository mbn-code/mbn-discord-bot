# Bot Documentation

## Introduction
This document provides documentation for the Discord bot implemented using the Discord.py library. The bot is designed to perform various functions, including logging messages, moderating channels, providing information about programming, and interacting with users.

## Table of Contents
1. [Bot Initialization](#bot-initialization)
2. [Logging](#logging)
3. [Moderation Commands](#moderation-commands)
4. [Role Management](#role-management)
5. [Credits System](#credits-system)
6. [Polls](#polls)
7. [Weather](#weather)
8. [Support Tickets](#support-tickets)
9. [CVE Information](#cve-information)
10. [Stack Overflow Search](#stack-overflow-search)
11. [GitHub Repository Search](#github-repository-search)
12. [Command List](#command-list)

## Bot Initialization
The bot is initialized with the following configurations:
- Command prefix: `!`
- Intents: All Discord intents are enabled.

## Logging
The bot logs various events, including messages, message edits, message deletes, reactions, member joins/leaves/updates, server updates, role updates, bans, unbans, voice state updates, user updates, member presence updates, integrations, raw events, and typing events.

## Moderation Commands
- `!mute`: Mutes a member.
- `!unmute`: Unmutes a member.
- `!ban`: Bans a member.
- `!timeout`: Temporarily mutes a member.
- `!clear`: Clears a specified number of messages.
- `!warn`: Warns a member.
- `!purge`: Purges a specified number of messages.
- `!purgeuser`: Purges all messages from a specific user.
- `!userinfo`: Displays information about a user.
- `!ticket`: Creates a support ticket.

## Role Management
- `!role`: Allows users to choose roles through reactions.
- `!buy_role`: Allows users to buy roles using credits.

## Credits System
- `!post`: Awards credits for valid posts.
- `!credits`: Displays the number of credits a user has.

## Polls
- `!poll`: Creates a poll with a specified question and options.

## Weather
- `!weather`: Displays the current weather for a specified city.

## Support Tickets
- `!ticket`: Creates a support ticket.

## CVE Information
- `!cve`: Fetches information about a specific Common Vulnerabilities and Exposures (CVE) entry.

## Stack Overflow Search
- `!stackoverflow`: Searches Stack Overflow for a programming question.

## GitHub Repository Search
- `!github`: Searches GitHub for a repository and displays the one with the most stars.

## Command List
- `!commands`: Displays a list of available commands and their parameters.

## Conclusion
This documentation provides an overview of the implemented Discord bot, its functionalities, and how to use its various commands. Users can refer to this documentation for guidance on interacting with the bot and understanding its capabilities.
