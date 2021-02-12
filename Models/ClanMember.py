import re
from typing import Optional, List

import discord

from Exceptions.AlreadyAttackError import AlreadyAttackError
from Exceptions.AlreadyUseTaskKillError import AlreadyUseTaskKillError
from Exceptions.NotAttackError import NotAttackError
from Exceptions.MaxAttackError import MaxAttackError
from Models.AttackStatus import AttackStatus
from Models.ClanBattleEmoji import ClanBattleEmoji
from Models.LoadConfig import LoadConfig


class ClanMember:
    """
    クランメンバーの状態を管理する
    """
    MAX_ATTACK_COUNT = 3

    # ---- attributes ---- #
    # discordのUserデータ
    discord_guild_member: discord.Member

    # 凸中かどうか(メッセージ管理してれば凸中)
    attack_message: Optional[discord.Message]

    # 現在の凸状態
    attack_status: AttackStatus
    # 過去の凸状態
    attack_history: List[AttackStatus]

    def __init__(self, member: discord.Member):
        """
        管理データ初期化
        """
        self.discord_guild_member = member
        self.reset_status()

    def reset_status(self):
        """
        管理データを初期化する
        :return:
        """
        self.attack_message = None
        self.attack_status = AttackStatus(is_carry_over=False, attack_count=0, use_task_kill=False)
        self.attack_history = []

    async def get_attack_message_copy(self) -> discord.Message:
        """
        messageのcopyを取得する
        :return:
        """
        return await self.attack_message.channel.fetch_message(self.attack_message.id)

    @staticmethod
    async def _reaction_to_message(message: discord.Message, message_str: str):
        """
        凸終了/キャンセル時の反応処理
        :param message:
        :param message_str:
        :return:
        """
        # configの設定値をもとに、mentionにするかreactionにするか変える
        config: LoadConfig = LoadConfig.get_instance()
        if config.use_emoji_reaction:
            await message.add_reaction(ClanBattleEmoji.THUMBS_UP)
        else:
            await message.reply(message_str)

    def attack(self, message: discord.Message):
        """
        凸処理
        :return:
        """
        # 凸終了が出てないのに宣言するのはおかしい
        if self.attack_message is not None:
            raise AlreadyAttackError('先に凸完了宣言をしてください')

        # 3凸超えて凸するのはおかしい
        if self.attack_status.attack_count >= ClanMember.MAX_ATTACK_COUNT:
            raise MaxAttackError()

        self.attack_message = message

    async def finish(self, is_kill: bool):
        """
        凸完了処理

        持越しが発生した場合・持越しで凸した場合は処理が異なるので注意

        :param is_kill:
        :return:
        """
        # 凸宣言がなかった場合はエラー
        if self.attack_message is None:
            raise NotAttackError()

        # リアクション生成(先に作っておかないと、持ち越しなのかどうなのかが不明になる)
        return_message: str = "{} さんの{}凸目{}を終了しました".format(
            self.get_member_nickname(),
            self.attack_status.attack_count + 1,
            "(持越し)" if self.attack_status.is_carry_over else ""
        )

        # 現在の凸状態を履歴に残す
        self.attack_history.append(self.attack_status)
        prev_attack_status: AttackStatus = self.attack_status

        # 持越し凸の場合は倒したかどうかにかかわらず持越しなし
        if self.attack_status.is_carry_over:
            self.attack_status = AttackStatus(is_carry_over=False,
                                              attack_count=prev_attack_status.attack_count + 1,
                                              use_task_kill=prev_attack_status.use_task_kill)
        # 持越し無し＋討伐で持越しあり
        else:
            if is_kill:
                self.attack_status = AttackStatus(is_carry_over=True,
                                                  attack_count=prev_attack_status.attack_count,
                                                  use_task_kill=prev_attack_status.use_task_kill)
                return_message += "【持越し発生】"
            else:
                self.attack_status = AttackStatus(is_carry_over=False,
                                                  attack_count=prev_attack_status.attack_count + 1,
                                                  use_task_kill=prev_attack_status.use_task_kill)

        # レスポンスより先に凸状態を消すので、コピーを取っておく
        response_target_message: discord.Message = await self.get_attack_message_copy()

        # 凸状態削除
        self.attack_message = None

        # リアクション送信
        await ClanMember._reaction_to_message(response_target_message, return_message)

        # ニックネーム変更
        await self.update_member_name()

    async def cancel(self):
        """
        凸キャンセル処理

        :return:
        """
        if self.attack_message is None:
            raise NotAttackError()

        # レスポンスより先に凸状態を消すので、コピーを取っておく
        response_target_message: discord.Message = await self.get_attack_message_copy()

        # 凸前状況と凸後状況が変わらない(ｷｬﾝｾﾙ)のため、更新の前でも後でも問題なし
        return_message: str = "{} さんの{}凸目{}をキャンセルしました".format(
            self.get_member_nickname(),
            self.attack_status.attack_count + 1,
            "(持越し)" if self.attack_status.is_carry_over else ""
        )

        # 凸状態リセット
        self.attack_message = None

        # リアクション送信
        await ClanMember._reaction_to_message(response_target_message, return_message)

    async def exec_task_kill(self, message: discord.Message):
        """
        タスキル使用処理
        :return:
        """
        # タスクキルをすでにしてたらダメ
        if self.attack_status.use_task_kill:
            raise AlreadyUseTaskKillError()
        # そもそも凸していないときはタスキルできない
        if self.attack_message is None:
            raise NotAttackError()

        # status 更新
        self.attack_history.append(self.attack_status)
        previous_status: AttackStatus = self.attack_status
        self.attack_status = AttackStatus(is_carry_over=previous_status.is_carry_over,
                                          attack_count=previous_status.attack_count,
                                          use_task_kill=True)

        self.attack_message = None

        # キャンセル処理
        return_message: str = "【タスキル使用】{} さんの{}凸目{}をキャンセルしました".format(
            self.get_member_nickname(),
            self.attack_status.attack_count + 1,
            "(持越し)" if self.attack_status.is_carry_over else ""
        )
        await message.reply(return_message)

        # ニックネーム変更
        await self.update_member_name()

    async def previous_status(self, message: discord.Message):
        """
        状態をひとつ前に戻す
        :return:
        """
        if len(self.attack_history) == 0:
            raise Exception()

        # 戻す前の凸状況を保持しておく
        previous_attack_status: AttackStatus = self.attack_status

        # 凸状態をひとつ前に戻す
        self.attack_status = self.attack_history.pop(-1)

        # ひとつ前の凸状況
        previous_status_message: str = "【前回】{}凸 {} {}".format(
            previous_attack_status.attack_count,
            "【持越し】" if previous_attack_status.is_carry_over else "",
            "【タスキル済み】" if previous_attack_status.use_task_kill else "")
        # 今回の凸状況
        now_status_message: str = "【今回】{}凸 {} {} ".format(
            self.attack_status.attack_count,
            "【持越し】" if self.attack_status.is_carry_over else "",
            "【タスキル済み】" if self.attack_status.use_task_kill else "")
        return_message: str = "{}さんの状態を変更しました。\n{}\n{}".format(self.get_member_nickname(),
                                                               previous_status_message, now_status_message)
        # 該当チャンネルに返信する
        await message.reply(return_message)

        # ニックネーム変更
        await self.update_member_name()

    def get_member_nickname(self) -> str:
        """
        ユーザのニックネームを取得する
        :return:
        """
        return re.sub(r'__.+$', '', self.discord_guild_member.display_name)

    async def update_member_name(self):
        """
        ユーザ名に状態を追加する
        本機能は権限周りに問題があれば例外で止まってしまうので、エラーを握りつぶします
        :return:
        """
        # 設定値で設定が入ってない場合は何もしない
        config: LoadConfig = LoadConfig.get_instance()
        if not config.is_change_nickname:
            return

        user_name: str = self.get_member_nickname()

        # 0.5凸以上 / タスキル利用済みの場合はニックネーム変更
        if self.attack_status.attack_count != 0 or self.attack_status.is_carry_over or self.attack_status.use_task_kill:
            # 凸回数追加
            user_name += '__{}'.format(self.attack_status.attack_count)
            # 持越しがあれば持越し追加
            user_name += '.5凸' if self.attack_status.is_carry_over else '凸'
            # タスキルしてればその旨を追加
            user_name += '_タスキル済み' if self.attack_status.use_task_kill else ''

        try:
            await self.discord_guild_member.edit(nick=user_name)
        except:
            print("nickname変更のパーミッションエラーを握りつぶしました")

    def remain_attack_count(self) -> int:
        return ClanMember.MAX_ATTACK_COUNT - self.attack_status.attack_count
