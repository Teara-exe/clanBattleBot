import discord
from discord.ext import commands

from Lib.Utils import Utils
from Models.ClanMember import ClanMember
from Models.Context import Context
from Models.ClanBattleEmoji import ClanBattleEmoji


class AttackFinishCog(commands.Cog):
    """
    攻撃終了処理(持越しなし)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="f", aliases=["終了", "finish"])
    async def on_finish(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # 終了処理
        await self._finish(ctx.message)

    @commands.Cog.listener(name='on_reaction_add')
    async def on_cancel_reaction(self, reaction: discord.Reaction, member: discord.Member):
        # 反応した絵文字が終了絵文字でなければスルー
        if not Utils.check_emoji(reaction, ClanBattleEmoji.END):
            return
        # 反応がbotだったらスルー
        if member.bot:
            return
        # 管理メッセージ以外の場合はスルー
        context: Context = await Context.get_instance(self.bot)
        if not context.check_managed_message(reaction.message, member):
            return

        # 終了処理
        await self._finish(reaction.message)

    async def _finish(self, message: discord.Message):
        # 対象チャンネル以外でスルー
        if not Utils.check_channel(message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(message.author.id)

        # hack: 更新前に今の状態をもとに返すメッセージを作成する
        return_message: str = "{} さんの{}凸目{}を終了しました".format(
            clan_member.get_member_nickname(),
            clan_member.attack_status.attack_count + 1,
            "(持越し)" if clan_member.attack_status.is_carry_over else ""
        )

        # 終了処理
        clan_member.finish(is_kill=False)
        await message.channel.send(return_message)

        # 凸状態が変わるのでニックネーム修正
        await clan_member.update_member_name()
