import discord
from discord.ext import commands

from Models.Context import Context


class SameTimeAttackStartCog(commands.Cog):
    """
    同時凸開始処理
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dstart")
    async def same_time_attack_start(self, ctx: commands.context.Context, *args):
        remain: int = int(args[0])

        # 同時凸データ追加
        context: Context = await Context.get_instance(self.bot)
        context.same_time_attack.start(remain)
        print(context.same_time_attack.format_status())
        await ctx.message.channel.send(context.same_time_attack.format_status())
