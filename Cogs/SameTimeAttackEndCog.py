import discord
from discord.ext import commands

from yukarisan.Models.Context import Context


class SameTimeAttackEndCog(commands.Cog):
    """
    同時凸を終了する時の処理
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dend")
    async def end(self, ctx: commands.context.Context):

        # 同時凸開始
        context: Context = await Context.get_instance(self.bot)
        context.same_time_attack.end()
        await ctx.message.channel.send("------ 同時凸終了 ------")

