import os
from pathlib import Path
from threading import Lock

import yaml


class LoadConfig:
    """
    Singleton Object

    設定ファイルの読み込みをして、値を保持する
    """
    _unique_instance = None
    _lock = Lock()

    # member variables
    discord_bot_token: str
    target_guild_id: int
    target_role_id: int
    attack_management_channel_id: int
    attack_status_channel_id: int
    is_change_nickname: bool

    def __new__(cls):
        raise NotImplementedError("Cannot initialize via Constructor")

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            with cls._lock:
                if not cls._unique_instance:
                    cls._unique_instance = cls.__internal_new__()

                    # 設定ファイルの読み込みを行う
                    path: Path = Path(os.path.dirname(os.path.abspath(__file__)))
                    abs_dir: str = str(path.parent)
                    with open(os.path.join(abs_dir, 'appsettings.yml'), "r", encoding="utf-8_sig") as f:
                        settings = yaml.safe_load(f)
                        cls.discord_bot_token = settings["discord_bot_token"]
                        cls.target_guild_id = settings["target_guild_id"]
                        cls.target_role_id = settings["target_role_id"]
                        cls.attack_management_channel_id = settings["attack_management_channel_id"]
                        cls.attack_status_channel_id = settings["attack_status_channel_id"]
                        cls.is_change_nickname = settings["is_change_nickname"]

        return cls._unique_instance
