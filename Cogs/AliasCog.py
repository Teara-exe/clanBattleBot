import re

import discord
from discord.ext import commands

from Cogs.AttackCog import AttackCog
from Models.ClanBattleEmoji import ClanBattleEmoji


class AliasCog(commands.Cog):
    """
    コマンドの仕様をよくわかってない人を救済する処理。
    なんかバグの温床になる気はしてるので、使わない方が良いと思う
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def command_alias(self, message: discord.Message):
        command_msg: str = message.content

        # 「a(スペース無し)数値」→「a」に変換 「凸(スペース無し)数値」→「凸」に変換 ※数値は半角or全角
        if re.match(r"^a[0-9０１２３４５６７８９]+$", command_msg) or re.match(r"^凸[0-9０１２３４５６７８９]+$", command_msg):
            ctx: commands.Context = await self.bot.get_context(message)
            cog: AttackCog = self.bot.get_cog("AttackCog")
            await cog.on_attack(ctx)
            # 変な文字列を送ってきたので燃やします
            await message.add_reaction(ClanBattleEmoji.FIRE)








