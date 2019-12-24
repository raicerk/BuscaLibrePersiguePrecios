class formato():
    valor = ""
    def __init__(self, valor):
        self.valor = valor
    def __format__(self, frmt):
        if (frmt == "miles"):
            return "{:,}".format(int(self.valor)).replace(",",".")