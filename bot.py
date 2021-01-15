import os
from pathlib import Path

import discord
import yaml
from discord.ext import commands

from yukarisan.Cogs.AttackCog import AttackCog
from yukarisan.Cogs.AttackStatusCog import AttackStatusCog
from yukarisan.Cogs.CommandErrorHandlerCog import CommandErrorHandlerCog
from yukarisan.Cogs.PreviousClanMemberStatusCog import PreviousClanMemberStatusCog
from yukarisan.Cogs.SetupCog import SetupCog
from yukarisan.Cogs.BossLapCalcCog import BossLapCalcCog
from yukarisan.Cogs.AttackCancelCog import AttackCancelCog
from yukarisan.Cogs.AttackFinishCog import AttackFinishCog
from yukarisan.Cogs.UpdateAttackCountCog import UpdateAttackCountCog
from yukarisan.Cogs.UpdateByDayChangeCog import UpdateByDayChangeCog
from yukarisan.Cogs.UseTaskKillCog import UseTaskKillCog
from yukarisan.Cogs.SameTimeAttackStartCog import SameTimeAttackStartCog
from yukarisan.Cogs.SameTimeAttackAddMemberCog import SameTimeAttackAddMemberCog
from yukarisan.Cogs.SameTimeAttackReportCog import SameTimeAttackReportCog
from yukarisan.Cogs.SameTimeAttackCommitCog import SameTimeAttackCommitCog
from yukarisan.Cogs.SameTimeAttackEndCog import SameTimeAttackEndCog
from yukarisan.Cogs.AttackOverKillCog import AttackOverKillCog
from yukarisan.Cogs.AttackCountWriteCog import AttackCountWriteCog

if __name__ == '__main__':
    # intentを入れないとメンバーが取れない
    intents: discord.Intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='', intents=intents)

    # start up
    bot.add_cog(SetupCog(bot))

    # 凸管理機能
    bot.add_cog(AttackCog(bot))
    bot.add_cog(AttackCancelCog(bot))
    bot.add_cog(AttackFinishCog(bot))
    bot.add_cog(AttackOverKillCog(bot))
    bot.add_cog(UseTaskKillCog(bot))
    bot.add_cog(AttackStatusCog(bot))
    bot.add_cog(PreviousClanMemberStatusCog(bot))

    # 同時凸機能
    bot.add_cog(SameTimeAttackStartCog(bot))
    bot.add_cog(SameTimeAttackAddMemberCog(bot))
    bot.add_cog(SameTimeAttackReportCog(bot))
    bot.add_cog(SameTimeAttackCommitCog(bot))
    bot.add_cog(SameTimeAttackEndCog(bot))

    # サブ機能
    bot.add_cog(AttackCountWriteCog(bot))
    bot.add_cog(BossLapCalcCog(bot))

    # schedule
    bot.add_cog(UpdateByDayChangeCog(bot))
    bot.add_cog(UpdateAttackCountCog(bot))

    # ErrorHandling
    bot.add_cog(CommandErrorHandlerCog(bot))

    # tokenを取得する
    path: Path = Path(os.path.dirname(os.path.abspath(__file__)))
    abs_dir: str = str(path)
    token: str
    with open(r'{}\appsettings.yml'.format(abs_dir), "r", encoding="utf-8_sig") as f:
        settings = yaml.safe_load(f)
        token = settings["discord_bot_token"]
    # Botの起動とDiscordサーバーへの接続
    bot.run(token)
