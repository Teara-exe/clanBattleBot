import discord

from yukarisan.Exceptions.AlreadyAttackError import AlreadyAttackError


class ErrorHandling:
    @staticmethod
    async def send_error_message(message: discord.Message, exception: Exception):
        send_str: str = "不明なエラーです。開発者に問い合わせてください。"
        if exception is AlreadyAttackError:
            send_str = "先に凸完了宣言をしてください"

        await message.reply(send_str)
