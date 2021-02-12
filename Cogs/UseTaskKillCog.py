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

    @commands.command(name="taskKill", aliases=["タスキル", "taskkill"])
    async def use_task_kill(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(ctx.message.author.id)

        # タスキル処理
        await clan_member.exec_task_kill(ctx.message)
