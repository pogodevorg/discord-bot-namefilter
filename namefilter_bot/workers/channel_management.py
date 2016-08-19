import asyncio
import discord
import logging
import re
import random

from namefilter_bot.workers import BaseWorker
from namefilter_bot import logger
from unidecode import unidecode


class ChannelManagement(BaseWorker):

    def initialize(self):
        pass

    def run(self):

        self.client.loop.create_task(self.filter())

    def IsValid(self, var):
        if var is None:
            return False
        else:
            return True
	
    async def filter(self):

        await self.client.wait_until_ready()

        # get arrays channels id need to post
        discord_channels = []
        for server in self.client.servers:
            for channel in server.channels:
                if channel.name in self.config.get('channels', []):
                    discord_channels.append(
                        discord.Object(channel.id))

        while not self.client.is_closed:
            for channel in discord_channels:
                await self.client.send_message(channel, message)

            await asyncio.sleep(300)

    def need_to_strip(self, message):

        except_roles = self.config.get('except_roles', [])

        # Do nothing if bot cannot find user
        if self.IsValid(message.author) is False:
            return False
        # Do nothing if bot is the sender in the message
        if message.author == self.client.user:
            return False
        # Do nothing if bot cannot find attribute roles
        if self.IsValid(message.author.roles) is False:
            return False
        """
        Ignore if message from except roles
        """
        for role in message.author.roles:
            if role.name in except_roles:
                return False

        """
        Check if message contains unicode name
        """
        # Manage channel nickname filter
        if message.channel.name in self.config.get('channels', []):
            random_nicknames = ['Carla', 'Price', 'Angelo', 'Cook', 'Charlene', 'Schwartz', 'Angel', 'Weber', 'Frederick', 'Daniel', 'Mack', 'Berry', 'Bobby', 'Guerrero', 'Willard', 'Allen', 'Krista', 'Walsh', 'Melanie', 'Perkins', 'Rickey', 'Carlson', 'Francis', 'Norman', 'Wilbert', 'Bowen', 'Gwen', 'Brewer', 'Stanley', 'Conner', 'Judy', 'Miller', 'Eduardo', 'Yates', 'Laverne', 'Morton', 'Julia', 'Foster', 'Leland', 'Steele', 'Dominic', 'Allison', 'Jason', 'Gray', 'Evan', 'Ortiz', 'Sheri', 'Rhodes', 'Kristy', 'Craig', 'Mamie', 'Glover', 'Marcella', 'Chapman', 'Allan', 'Ray', 'Erin', 'Lawrence', 'Robin', 'Reyes', 'Malcolm', 'Thornton', 'Maggie', 'Riley', 'Pat', 'Burns', 'Shelley', 'Soto', 'Lana', 'Harper', 'Leah', 'Harrington', 'Juana', 'Parker', 'Lindsay', 'Robbins', 'Bill', 'Simon', 'Jacquelyn', 'Cole', 'Laurence', 'Rios', 'Ralph', 'Garza', 'Marlon', 'Strickland', 'Minnie', 'Hammond', 'Ramon', 'Massey', 'Scott', 'Reid', 'Ray', 'Wagner', 'Stacy', 'Morales', 'Jan', 'Schultz', 'Spencer', 'Watson', 'WinnyDapooh', 'PigletDaPooh']
            authorname = message.author.name
            encoded_authorname = authorname.encode('unicode_escape')
            stripped_authorname = encoded_authorname.decode('unicode_escape').encode('ascii','ignore').decode("utf-8")
			#If name is fine return false, otherwise return True
            if (message.author.name == stripped_authorname):
                return False
            if ((message.author.name != stripped_authorname) or not (message.author.nick in random_nicknames)) and (message.author.nick is None):
                log_message = 'Unicode Name needs to be stripped for: '+message.author.name
                logger.log(log_message)
                logging.warning(log_message)
                return True
            else:
                return False