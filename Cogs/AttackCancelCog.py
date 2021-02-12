import discord
from discord.ext import commands

from Lib.Utils import Utils
from Models.ClanMember import ClanMember
from Models.Context import Context
from Models.ClanBattleEmoji import ClanBattleEmoji


class AttackCancelCog(commands.Cog):
    """
    ボス凸のキャンセル処理
    """

    # ---- attributes ----
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='c', aliases=["キャンセル", "cancel"])
    async def on_cancel(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # キャンセル処理
        await self._cancel(ctx.message)

    @commands.Cog.listener(name='on_reaction_add')
    async def on_cancel_reaction(self, reaction: discord.Reaction, member: discord.Member):
        # 反応した絵文字がキャンセル絵文字でなければスルー
        if not Utils.check_emoji(reaction, ClanBattleEmoji.CANCEL):
            return
        # 反応がbotだったらスルー
        if member.bot:
            return

        # 管理メッセージ以外の場合はスルー
        context: Context = await Context.get_instance(self.bot)
        if not context.check_managed_message(reaction.message, member):
            return

        # キャンセル処理
        await self._cancel(reaction.message)

    async def _cancel(self, message: discord.Message):
        # 対象チャンネル以外でスルー
        if not Utils.check_channel(message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(message.author.id)

        # キャンセル処理
        await clan_member.cancel()
