from typing import List
from bs4 import BeautifulSoup

"""
主要结构如下:
> 单词名称 
    > 单词名称-属性2发音2
        > 例句1
        > 例句2
        > 例句3
    > 单词名称-属性2-发音2
        > ...
    ....

"""

class Dictionary():
    def __init__(self, src: BeautifulSoup):
        # 单词解释实体, 可能有多个意义
        self._dictEntry: List[DictEntry] = []
        # 单词起源
        self._etym = []
        self._populate(src)
        
        
    def _populate(self, src: BeautifulSoup):
        '''
        填充子属性
        '''
        pass


class DictEntry():
    """
    字典实体类, 包含了字典介绍及实体.
    通常一个词性对应一个实体, 例如一个词既有名词属性又有动词属性, 则可能有两个DictEntry
    """
    def __init__(self, src: BeautifulSoup):
        self._dictionary_intro = ''
        self._entry: Entry = Entry(BeautifulSoup())
        self._populate(src)

    def _populate(self, src: BeautifulSoup):
        pass


class Entry():
    """
    DictEntry中的实体, 包含Head与Sense, 暂时已知以下两类:
        1. IdoceEntry
        2. BussDictEntry
    """
    def __init__(self, src: BeautifulSoup):
        self._head = Head(BeautifulSoup())
        self._sense = Sense(BeautifulSoup())


class IdoceEntry(Entry):
    """
    朗文当代英语
    """
    def __init__(self, src: BeautifulSoup):
        super().__init__(src)


class BussDictEntry(Entry):
    """
    朗文商业英语
    """
    def __init__(self, src: BeautifulSoup):
        super().__init__(src)


class Head():
    """
    单词的主要信息, 包含音标, 发音, 词性等
    """
    def __init__(self, src: BeautifulSoup):
        # header word
        self._hwd = ''
        # 连字符
        self._hyphenation = ''
        # 上标
        self._homnum = ''
        # 音标
        self._pron_codes = ''
        # 单词等级
        self._tooltip_levle = ''
        # TODO 单词频率, 采用缩写方式, 此频率是朗文分级, 具体分级???
        self._freq = []
        self._ac = ''
        # 词性
        self._pos = ''
        # 英音发音地址
        self._brefile = ''
        # 美音发音地址
        self._amefile = ''
        # 词性具体类型(有些head中可能不存在, Sense中也存在该属性), 例如: 名词的可数与不可数, 动词的及物与不及物
        self._gram = ''


class Sense():
    """
    单词的每个具体解释(一个单词通常有多个解释)
    """
    def __init__(self, src: BeautifulSoup) -> None:
        # 单词解释序号, 可选
        self._sense_num = ''
        self._signpost = ''
        self._gram = ''
        # 单词解释
        self._def = ''
        # 额外的一些语法, 可选
        self._gram_exa: Exa = GramExa(src)
        # 额外的一些搭配, 可选
        self._collo_exa: Exa = ColloExa(src)


class Exa():
    """
    单词的额外信息
    """
    def __init__(self, src: BeautifulSoup) -> None:
        self._prop = ''
        self._examples: List[Example] = []


class GramExa(Exa):
    """
    单词额外的语法信息
    """
    def __init__(self, src: BeautifulSoup) -> None:
        # prop通常是Gram中的第一个span标签
        # 由于暂时只知道PROPFORM和PROPFORMPREP所以使用第一个span进行匹配
        super().__init__(src)


class ColloExa(Exa):
    """
    单词额外的搭配信息
    """
    def __init__(self, src: BeautifulSoup) -> None:
        super().__init__(src)


class Example():
    """
    单词解释的例子(通常是一个句子), 包含:
        1. 句子
        2. 句子发音
    """
    def __init__(self, src: BeautifulSoup):
        self._speaker_file = ''
        self._sentence = ''

