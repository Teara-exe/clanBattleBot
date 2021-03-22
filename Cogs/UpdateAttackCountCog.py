from discord.ext import commands, tasks

from Models.Context import Context


class UpdateAttackCountCog(commands.Cog):
    """
    凸数表示の更新処理
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_attack_count.start()

    @tasks.loop(seconds=60)
    async def update_attack_count(self):
        context: Context = await Context.get_instance(self.bot)
        if context.attack_count_message is None:
            return
        await context.attack_count_message.edit(content=context.get_now_attack_count())

