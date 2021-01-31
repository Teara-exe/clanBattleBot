import discord
from discord.ext import commands

from Lib.Utils import Utils

from Models.ClanMember import ClanMember
from Models.Context import Context


class UseTaskKillCog(commands.Cog):
    """
    タスクキルの使用処理を行う
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="タスキル")
    async def use_task_kill_jp(self, ctx: commands.context.Context):
        await self.use_task_kill(ctx)

    @commands.command(name="taskKill")
    async def use_task_kill(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(ctx.message.author.id)

        clan_member.exec_task_kill()
        # キャンセル処理
        return_message: str = "【タスキル使用】{} さんの{}凸目{}をキャンセルしました".format(
            clan_member.discord_user_data.display_name,
            clan_member.attack_status.attack_count + 1,
            "(持越し)" if clan_member.attack_status.is_carry_over else ""
        )
        await ctx.message.channel.send(return_message)
