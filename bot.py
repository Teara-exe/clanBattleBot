import os
from pathlib import Path

import discord
import yaml
from discord.ext import commands
from Cogs import *
from Models.LoadConfig import LoadConfig

if __name__ == '__main__':
    # intentを入れないとメンバーが取れない
    intents: discord.Intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='', intents=intents)

    # start up
    bot.add_cog(SetupCog.SetupCog(bot))

    # 凸管理機能
    bot.add_cog(AttackCog.AttackCog(bot))
    bot.add_cog(AttackCancelCog.AttackCancelCog(bot))
    bot.add_cog(AttackFinishCog.AttackFinishCog(bot))
    bot.add_cog(AttackOverKillCog.AttackOverKillCog(bot))
    bot.add_cog(UseTaskKillCog.UseTaskKillCog(bot))
    bot.add_cog(AttackStatusCog.AttackStatusCog(bot))
    bot.add_cog(PreviousClanMemberStatusCog.PreviousClanMemberStatusCog(bot))

    # 同時凸機能
    bot.add_cog(SameTimeAttackStartCog.SameTimeAttackStartCog(bot))
    bot.add_cog(SameTimeAttackAddMemberCog.SameTimeAttackAddMemberCog(bot))
    bot.add_cog(SameTimeAttackReportCog.SameTimeAttackReportCog(bot))
    bot.add_cog(SameTimeAttackCommitCog.SameTimeAttackCommitCog(bot))
    bot.add_cog(SameTimeAttackEndCog.SameTimeAttackEndCog(bot))

    # サブ機能
    bot.add_cog(AttackCountWriteCog.AttackCountWriteCog(bot))
    bot.add_cog(BossLapCalcCog.BossLapCalcCog(bot))

    # schedule
    bot.add_cog(UpdateByDayChangeCog.UpdateByDayChangeCog(bot))
    bot.add_cog(UpdateAttackCountCog.UpdateAttackCountCog(bot))

    # ErrorHandling
    bot.add_cog(CommandErrorHandlerCog.CommandErrorHandlerCog(bot))

    # tokenを取得する
    config: LoadConfig = LoadConfig.get_instance()
    token: str = config.discord_bot_token

    # Botの起動とDiscordサーバーへの接続
    bot.run(token)
