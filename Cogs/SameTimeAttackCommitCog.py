import discord
from discord.ext import commands

from yukarisan.Models.Context import Context


class SameTimeAttackCommitCog(commands.Cog):
    """
    同時凸中の実際のダメージを確定する処理
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dcommit")
    async def commit_damage(self, ctx: commands.context.Context, *args):
        commit_damage: int = int(args[0])

        # 同時凸開始
        context: Context = await Context.get_instance(self.bot)
        context.same_time_attack.commit_damage(ctx.message.author, commit_damage)
        await ctx.message.channel.send(context.same_time_attack.format_status())
