import random

from backend.services.bible_gen import BibleGen


class TextGenerator:

    def get_text(self):
        wc = BibleGen(random_value=self.get_random_odd())
        # wc = BibleGen(random_value=15256)
        result = wc.run()
        init = result.find('text=') + 5
        finish = result.find('pronunciation=')
        return result[init:finish]

    @staticmethod
    def get_random_odd():
        value = random.randint(11111, 99999)
        while value % 2:
            value = random.randint(101, 999)
        return value
