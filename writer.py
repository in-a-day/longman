from engine import Engine
from longman_model import Dictionary
from longman_model import to_str, inner_str

class Writer():
    f = None

    def __init__(self, src):
        Engine(src)

    def write(self):
        raise Exception('not support writer')

class PyPrinter(Writer):
    def __init__(self, src):
        self._src = src

    def write(self):
        pass

class ConsoleWriter(Writer):
    def __init__(self, src):
        self._src = src

    def write(self):
        dc = Dictionary(self._src)
        # 首先打印出单词
        # 打印出词典类型
        for de in dc.dictEntry:
            # pring diction type
            if de.dictionary_intro:
                print(f'\n{de.dictionary_intro.string}')

            # print entry head
            head = de.entry.head
            head_str = inner_str(head.hyphenation) + \
                inner_str(head.homnum) + \
                inner_str(head.pron_codes) + \
                inner_str(head.tooltip_levle) + \
                inner_str(head.pos)
            print(head_str)

            # print meanning
            for sense in de.entry.sense:
                pass




        
        
        pass


class AnkiWriter(Writer):
    def write(self):
        pass
