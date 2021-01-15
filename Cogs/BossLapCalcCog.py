from discord.ext import commands

from yukarisan.Models.Boss import Boss


class BossLapCalcCog(commands.Cog):
    """
    スコアから何週目かと、どのボスまで回っているのか逆算する

    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="score")
    async def on_score(self, ctx: commands.context.Context, *args):
        score: int = int(args[0])
        now_lap, now_target = Boss.now_lap(score)
        print(now_lap, now_target)
