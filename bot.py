#
# Python name filter bot for discord
# Author: enjoy2000 | enjoy3013@gmail.com
# Modified By: fkndean | NameFilterBot
#
import discord
import json
import sys
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

    bot = FilterBot(client, config)
    api_key = config.get('api_key', 'NA')

    if api_key == 'NA':
        raise Exception('Please specify your api key!')

    @client.event
    async def on_message(message):
        if message.content.startswith('!resetnick'):
            try:
                await client.change_nickname(message.author, "")
                await client.send_message(message.author, "You have successfully reset your nickname to `%s`!\n```Please consider changing your username to an appropriate name that does not include unicode special characters.```" % message.author.name)
                await client.delete_message(message)
                return
            except discord.Forbidden:
                return
        if bot.on_message(message):
            nickname = message.author.name
            encoded_nickname = nickname.encode('unicode_escape')
            stripped_nickname = encoded_nickname.decode('unicode_escape').encode('ascii','ignore').decode("utf-8")
            if (len(str(stripped_nickname)) <= 3):
                stripped_nickname = random.choice(['Carla', 'Price', 'Angelo', 'Cook', 'Charlene', 'Schwartz', 'Angel', 'Weber', 'Frederick', 'Daniel', 'Mack', 'Berry', 'Bobby', 'Guerrero', 'Willard', 'Allen', 'Krista', 'Walsh', 'Melanie', 'Perkins', 'Rickey', 'Carlson', 'Francis', 'Norman', 'Wilbert', 'Bowen', 'Gwen', 'Brewer', 'Stanley', 'Conner', 'Judy', 'Miller', 'Eduardo', 'Yates', 'Laverne', 'Morton', 'Julia', 'Foster', 'Leland', 'Steele', 'Dominic', 'Allison', 'Jason', 'Gray', 'Evan', 'Ortiz', 'Sheri', 'Rhodes', 'Kristy', 'Craig', 'Mamie', 'Glover', 'Marcella', 'Chapman', 'Allan', 'Ray', 'Erin', 'Lawrence', 'Robin', 'Reyes', 'Malcolm', 'Thornton', 'Maggie', 'Riley', 'Pat', 'Burns', 'Shelley', 'Soto', 'Lana', 'Harper', 'Leah', 'Harrington', 'Juana', 'Parker', 'Lindsay', 'Robbins', 'Bill', 'Simon', 'Jacquelyn', 'Cole', 'Laurence', 'Rios', 'Ralph', 'Garza', 'Marlon', 'Strickland', 'Minnie', 'Hammond', 'Ramon', 'Massey', 'Scott', 'Reid', 'Ray', 'Wagner', 'Stacy', 'Morales', 'Jan', 'Schultz', 'Spencer', 'Watson', 'WinnyDapooh', 'PigletDaPooh'])
            try:
                await client.change_nickname(message.author, stripped_nickname)
                await client.send_message(message.author, "```"+"Your nickname was changed to "+stripped_nickname+"\nThis could've happened for a couple reasons:\n1.) Your name is 3 characters or less\n2.) Your name contained Unicode\nIf you wish to have a different name on our Discord, please change your username and use the !resetnick command in #lounge```")
            except discord.Forbidden:
                return
    bot.run_worker('ChannelManagement')


    client.run(api_key)
