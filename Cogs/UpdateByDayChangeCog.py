from datetime import datetime, time, timedelta

import discord
from discord.ext import commands, tasks

from yukarisan.Models.Context import Context


class UpdateByDayChangeCog(commands.Cog):
    """
    毎日5時に行う処理
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_day.start()

    @tasks.loop(seconds=30)
    async def change_day(self):
        context: Context = await Context.get_instance(self.bot)

        # 最後に更新した日時～今の日時で午前5時を跨いでいたら更新
        # 最後に更新した日時が00:00-04:59の場合は、その日の05:00
        last_update: datetime = context.last_day_change_update
        last_update_time: time = last_update.time()
        target_datetime: datetime
        if time(0, 0, 0) <= last_update_time <= time(4, 59, 59, 99):
            target_datetime = datetime(last_update.year, last_update.month, last_update.day, 5, 0, 0)
        else:
            next_day = last_update + timedelta(days=1)
            target_datetime = datetime(next_day.year, next_day.month, next_day.day, 5, 0, 0)

        # 目標日時を跨いでいたら実行して、実行日時を修正
        now_datetime: datetime = datetime.now()
        if last_update < target_datetime <= now_datetime:
            # Statusの更新
            context.reset_status(now_datetime)
            print("reset_status...{}".format(now_datetime.strftime("%H:%M:%S")))

        # 凸数管理メッセージが管理されていなかったら投稿してセットする
        if context.attack_count_message is None:
            return_message: str = context.get_now_attack_count()
            channel: discord.TextChannel = self.bot.get_channel(context.attack_status_channel_id)
            context.attack_count_message = await channel.send(return_message)
