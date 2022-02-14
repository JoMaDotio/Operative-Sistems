# hello
class Proceso:
    def __init__(self, name, time, id, ope, num1, num2):
        self.id = id
        self.name = name
        self.time = time
        self.result = None
        self.ope = ope
        self.num1 = num1
        self.num2 = num2
        self.num_lote = None

    def show_info(self):
        print("Id: " + str(self.id))
        print("Nombre: " + self.name)
        print("Operacion: " + str(self.num1) + self.ope + str(self.num2))
        print("TME: " + str(self.time))

    def show_next(self):
        print(f"{self.id}\t{self.time}")

    def show_end(self):
        print(
            f"{self.id}\t{str(self.num1) + self.ope + str(self.num2)}\t\t{self.result}\t\t{self.num_lote}")

    def do_operation(self):
        if self.ope == "/" or self.ope == "%":
            if self.num2 == 0:
                return False

        if self.ope == "+":
            self.result = self.num1 + self.num2
        elif self.ope == "-":
            self.result = self.num1 - self.num2
        elif self.ope == "*":
            self.result = self.num1 * self.num2
        elif self.ope == "/":
            self.result = self.num1 / self.num2
        elif self.ope == "%":
            self.result = self.num1 % self.num2
        else:
            return False

        return True
