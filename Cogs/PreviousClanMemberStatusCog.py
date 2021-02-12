from discord.ext import commands

from Lib.Utils import Utils
from Models.AttackStatus import AttackStatus
from Models.ClanMember import ClanMember
from Models.Context import Context


class PreviousClanMemberStatusCog(commands.Cog):
    """
    クラメンの凸状況をひとつ前の状態に戻す
    """
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("back")
    async def previous_status(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # 対象チャンネル以外でスルー
        if not Utils.check_channel(ctx.message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(ctx.message.author.id)

        # ひとつ前に戻す処理
        await clan_member.previous_status(ctx.message)
