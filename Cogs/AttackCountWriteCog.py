import discord
from discord.ext import commands

from yukarisan.Lib.Utils import Utils
from yukarisan.Models.Context import Context


class AttackCountWriteCog(commands.Cog):
    """
    現在の凸状況を取得する
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dispcount")
    async def write_count(self, ctx: commands.context.Context):
        # 対象チャンネル以外でスルー
        if not await Utils.check_channel(self.bot, ctx.message):
            return

        context: Context = await Context.get_instance(self.bot)
        await ctx.channel.send(context.get_now_attack_count())

    @commands.command("凸数")
    async def write_count_jp(self, ctx: commands.context.Context):
        await self.write_count(ctx)
