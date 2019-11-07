class CTile:
    """
    block je list s výčtem výšek, které nelze projít. 0=zem, 1=výchozí hladina pro pohyb
    """
    def __init__(self, char, block=[0]):
        self.char = char
        self.block = block
