import re


class Erp:

    def __init__(self):
        pass

    def get_program(self, ba: str) -> str:
        regex = r'BA[0-9]{6}'
        if not re.search(regex, ba):  # value of ba might be a part number
            return ba

        return 'Nummer1'
