from datetime import datetime
from typing import List

from yukarisan.GachaRate import GachaRate
from yukarisan.GachaSchedule import GachaSchedule


class Gacha:
    pname = ['ユイ(プリンセス)', 'コッコロ(プリンセス)', 'ペコリーヌ(プリンセス)', 'クリスティーナ', 'ムイミ', 'ネネカ']
    s3name = ['マコト', 'キョウカ', 'トモ', 'ルナ', 'カスミ', 'ジュン', 'アリサ', 'アン', 'クウカ(オーエド)',
              'ニノン(オーエド)', 'ミミ(ハロウィン)', 'ルカ', 'クロエ', 'イリヤ', 'アンナ', 'グレア', 'カヤ',
              'イリヤ(クリスマス)', 'カスミ(マジカル)', 'ノゾミ', 'マホ', 'シズル', 'サレン', 'ジータ', 'ニノン',
              'リノ', 'アキノ', 'モニカ', 'イオ', 'ハツネ', 'アオイ(編入生)', 'ユニ', 'チエル', 'リン(レンジャー)',
              'マヒル(レンジャー)', 'リノ(ワンダー)', 'イノリ', 'ナナカ(サマー)']
    s2name = ['カオリ', 'ナナカ', 'エリコ', 'シオリ', 'ミミ', 'タマキ', 'マツリ', 'スズナ', 'ミヤコ', 'クウカ',
              'アカリ', 'ミツキ', 'ツムギ', 'ミサト', 'アヤネ', 'シノブ', 'チカ', 'ミフユ', 'リン', 'ユキ', 'マヒル']
    s1name = ['レイ', 'ヨリ', 'ヒヨリ', 'リマ', 'ユカリ', 'クルミ', 'ミソギ', 'スズメ', 'アユミ', 'アオイ', 'ミサキ']

    limited = ['ユイ(ニューイヤー)', 'ヒヨリ(ニューイヤー)', 'キャル(ニューイヤー)', 'コッコロ(ニューイヤー)',
               'シズル(バレンタイン)', 'ペコリーヌ(サマー)', 'スズメ(サマー)', 'タマキ(サマー)', 'キャル(サマー)',
               'スズナ(サマー)', 'サレン(サマー)', 'マホ(サマー)', 'マコト(サマー)', 'ルカ(サマー)',
               'シノブ(ハロウィン)', 'キョウカ(ハロウィン)', 'チカ(クリスマス)', 'アヤネ(クリスマス)',
               'クリスティーナ(クリスマス)', 'エミリア', 'レム', 'ウヅキ(デレマス)', 'リン(デレマス)', ]
    event = ['レイ(ニューイヤー)', 'スズメ(ニューイヤー)', 'エリコ(バレンタイン)', 'コッコロ(サマー)',
             'ミフユ(サマー)', 'イオ(サマー)', 'カオリ(サマー)', 'アンナ(サマー)', 'ミヤコ(ハロウィン)',
             'ミソギ(ハロウィン)', 'クルミ(クリスマス)', 'ノゾミ(クリスマス)', 'ラム', 'ミオ(デレマス)',
             'アユミ(ワンダー)', 'キャル', 'ペコリーヌ', 'コッコロ', 'ユイ']

    def __init__(self):
        self.gachabox: List[GachaRate] = []
        self.limitdate = '2000/01/01 00:00:00'
        self.gachatype = '3'
        self.prize = False

    def GachaSave(self):
        global GachaData

        GachaData = []
        for n in self.s3name:
            GachaData.append(GachaSchedule('2000/01/01 00:00:00', '3', n))

        for n in self.s2name:
            GachaData.append(GachaSchedule('2000/01/01 00:00:00', '2', n))

        for n in self.s1name:
            GachaData.append(GachaSchedule('2000/01/01 00:00:00', '1', n))

        for n in self.pname:
            GachaData.append(GachaSchedule('2000/01/01 00:00:00', 'f', n))

        GachaData.append(GachaSchedule('2020/06/24 12:00:00', 'p', 'クリスティーナ(クリスマス)'))
        GachaData.append(GachaSchedule('2020/06/30 12:00:00', 'f', 'ユイ(プリンセス)'))

        GlobalStorage.save()

    @staticmethod
    def typetoindex(c) -> int:
        if (c == 'd'): return 0
        if (c == 'l'): return 0
        if (c == 'p'): return 0
        if (c == 'f'): return 1
        if (c == '3'): return 2
        if (c == '2'): return 3
        if (c == '1'): return 4
        return -1

    def PickUpDelete(self, name):
        if type(name) is list:
            for m in name:
                self.PickUpDelete(m)

        for gacharate in self.gachabox:
            if name in gacharate.namelist:
                gacharate.namelist.remove(name)

    def Decorate(self):
        for i in range(len(self.gachabox[0].namelist)):
            self.gachabox[0].namelist[i] += ' PicuUp!'

        for i in range(len(self.gachabox[1].namelist)):
            self.gachabox[1].namelist[i] += ' PriFes!'

    def FindPrincess(self, name):
        if len(self.gachabox) == 0:
            self.GetBoxData()

        if name in self.limited: return 'l'
        if name in self.gachabox[0].namelist: return self.gachatype
        if name in self.gachabox[1].namelist: return 'f'
        if name in self.gachabox[2].namelist: return '3'
        if name in self.gachabox[3].namelist: return '2'
        if name in self.gachabox[4].namelist: return '1'

        return '0'

    @staticmethod
    def AppendList(namelist, name):
        if type(name) is list:
            for n in name:
                if n not in namelist:
                    namelist.append(n)
        else:
            if name not in namelist:
                namelist.append(name)

    def BoxReset(self):
        self.gachabox = []
        self.limitdate = '2000/01/01 00:00:00'

    def GetBoxData(self) -> List[GachaRate]:
        datetime_format = datetime.datetime.now()
        datestr = datetime_format.strftime("%Y/%m/%d %H:%M:%S")  # 2017/11/12 09:55:28

        if self.limitdate is None:
            if GachaData[-1].startdate <= datestr:
                return self.gachabox
        elif datestr < self.limitdate:
            return self.gachabox

        self.limitdate = None
        pickup = None
        self.gachabox: List[GachaRate] = [
            GachaRate(0.0, 3, []),
            GachaRate(0.0, 3, []),
            GachaRate(0.0, 3, []),
            GachaRate(0.0, 2, []),
            GachaRate(0.0, 1, []),
        ]

        for m in GachaData:
            if datestr < m.startdate:
                self.limitdate = m.startdate
                break

            pickup = m
            n = self.typetoindex(m.gachatype)
            if 0 < n:
                self.AppendList(self.gachabox[n].namelist, m.name)
            else:
                self.AppendList(self.limited, m.name)

        self.PickUpDelete(pickup.name)
        self.AppendList(self.gachabox[0].namelist, pickup.name)
        self.Decorate()

        lot = GachaLotData[0]
        if pickup.gachatype == 'l': lot = GachaLotData[1]
        if pickup.gachatype == 'p': lot = GachaLotData[2]
        if pickup.gachatype == 'd': lot = GachaLotData[3]
        if pickup.gachatype == 'f': lot = GachaLotData[4]

        for m in range(len(lot)):
            self.gachabox[m].rate = lot[m]

        if pickup.gachatype == 'p':
            self.prize = True
        else:
            self.prize = False

        self.gachatype = pickup.gachatype

        return self.gachabox

    @staticmethod
    def NameListToString(namelist):
        if type(namelist) is str:
            return namelist
        if type(namelist) is list:
            return ','.join(namelist)
        return ''

    def ToString(self):
        self.GetBoxData()

        message = ''
        message += '%s %s\n' % (self.GachaType(self.gachatype), GachaData[-1].startdate)

        for rate in self.gachabox:
            unitrate = 0.0 if len(rate.namelist) <= 0 else rate.rate / len(rate.namelist)
            message += '%0.3f(%0.3f) %d %s len:%d\n' % (
            rate.rate, unitrate, rate.star, rate.namelist[-1], len(rate.namelist))

        return message

    @staticmethod
    def GachaType(g):
        if g == '1': return '恒常星1'
        if g == '2': return '恒常星2'
        if g == '3': return '恒常星3'
        if g == 'l': return '限定'
        if g == 'd': return '2倍'
        if g == 'p': return 'プライズ'
        if g == 'f': return 'プリフェス'
        return 'Unknown'

    @staticmethod
    def GachaScheduleData():
        message = ''
        num = 0
        for m in reversed(GachaData):
            if 9 <= num or m.startdate <= '2000/01/01 00:00:00':
                break
            message += '%d: %s [%s] [%s]\n' % (
            num + 1, m.startdate, Gacha.GachaType(m.gachatype), Gacha.NameListToString(m.name))
            num += 1

        return message

    @staticmethod
    def Lottery(box: List[T], leaststar=1) -> T:
        rndstar = random.random() * 100
        before = None
        for b in box:
            if b.star < leaststar:
                return before

            if rndstar <= b.rate:
                return b

            rndstar -= b.rate
            before = b

    @staticmethod
    def LotteryPrincess(box: List[GachaRate], leaststar=1) -> Princess:

        b = Gacha.Lottery(box, leaststar)
        p = random.randint(0, len(b.namelist) - 1)
        return Princess(b.namelist[p], b.star)

    @staticmethod
    def LotteryPrize(leaststar=1) -> PrizeRate:
        box = [
            PrizeRate(0.5, 6, 40, 5, 5),
            PrizeRate(1, 5, 20, 5, 3),
            PrizeRate(5, 4, 5, 1, 3),
            PrizeRate(10, 3, 1, 1, 2),
            PrizeRate(23.5, 2, 0, 1, 1),
            PrizeRate(100, 1, 0, 1, 0),
        ]

        return Gacha.Lottery(box, leaststar)