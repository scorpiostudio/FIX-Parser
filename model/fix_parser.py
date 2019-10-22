import re
from fix_message import FIXMessage


class FIXParser(object):
    """

    """
    def __init__(self):
        self.pattern = re.compile('8=FIX.\d.\d[.|\^?,\x01]9=\d+[.|\^?,\x01]35=\w[.|\^?,\x01].+?10=\d\d\d[.|\^?,\x01]?')

    def parse_fix_message(self, fix_text):
        print fix_text
        messages = self._split_fix_text(fix_text)
        lines = list()
        for raw_message in messages:
            fix_message = FIXMessage(raw_message).parse()
            lines.append(fix_message)

        return lines

    def _split_fix_text(self, fix_text):
        lines = list()
        text = fix_text
        if text is None:
            return lines
        while True:
            match = self.pattern.search(text)
            print match
            if match is None:
                break
            index = match.span()[1]
            lines.append(text[0:index])
            text = text[index:]
        return lines


if __name__ == '__main__':
    parser = FIXParser()
    filter_list = []
    lines = parser.parse_fix_message(FIX_MESSAGE, filter_list)
    print lines

