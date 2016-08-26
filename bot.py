#
# Python name filter bot for discord
# Author: enjoy2000 | enjoy3013@gmail.com
# Modified By: fkndean | NameFilterBot
#
import discord
import json
import sys
import logging
import random

from namefilter_bot import NameFilterBot, logger

client = discord.Client()

if __name__ == '__main__':

    @client.event
    async def on_ready():
        """ Connected to bot """
        logger.log('Logged in as')
        logger.log(client.user.name)
        logger.log(client.user.id)
        logger.log('------')

    config = {}
    with open('config.json') as output:
        config = json.load(output)

    bot = NameFilterBot(client, config)
    api_key = config.get('api_key', 'NA')

    if api_key == 'NA':
        raise Exception('Please specify your api key!')

    @client.event
    async def on_message(message):
        if message.content.startswith('!resetnick'):
            try:
                except_roles = bot.config.get('except_roles', [])
                for role in message.author.roles:
                    if role.name in except_roles:
                        await client.send_message(message.author, "[EXCEPTION ROLES] You may not reset your nickname!")
                        await client.delete_message(message)
                        return
                if message.author.nick is None:
                    await client.send_message(message.author, "`You have already reset your nickname!`")
                    await client.delete_message(message)
                    return
                await client.change_nickname(message.author, "")
                await client.send_message(message.author, "You have successfully reset your name back to `%s`!\n```Please consider changing your username to an appropriate name that does not include unicode special characters.```" % message.author.name)
                await client.delete_message(message)
                log_message = 'Executed Reset Name for User: ' + message.author.name
                logger.log(log_message)
                logging.warning(log_message)
                return
            except discord.Forbidden:
                log_message = 'I do not have required permissions to do this on ' + message.author.name
                logger.log(log_message)
                logging.warning(log_message)
                return
            except AttributeError:
                log_message = 'I cannot grab roles for ' + message.author.name
                logger.log(log_message)
                logging.warning(log_message)
                return
        if bot.on_message(message):
            authorname = message.author.name
            encoded_authorname = authorname.encode('unicode_escape')
            stripped_authorname = encoded_authorname.decode('unicode_escape').encode('ascii','ignore').decode("utf-8")
            if (len(str(stripped_authorname)) <= 3):
                stripped_authorname = random.choice(['Carla', 'Price', 'Angelo', 'Cook', 'Charlene', 'Schwartz', 'Angel', 'Weber', 'Frederick', 'Daniel', 'Mack', 'Berry', 'Bobby', 'Guerrero', 'Willard', 'Allen', 'Krista', 'Walsh', 'Melanie', 'Perkins', 'Rickey', 'Carlson', 'Francis', 'Norman', 'Wilbert', 'Bowen', 'Gwen', 'Brewer', 'Stanley', 'Conner', 'Judy', 'Miller', 'Eduardo', 'Yates', 'Laverne', 'Morton', 'Julia', 'Foster', 'Leland', 'Steele', 'Dominic', 'Allison', 'Jason', 'Gray', 'Evan', 'Ortiz', 'Sheri', 'Rhodes', 'Kristy', 'Craig', 'Mamie', 'Glover', 'Marcella', 'Chapman', 'Allan', 'Ray', 'Erin', 'Lawrence', 'Robin', 'Reyes', 'Malcolm', 'Thornton', 'Maggie', 'Riley', 'Pat', 'Burns', 'Shelley', 'Soto', 'Lana', 'Harper', 'Leah', 'Harrington', 'Juana', 'Parker', 'Lindsay', 'Robbins', 'Bill', 'Simon', 'Jacquelyn', 'Cole', 'Laurence', 'Rios', 'Ralph', 'Garza', 'Marlon', 'Strickland', 'Minnie', 'Hammond', 'Ramon', 'Massey', 'Scott', 'Reid', 'Ray', 'Wagner', 'Stacy', 'Morales', 'Jan', 'Schultz', 'Spencer', 'Watson', 'WinnyDapooh', 'PigletDaPooh'])
            try:
                await client.change_nickname(message.author, stripped_authorname)
                await client.send_message(message.author, "```"+"Your nickname was changed to "+stripped_authorname+"\nThis could've happened for a couple reasons:\n1.) Your name is 3 characters or less\n2.) Your name contained Unicode\nIf you wish to have a different name on our Discord, please change your username and use the !resetnick command in #lounge```")
                await client.delete_message(message)
            except discord.Forbidden:
                return
    bot.run_worker('ChannelManagement')


    client.run(api_key)
