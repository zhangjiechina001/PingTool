import re


class CharValid:
    def valid(self, input: str) -> bool:
        pass


class FurnaceNumberValid(CharValid):
    def valid(self, input: str) -> bool:
        if len(input) == 1:
            # return input == 'Z'
            pattern = r"^[A-Z]$"
            return re.match(pattern, input)
        else:
            pattern = r"^\d{7}$"
            return re.match(pattern, input)


class IndexValid(CharValid):
    def valid(self, input: str) -> bool:
        pattern = r"^\d{3}$"
        return re.match(pattern, input)


class LengthValid(CharValid):
    def valid(self, input: str) -> bool:
        pattern = r"^[1-9][1-9]00$"
        if not re.match(pattern, input):
            return False

        index = int(input)
        return 5500 <= index <= 6800


class BrandValid(CharValid):
    def valid(self, input: str) -> bool:
        brands = ['20CrMoH']
        return input in brands
