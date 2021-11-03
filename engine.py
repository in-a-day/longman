from longman_model import Dictionary
from bs4 import BeautifulSoup


class Engine():

    def __init__(self, src):
        pass

    def exec(self):
        with open('./range.html') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            Dictionary(str(soup))


if __name__ == '__main__':
    Engine('').exec()


