import discord
from discord.ext import commands

from Models.Context import Context
from Models.LoadConfig import LoadConfig


class Utils:
    @staticmethod
    def has_to_bot_reaction(message: discord.Message, bot: commands.Bot):
        return Utils.is_message_author_bot(message) and Utils.is_message_mention_to_bot(message, bot)

    @staticmethod
    def is_message_author_bot(message: discord.Message) -> bool:
        return message.author.bot

    @staticmethod
    def is_message_mention_to_bot(message: discord.Message, bot: commands.Bot):
        return bot.user not in message.mentions

    @staticmethod
    def check_emoji(reaction: discord.Reaction, emoji: str) -> bool:
        return reaction.emoji == emoji

    @staticmethod
    def check_channel(message: discord.Message) -> bool:
        config: LoadConfig = LoadConfig.get_instance()
        return config.attack_management_channel_id == message.channel.id


