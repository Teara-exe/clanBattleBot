from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError

from Exceptions.AlreadyAttackError import AlreadyAttackError
from Exceptions.AlreadySameAttackStartError import AlreadySameAttackStartError
from Exceptions.AlreadySameAttackStartMemberError import AlreadySameAttackStartMemberError
from Exceptions.AlreadyUseTaskKillError import AlreadyUseTaskKillError
from Exceptions.ClanMemberNotFoundError import ClanMemberNotFoundError
from Exceptions.MaxAttackError import MaxAttackError
from Exceptions.NotAttackError import NotAttackError
from Exceptions.NotExistPreviousAttackStatusException import NotExistPreviousAttackStatusException
from Exceptions.NotSameAttackStartError import NotSameAttackStartError


class CommandErrorHandlerCog(commands.Cog):
    """
    コマンドエラー時のハンドリング処理
    """
    # ---- attributes ----
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.context.Context, error):
        send_str: str = "不明なエラーです。開発者に問い合わせてください。"

        # コマンドないエラーは無視する
        if isinstance(error, CommandNotFound):
            return

        # 自分が投げたエラーは原因がわかるので、エラーメッセージを書き換える
        if isinstance(error, CommandInvokeError):
            if isinstance(error.original, AlreadyAttackError):
                send_str = "先に凸完了宣言をしてください。\nメッセージが見つからない、リアクションを押しても動かない場合は「キャンセル」、もしくは「c」と送信してください。"
            elif isinstance(error.original, AlreadySameAttackStartError):
                send_str = "既に同時凸が開始されています。先に前の同時凸を終了させてください。"
            elif isinstance(error.original, AlreadySameAttackStartMemberError):
                send_str = "既に同時凸のメンバーに含まれています。"
            elif isinstance(error.original, AlreadyUseTaskKillError):
                send_str = "既にタスクキルを使っています"
            elif isinstance(error.original, ClanMemberNotFoundError):
                send_str = "クラメンにクラバト用ロールが付与されていません。管理者に問い合わせてください。"
            elif isinstance(error.original, MaxAttackError):
                send_str = "既に3凸完了しています。"
            elif isinstance(error.original, NotAttackError):
                send_str = "先に凸宣言をしてください。"
            elif isinstance(error.original, NotSameAttackStartError):
                send_str = "同時凸か開始されていません。"
            elif isinstance(error.original, NotExistPreviousAttackStatusException):
                send_str = "これ以上戻ることはできません。"

        await ctx.message.reply(send_str)
