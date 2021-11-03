from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from typing import Union


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

class Writer():
    f = None
    sense_num = 1

def to_str(el):
    return str(el) if el is not None else ''


def inner_str(tag: Union[Tag, NavigableString, None], recursive: bool = True) -> str:
    if tag is None:
        return ''
    elif isinstance(tag, NavigableString):
        return tag.string
    
    stream = tag.descendants if recursive else tag.children
    return "".join(i.string for i in stream if isinstance(i, NavigableString)).strip()


class Dictionary():
    def __init__(self, src: str):
        with open('./1.txt', 'w') as fl:
            Writer.f = fl
            soup = BeautifulSoup(src)
            if soup.find(class_ ='dictionary') is None:
                print('no dictionary element')
                return
            # 单词解释实体, 可能有多个意义
            self.dictEntry = [DictEntry(to_str(i)) for i in soup.find_all(class_ = 'dictentry')]
            # 单词起源
            self.etym = [Etym(to_str(i)) for i in soup.findAll(class_ = 'etym')]
            Writer.f.flush()
            Writer.f.close()



class DictEntry():
    """
    字典实体类, 包含了字典介绍及实体.
    通常一个词性对应一个实体, 例如一个词既有名词属性又有动词属性, 则可能有两个DictEntry
    """

    def __init__(self, src: str):
        Writer.f.write('\n\n-> dictentry\n')
        Writer.sense_num = 1
        soup = BeautifulSoup(src)
        # 词典介绍, 例如: From Longman Dictionary of Contemporary English
        self.dictionary_intro = soup.find(class_ = 'dictionary_intro')
        # 实体, 包含了具体的单词解释
        self.entry: Entry = Entry(to_str(soup.find(class_ = 'Entry')))


class Etym():
    """
    单词起源
    """

    def __init__(self, src: str):
        Writer.f.write('\n\n-> footer\n')
        soup = BeautifulSoup(src)
        self.asset_intro = soup.find(class_ = 'asset_intro')
        self.head = Head(to_str(soup.find(class_ = 'Head')))


class Entry():
    """
    DictEntry中的实体, 单词解释信息, 主要包含Head与Sense, 暂时已知以下两类:
        1. IdoceEntry
        2. BussDictEntry
    """

    def __init__(self, src: str):
        soup = BeautifulSoup(src)
        self.head: Head = Head(to_str(soup.find(class_ = 'Head')))
        # 可能包含多个Sense
        self.sense: List[Sense] = [Sense(to_str(i)) for i in soup.find_all(class_ = 'Sense')]



class IdoceEntry(Entry):
    """
    朗文当代英语
    """

    def __init__(self, src: str):
        super().__init__(src)


class BussDictEntry(Entry):
    """
    朗文商业英语
    """

    def __init__(self, src: str):
        super().__init__(src)


class Head():
    """
    单词的主要信息, 包含音标, 发音, 词性等
    """

    def __init__(self, src: str):
        soup = BeautifulSoup(src)
        # header word
        self.hwd = soup.find(class_ = 'HWD')
        # 连字符
        self.hyphenation = soup.find(class_ = 'HYPHENATION')
        # 上标
        self.homnum = soup.find(class_ = 'HOMNUM')
        # 音标
        self.pron_codes = soup.find(class_ = 'PronCodes')
        # 单词等级
        self.tooltip_levle = soup.find(class_ = 'tooltip LEVEL')
        # TODO 单词频率, 采用缩写方式, 此频率是朗文分级, 具体分级???
        self.freq = soup.find_all(class_ = 'FREQ')
        self.ac = soup.find(class_ = 'AC')
        # 词性
        self.pos = soup.find(class_ = 'POS')

        # 发音
        speakers = soup.find_all(class_ = 'speaker')
        if len(speakers) == 1:
            # 英音发音地址
            self.brefile = speakers[0].get('data-src-mp3')
        elif len(speakers) == 2:
            # 美音发音地址
            self.brefile = speakers[0].get('data-src-mp3')
            self.amefile = speakers[1].get('data-src-mp3')
        
        # 词性具体类型(有些head中可能不存在, Sense中也存在该属性), 例如: 名词的可数与不可数, 动词的及物与不及物
        self.gram = inner_str(soup.find(class_ = 'GRAM'))


class Sense():
    """
    单词的每个具体解释(一个单词通常有多个解释)
    """

    def __init__(self, src: str) -> None:
        soup = BeautifulSoup(src).find(class_ = 'Sense') 
        isSub = False
        if not soup:
            soup = BeautifulSoup(src).find(class_ = 'Subsense') 
            isSub = True
        if not soup:
            return
        # 单词解释序号, 可选
        self.sense_num = soup.find(class_ = 'sensenum')
        Writer.f.write(f'{" " if isSub else ""}{inner_str(self.sense_num)}. sense\n')
        self.signpost = soup.find(class_ = 'SIGNPOST')
        # 词性, 例如: 可数不可数
        self.gram = soup.find(class_ = 'GRAM')
        # 单词解释
        self.definition = soup.find(class_ = 'DEF')
        # 例子, 可选
        self.examples: List[Example] = [Example(to_str(i)) for i in soup.find_all(class_ = 'EXAMPLE', recursive=False)]
        # 额外的一些语法, 可选
        self.gram_exa: List[Exa] = [GramExa(to_str(i)) for i in soup.find_all(class_ = 'GramExa', recursive=False)]
        # 额外的一些搭配, 可选
        self.collo_exa: List[Exa] = [ColloExa(to_str(i)) for i in soup.find_all(class_ = 'ColloExa', recursive=False)]


        # 这里造成了无限递归, 子例子, 可选
        sub_senses = soup.find_all(class_ = 'Subsense', recursive=False)
        print(sub_senses)
        print('------')
        if sub_senses:
            self.sub_sense: List[Sense] = [Sense(to_str(i)) for i in sub_senses]



class Exa():
    """
    单词的额外信息
    """

    def __init__(self, src: str) -> None:
        soup = BeautifulSoup(src)
        self.prop = soup.find('span')
        self.examples: List[Example] = [Example(to_str(i)) for i in soup.find_all(class_ = 'EXAMPLE')]



class GramExa(Exa):
    """
    单词额外的语法信息
    """

    def __init__(self, src: str) -> None:
        # prop通常是Gram中的第一个span标签
        # 由于暂时只知道PROPFORM和PROPFORMPREP所以使用第一个span进行匹配
        Writer.f.write('    -> gram exa\n')
        super().__init__(src)


class ColloExa(Exa):
    """
    单词额外的搭配信息
    """

    def __init__(self, src: str) -> None:
        Writer.f.write('    -> collo exa\n')
        super().__init__(src)


class Example():
    """
    单词解释的例子(通常是一个句子), 包含:
        1. 句子
        2. 句子发音
    """

    def __init__(self, src: str):
        Writer.f.write('      ~ ex  ')
        soup = BeautifulSoup(src)
        speaker = soup.find(class_ = 'speaker')
        if isinstance(speaker, Tag):
            self.speaker_file = speaker.get('data-src-mp3')
        stc = soup.find(class_ = 'EXAMPLE')
        if isinstance(stc, Tag):
            self.sentence: str = inner_str(stc, recursive=True)
        Writer.f.write(f'{self.sentence}\n')
