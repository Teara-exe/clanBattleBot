from typing import List

import discord
from Exceptions.AlreadySameAttackStartError import AlreadySameAttackStartError
from Exceptions.NotSameAttackStartError import NotSameAttackStartError
from Exceptions.AlreadySameAttackStartMemberError import AlreadySameAttackStartMemberError


class SameAttackData:
    """
    同時凸開始時に集計するデータ
    """
    member: discord.abc.User
    suspect_damage: int
    real_damage: int

    def __init__(self, member: discord.abc.User, suspect: int):
        self.member = member
        self.suspect_damage = suspect
        self.real_damage = 0


class SameTimeAttack:
    """
    同時凸管理データ
    """
    same_time_start_flag: bool
    attack_info: List[SameAttackData]
    remain: int

    def __init__(self):
        self.same_time_start_flag = False
        self.attack_info = []

    def start(self, remain: int):
        """
        同時凸開始時の処理

        :param remain:
        :return:
        """
        # 既に出てきたらNG
        if self.same_time_start_flag:
            raise AlreadySameAttackStartError()

        # 残HPと殴り開始を保存
        self.remain = remain
        self.same_time_start_flag = True

    def add_member(self, member: discord.abc.User, suspect: int):
        """
        同時凸開始メンバー追加
        :param member:
        :param suspect:
        :return:
        """
        # 同時凸開始している人はスルー
        for same_attack_data in self.attack_info:
            if same_attack_data.member == member:
                raise AlreadySameAttackStartMemberError()
        # 凸データ追加
        self.attack_info.append(SameAttackData(member, suspect))

    def real_damage_add(self, member: discord.abc.User, real_damage: int):
        """
        予測ダメージを追加
        :param member:
        :param real_damage:
        :return:
        """
        same_attack_data: SameAttackData = self._search_same_attack_member(member)
        same_attack_data.real_damage = real_damage

    def commit_damage(self, member: discord.Member, commit_damage: int):
        """
        ダメージの確定処理
        :param member:
        :param commit_damage:
        :return:
        """
        self._remove_same_attack_member(member)
        self.remain -= commit_damage

    def end(self):
        """
        同時凸終了処理

        :return:
        """
        if not self.same_time_start_flag:
            raise NotSameAttackStartError()
        self._reset()

    def format_status(self) -> str:
        """
        同時凸状態の出力
        :return:
        """
        suspect_remain: int = self.remain
        real_remain: int = self.remain

        format_member_str: str = ""
        for same_attack_data in self.attack_info:
            suspect_remain -= same_attack_data.suspect_damage
            real_remain -= same_attack_data.real_damage
            format_member_str += "{}\t\t予測:{}万\t\t実際:{}万\n".format(
                same_attack_data.member.display_name, same_attack_data.suspect_damage, same_attack_data.real_damage)

        format_summary_str: str = "現在の残り：{}万  予測: {}万  実際: {}万\n".format(self.remain, suspect_remain, real_remain)

        return "```\n{}{}```".format(format_summary_str, format_member_str)

    def _reset(self):
        """
        リセット処理
        :return:
        """
        self.attack_info = []
        self.remain = 0
        self.same_time_start_flag = False

    def _search_same_attack_member(self, member: discord.abc.User) -> SameAttackData:
        """
        同時凸メンバーの検索
        :param member:
        :return:
        """
        for same_attack_data in self.attack_info:
            if same_attack_data.member == member:
                return same_attack_data

    def _remove_same_attack_member(self, member: discord.abc.User):
        """
        同時凸メンバーの削除
        :param member:
        :return:
        """
        same_attack_member: SameAttackData = self._search_same_attack_member(member)
        self.attack_info.remove(same_attack_member)
