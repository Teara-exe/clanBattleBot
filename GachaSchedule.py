class GachaSchedule:
    def __init__(self, startdate, gachatype, name):
        self.startdate = startdate
        self.gachatype = gachatype
        self.name = name

    def Serialize(self):
        ret = {}
        ignore = []

        for key, value in self.__dict__.items():
            if not key in ignore:
                ret[key] = value

        return ret

    @staticmethod
    def Deserialize(dic):
        result = GachaSchedule('', '', '')
        for key, value in dic.items():
            result.__dict__[key] = value
        return result