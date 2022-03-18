class Proceso:
    def __init__(self, time, id, ope, num1, num2):
        self.id = id
        self.ope = ope
        self.num1 = num1
        self.num2 = num2
        self.result = None
        self.time = time
        self.time_remainder = None
        self.come_time = None
        self.end_time = None
        self.return_time = None
        self.execute_time = None
        self.response_time = None
        self.wait_time = None
        self.blocked_time = 0

    def calculate_times(self):
        self.return_time = self.end_time - self.come_time
        self.response_time = self.execute_time - self.come_time
        self.wait_time = self.return_time - (self.time - self.time_remainder)

    def show_info(self):
        print("Id: " + str(self.id))
        print("Operacion: " + str(self.num1) + self.ope + str(self.num2))
        print("TME: " + str(self.time))

    def show_next(self):
        print(f"{self.id}\t{self.time}\t{self.time_remainder}")

    def show_end(self):
        if self.result == "Error":
            rest = "Error"
        else:
            rest = f"{self.result:.2f}"
        print(
            f"{self.id}\t{str(self.num1) + self.ope + str(self.num2)}\t\t{rest}")

    def show_end_program(self):
        if self.result == "Error":
            rest = "Error"
        else:
            rest = f"{self.result:.2f}"
        print(f"{self.id}\t{str(self.num1) + self.ope + str(self.num2)}\t\t{rest}\t\t{self.come_time}\t{self.end_time}\t{self.end_time-self.come_time}\t{self.response_time}\t{(self.end_time-self.come_time)-self.execute_time}\t{self.execute_time}")

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

    def show_bloked(self):
        print(f"{self.id}\t{self.time-self.time_remainder}\t{self.blocked_time}")

    def show_operation(self):
        return f"{self.num1}{self.ope}{self.num2}"
