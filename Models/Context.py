from datetime import datetime
from threading import Lock
from typing import List, Optional
import yaml
import os
from pathlib import Path

import discord
from discord.ext import commands

from Models.ClanMember import ClanMember
from Exceptions.ClanMemberNotFoundError import ClanMemberNotFoundError
from Models.LoadConfig import LoadConfig
from Models.SameTimeAttack import SameTimeAttack


class Context:
    """
    Singleton Object

    """
    _unique_instance = None
    _lock = Lock()

    # その他管理する値
    bot: commands.Bot
    clan_members: List[ClanMember]
    same_time_attack: SameTimeAttack  # 同時凸管理
    last_day_change_update: datetime  # 日付更新処理を行った日時
    attack_count_message: Optional[discord.Message]  # 凸数メッセージ

    def __new__(cls):
        raise NotImplementedError("Cannot initialize via Constructor")

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    async def get_instance(cls, bot: commands.Bot):
        if not cls._unique_instance:
            with cls._lock:
                if not cls._unique_instance:
                    cls._unique_instance = cls.__internal_new__()

                    # 初期化処理
                    cls.bot = bot
                    cls.clan_members = []
                    cls.same_time_attack = SameTimeAttack()
                    cls.last_day_change_update = datetime.now()
                    cls.attack_count_message = None
                    await cls._setup()

        return cls._unique_instance

    @classmethod
    async def _setup(cls):
        # 特定のロールのユーザを集める
        # note: 1つのguildのみにいれる想定
        target_guild: discord.Guild
        config: LoadConfig = LoadConfig.get_instance()
        for guild in cls.bot.guilds:
            if guild.id == config.target_guild_id:
                target_guild = guild
                break

        target_role: discord.Role
        for role in target_guild.roles:
            if role.id == config.target_role_id:
                target_role = role
        for member in target_role.members:
            cls.clan_members.append(ClanMember(await target_guild.fetch_member(member.id)))

    def check_managed_message(self, message: discord.Message, member: discord.Member) -> bool:
        # 全ユーザの管理メッセージと比較
        for clan_member in self.clan_members:
            if clan_member.attack_message == message and clan_member.discord_guild_member == member:
                return True
        return False

    def get_clan_member(self, user_id: int) -> ClanMember:
        for clan_member in self.clan_members:
            if clan_member.discord_guild_member.id == user_id:
                return clan_member
        raise ClanMemberNotFoundError()

    def get_now_attack_count(self) -> str:
        """
        現在の凸数を出力する
        :return:
        """
        now_datetime: datetime = datetime.now()
        format_str: str = "{} 時点での凸数\n".format(now_datetime.strftime("%m/%d %H:%M:%S"))
        remain_count: int = 0

        for i in range(ClanMember.MAX_ATTACK_COUNT + 1):
            row_data: str = ""
            members: List[ClanMember] = self._get_count_members(i)
            for member in members:
                row_data += "{} ".format(member.get_member_nickname())
            format_str += "{}凸 \n```\n {}\n```\n".format(i, row_data)

        # 持越しのメンバー取得
        carry_over_members: List[ClanMember] = self._get_carry_over_members()
        row_data: str = ""
        for member in carry_over_members:
            row_data += "{} ".format(member.get_member_nickname())
        format_str += "持越し\n```{} ```\n".format(row_data)

        # 残凸数
        for member in self.clan_members:
            remain_count += member.remain_attack_count()
        format_str += "残凸数: {}\n".format(remain_count)

        # 持越し
        format_str += "持越し数: {}\n".format(len(carry_over_members))

        return format_str

    def get_now_attack_member(self) -> str:
        return_message: str = ""
        for clan_member in self.clan_members:
            # 現在凸中かどうかチェック
            if clan_member.attack_message is None:
                continue

            # 凸中のメンバーのデータをフォーマットして渡す
            return_message += "{}さん\t\t{}凸目{}\n".format(
                clan_member.get_member_nickname(),
                clan_member.attack_status.attack_count + 1,
                "【持越し】" if clan_member.attack_status.is_carry_over else ""
            )
        return return_message

    async def reset_status(self, now_datetime: datetime):
        """
        状態のリセット処理を行う。
        - 凸状況リセット
        - ニックネームリセット
        - 同時凸状態解除
        - 新規凸数掲示板作成
        :param now_datetime:
        :return:
        """
        for clan_member in self.clan_members:
            clan_member.reset_status()
            await clan_member.update_member_name()
        self.same_time_attack = SameTimeAttack()
        self.last_day_change_update = now_datetime
        self.attack_count_message = None

    def _get_count_members(self, count: int) -> List[ClanMember]:
        return list(filter(lambda x: x.attack_status.attack_count == count, self.clan_members))

    def _get_carry_over_members(self) -> List[ClanMember]:
        return list(filter(lambda x: x.attack_status.is_carry_over, self.clan_members))
