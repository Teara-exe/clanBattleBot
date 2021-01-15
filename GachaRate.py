from typing import List


class GachaRate:
    def __init__(self, rate, star, namelist):
        self.rate: float = rate
        self.star: int = star
        self.namelist: List[str] = namelist
