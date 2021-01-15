from discord.ext import commands

from yukarisan.Lib.Utils import Utils
from yukarisan.Models.AttackStatus import AttackStatus
from yukarisan.Models.ClanMember import ClanMember
from yukarisan.Models.Context import Context


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

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(ctx.message.author.id)

        # 1個前のステータスを出力する
        previous_attack_status: AttackStatus = clan_member.attack_status
        clan_member.previous_status()
        now_attack_status: AttackStatus = clan_member.attack_status

        # メッセージ生成
        previous_status_message: str = "【前回】{}凸 {} {}".format(
            previous_attack_status.attack_count,
            "【持越し】" if previous_attack_status.is_carry_over else "",
            "【タスキル済み】" if previous_attack_status.use_task_kill else "")
        now_status_message: str = "【今回】{}凸 {} {} ".format(
            now_attack_status.attack_count,
            "【持越し】" if now_attack_status.is_carry_over else "",
            "【タスキル済み】" if now_attack_status.use_task_kill else "")

        return_message: str = "{}さんの状態を変更しました。\n{}\n{}".format(clan_member.discord_user_data.display_name,
                                                               previous_status_message, now_status_message)
        await ctx.message.channel.send(return_message)
