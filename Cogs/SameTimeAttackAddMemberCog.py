import discord
from discord.ext import commands
from yukarisan.Models.Context import Context


class SameTimeAttackAddMemberCog(commands.Cog):
    """
    同時凸するメンバーの追加
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("dadd")
    async def add_member(self, ctx: commands.context.Context, *args):
        # 予測ダメージ取得
        suspect: int = int(args[0])

        # 同時凸開始
        context: Context = await Context.get_instance(self.bot)
        context.same_time_attack.add_member(ctx.message.author, suspect)
        await ctx.message.channel.send(context.same_time_attack.format_status())
