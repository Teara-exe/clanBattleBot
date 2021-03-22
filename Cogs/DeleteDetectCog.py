import discord
from discord.ext import commands

from Lib.Utils import Utils


class DeleteDetectCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message_delete")
    async def check_delete(self, message: discord.Message):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(message):
            return

        # 対象チャンネル以外でスルー
        if not Utils.check_channel(message):
            return

        await message.channel.send("{} \nこのチャンネルでメッセージを削除・変更はしないでください。\n".format(message.author.mention)
                                   + "もし間違って凸宣言をした場合は、リアクションかコマンドで取り消してください。")

    @commands.Cog.listener(name="on_message_edit")
    async def check_edit(self, before_message: discord.Message, after_message: discord.Message):
        # botの発言 / 自分へのメンション以外は無視
        if Utils.is_message_author_bot(after_message):
            return

        # 対象チャンネル以外でスルー
        if not Utils.check_channel(after_message):
            return

        await after_message.reply("このチャンネルでメッセージを削除・変更はしないでください。\n"
                                  + "もし間違って凸宣言をした場合は、リアクションかコマンドで取り消してください。")
