from discord.ext import commands

from yukarisan.Lib.Utils import Utils
from yukarisan.Models.Context import Context


class AttackStatusCog(commands.Cog):
    """
    現在凸している人を取得する
    """
    # ---- attributes ----
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("status")
    async def now_status(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # 対象チャンネル以外でスルー
        if not await Utils.check_channel(self.bot, ctx.message):
            return

        context: Context = await Context.get_instance(self.bot)
        return_message: str = context.get_now_attack_member()

        await ctx.message.channel.send("現在のボスに凸しているメンバーの一覧です。\n```\n {} \n```".format(return_message))
