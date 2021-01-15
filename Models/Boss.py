class Boss:
    LEVEL_UP_LAP = [4, 11, 35, 45, 100000]
    BOSS_HP = [
        [[600, 1.2], [800, 1.2], [1000, 1.3], [1200, 1.4], [1500, 1.5]],
        [[600, 1.6], [800, 1.6], [1000, 1.8], [1200, 1.9], [1500, 2.0]],
        [[700, 2.0], [900, 2.0], [1200, 2.4], [1500, 2.4], [2000, 2.6]],
        [[1700, 3.5], [1800, 3.5], [2000, 3.7], [2100, 3.8], [2300, 4.0]],
        [[8500, 3.5], [9000, 3.5], [9500, 3.7], [10000, 3.8], [11000, 4.0]]
    ]

    now_lap: int
    now_boss: int

    def __init__(self):
        pass

    def next_boss(self):
        # 現在のボスを確定させる
        self.now_boss += 1
        if self.now_boss >= len(Boss.BOSS_HP[0]):
            self.now_boss = 1
            self.now_lap += 1

    def prev_boss(self):
        # 一個前に戻る
        self.now_boss -= 1
        if self.now_boss <= 0:
            self.now_boss = len(Boss.BOSS_HP[0])
            self.now_lap -= 1

    def reset_status(self):
        self.now_lap = 1
        self.now_boss = 1

    @staticmethod
    def now_lap(score: int) -> (int, int):
        sum_all: int = 0
        now_lap: int = 0
        now_boss_target: int = 1

        loop_break_flag: bool = False

        for lap in range(1, 300):

            now_lap = lap
            # 現在の段階目を取得する
            step: int = 0
            for i, border_lap in enumerate(Boss.LEVEL_UP_LAP):
                step = i
                # 現在のlapを超えていなかったら終了
                if lap < border_lap:
                    break
            # スコア計算
            boss_no: int = 0
            for hp, rate in Boss.BOSS_HP[step]:
                boss_no += 1
                now_boss_target = boss_no
                sum_all += hp * rate
                if score < sum_all:
                    loop_break_flag = True
                    break

            # これ以上ループしなくていい場合は終了
            if loop_break_flag:
                break

        return now_lap, now_boss_target

    @staticmethod
    def __calc_next_step(next_lap: int) -> int:
        now_step: int = 1
        for cnt, border in enumerate(Boss.LEVEL_UP_LAP):
            if next_lap >= border:
                now_step = cnt + 1
            else:
                break
        return now_step
