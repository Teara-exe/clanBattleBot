class AttackStatus:
    # 持越し中かどうか
    is_carry_over: bool
    # 凸回数
    attack_count: int
    # タスクキルしたかどうか
    use_task_kill: bool

    def __init__(self, is_carry_over: bool, attack_count: int, use_task_kill: bool):
        self.is_carry_over = is_carry_over
        self.attack_count = attack_count
        self.use_task_kill = use_task_kill
