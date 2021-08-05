class Check_security:
    def __init__(self, sec_id: str):
        self.__set_share_or_bond(sec_id)
        self.__set_board_id(sec_id)

    def __set_share_or_bond(self, sec_id):
        if 3 <= len(sec_id) <= 5:
            self.__share_or_bond = 'shares'
        elif len(sec_id) == 12:
            self.__share_or_bond = 'bonds'

    def __set_board_id(self, sec_id):
        if self.__share_or_bond == 'shares':
            if sec_id[:3] == 'VTB' and sec_id[3] != 'R':
                self.__board_id = 'TQTF'
            else:
                self.__board_id = 'TQBR'

        elif self.__share_or_bond == 'bonds':
            if sec_id[:2] == 'RU':
                self.__board_id = 'TQCB'
            elif sec_id[:2] == 'SU':
                self.__board_id = 'TQOB'

    def get_share_or_bond(self):
        return self.__share_or_bond

    def get_board_id(self):
        return self.__board_id
