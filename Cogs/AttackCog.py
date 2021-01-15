import discord
from discord.ext import commands

from yukarisan.Lib.Utils import Utils
from yukarisan.Models.ClanMember import ClanMember
from yukarisan.Models.Context import Context
from yukarisan.Models.ClanBattleEmoji import ClanBattleEmoji


class AttackCog(commands.Cog):
    """
    ボスへの凸処理
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="a")
    async def on_attack(self, ctx: commands.context.Context):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(ctx.message):
            return

        # 対象チャンネル以外でスルー
        if not await Utils.check_channel(self.bot, ctx.message):
            return

        # クラメンデータ検索
        context: Context = await Context.get_instance(self.bot)
        clan_member: ClanMember = context.get_clan_member(ctx.author.id)

        # 凸のデータ保存
        clan_member.attack(ctx.message)

        # メッセージに対してリアクションを送出する
        await ctx.message.add_reaction(ClanBattleEmoji.END)
        await ctx.message.add_reaction(ClanBattleEmoji.KILL)
        await ctx.message.add_reaction(ClanBattleEmoji.CANCEL)

    @commands.command(name="凸")
    async def on_attack_jp(self, ctx: commands.context.Context):
        await self.on_attack(ctx)
