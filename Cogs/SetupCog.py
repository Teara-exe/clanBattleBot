from discord.ext import commands

from Models.Context import Context


class SetupCog(commands.Cog):
    """
    初回起動時に行う処理。

    ロールからクラメンを取得し、内部データに保持する
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # 起動時にContextを生成しておく
        await Context.get_instance(self.bot)

        print("finish set up.")
