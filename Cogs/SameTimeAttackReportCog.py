import discord
from discord.ext import commands

from yukarisan.Models.Context import Context


class SameTimeAttackReportCog(commands.Cog):
    """
    同時凸の着地予定スコアを登録する
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dreport")
    async def attack_report(self, ctx: commands.context.Context, *args):
        real_damage: int = int(args[0])

        context: Context = await Context.get_instance(self.bot)
        context.same_time_attack.real_damage_add(ctx.message.author, real_damage)
        print(context.same_time_attack.format_status())
        await ctx.message.channel.send(context.same_time_attack.format_status())
