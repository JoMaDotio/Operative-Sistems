import random
import os
import msvcrt
from time import sleep
from turtle import up

from matplotlib.pyplot import flag
from proceso import *


class Process_Admin:
    def __init__(self):
        self.news = []
        self.done = []
        self.ready = []
        self.blocked = []
        self.in_execution = []

        self.global_counter = 0
        self.num_process = 0
        self.id_control = 1

        self.keyboard_flag = "c"
        self.flag_done = False
        self.update = False
        self.endless_flag = False

        self.endless_process = Proceso(10, "Proceso nulo", "+", 1, 1)

    def unique_id(self, id):
        for pro in self.news:
            if pro.id == id:
                return False
        return True

    def valid_time(self, value):
        return value > 0

    def valid_operation(self, num1, ope, num2):
        if ope == "/" or ope == "%":
            if num2 == 0:
                return False
        return True

    def capture_process(self, num_processs):
        operators = ["+", "-", "*", "/", "%"]
        cont = 0
        while(cont < num_processs):
            tms = random.randint(6, 16)
            while (not self.valid_time(tms)):
                tms = random.randint(6, 16)
                if (self.valid_time(tms)):
                    break
                continue
            id = self.id_control
            while (not self.unique_id(id)):
                id = self.id_control + 1
                if (self.unique_id(id)):
                    break
                continue
            num1 = random.randint(-100, 100)
            operador = operators[random.randint(0, 4)]
            num2 = random.randint(-100, 100)
            while (not self.valid_operation(num1, operador, num2)):
                print("Operacion invalida, vuelva a ingresar los valores")
                num1 = random.randint(-100, 100)
                operador = operators[random.randint(0, 4)]
                num2 = random.randint(-100, 100)
                if (self.valid_operation(num1, operador, num2)):
                    break
                continue
            cont += 1
            tmp = Proceso(tms, self.id_control, operador, num1, num2)
            tmp.do_operation()
            self.news.append(tmp)
            os.system("cls")
            self.id_control += 1
        self.num_process += num_processs
        if self.keyboard_flag == "n":
            self.keyboard_flag = "c"

    def handle_keyboard_event(self):

        if self.endless_flag:
            return self.keyboard_flag
        if msvcrt.kbhit():
            leter = msvcrt.getch().decode("ASCII")
            if self.keyboard_flag == "p":
                if leter != "c":
                    self.keyboard_flag = "p"
                else:
                    self.keyboard_flag = "c"
            elif leter == "p":
                self.keyboard_flag = "p"
                print("Programa en pausa")
            elif leter == "i":
                self.keyboard_flag = "i"
            elif leter == "e":
                self.keyboard_flag = "e"
            elif leter == "c":
                self.keyboard_flag = "c"
            elif leter == "n":
                self.keyboard_flag = "n"
        return self.keyboard_flag

    def update_bloked(self):
        if len(self.blocked) == 0:
            return
        for i in range(len(self.blocked)):
            self.blocked[i].blocked_time += 1
            if self.blocked[i].blocked_time == 8:
                self.blocked[i].blocked_time = 0
                self.ready.append(self.blocked.pop(i))
                return True
        return False

    def show_ready_queue(self):
        print("------------------procesos en listo----------")
        print("Id\tTMS\tTR")
        for p in self.ready:
            p.show_next()

    def show_in_execution(self, time_left, time_on):
        print("\n-------proceso en ejecucion--------")
        self.in_execution[0].show_info()
        print("Tiempo restante: " + str(time_left))
        print("Tiempo avanzado: " + str(time_on))

    def show_blocked_queue(self):
        print("\n----------Procesos bloquedos-----------")
        print("Id\tTR\tTB")
        for p in self.blocked:
            p.show_bloked()

    def show_ended_queue(self):
        print("\n----------Procesos terminados----------")
        print("Id\tOperacion\tResultado")
        for pro in self.done:
            pro.show_end()

    def administrator(self):
        num_pro = int(input("Cuantos procesos quieres: "))
        self.capture_process(num_pro)
        # cont_ready = len(self.ready)
        # cont_blocked = len(self.blocked)
        # cont_in_execution = len(self.in_execution)
        while (not self.flag_done):
            cont_ready = len(self.ready)
            cont_blocked = len(self.blocked)
            cont_in_execution = len(self.in_execution)
            on_memory = cont_ready + cont_blocked + cont_in_execution

            while (on_memory < 5 and len(self.news) > 0):
                temp_proc = self.news.pop(0)
                temp_proc.come_time = self.global_counter
                self.ready.append(temp_proc)
                on_memory += 1
                cont_ready += 1

            if on_memory > 0 and cont_ready != 0:
                if self.endless_flag:
                    self.in_execution.pop()
                    self.endless_flag = False

                temp_proc = self.ready.pop(0)
                if temp_proc.response_time == None:
                    temp_proc.response_time = self.global_counter - temp_proc.come_time
                self.in_execution.append(temp_proc)
            else:
                self.in_execution.append(self.endless_process)
                self.endless_flag = True

            time_left = self.in_execution[0].time
            time_on = 0
            if (self.in_execution[0].time_remainder != None):
                time_left = self.in_execution[0].time_remainder
                time_on = self.in_execution[0].time - \
                    self.in_execution[0].time_remainder
            while (time_on < time_left):
                if (self.endless_flag and (len(self.news) == 0) and on_memory <= 1):
                    self.endless_flag = False
                    self.flag_done = True
                    break
                if self.endless_flag and self.update:
                    break
                self.keyboard_flag = self.handle_keyboard_event()

                if self.keyboard_flag == "p":
                    continue
                elif self.keyboard_flag == "e":
                    self.in_execution[0].result = "Error"
                    self.in_execution[0].end_time = self.global_counter
                    self.in_execution[0].execute_time = time_on
                    break
                elif self.keyboard_flag == "i":
                    self.in_execution[0].time_remainder = self.in_execution[0].time - time_on
                    self.blocked.append(self.in_execution[0])
                    self.in_execution.pop()
                    break
                elif self.keyboard_flag == "n":
                    self.capture_process(1)
                    if on_memory < 5:
                        self.news[0].come_time = self.global_counter
                        self.ready.append(self.news.pop(0))
                        on_memory += 1

                print(f"Procesos en la cola de nuevos {len(self.news)}")
                print(f"Contador global: {self.global_counter}")
                time_on += 1
                self.global_counter += 1
                self.update = self.update_bloked()
                self.show_ready_queue()
                self.show_in_execution(time_left, time_on)
                self.show_blocked_queue()
                self.show_ended_queue()
                sleep(1)

                if self.keyboard_flag != "p":
                    os.system("cls")
            if self.flag_done:
                break

            if self.keyboard_flag != "i" and not self.endless_flag:
                if self.in_execution[0].end_time == None:
                    self.in_execution[0].end_time = self.global_counter
                if self.in_execution[0].execute_time == None:
                    self.in_execution[0].execute_time = self.in_execution[0].time
                self.done.append(self.in_execution.pop(0))
            self.keyboard_flag = "c"
            if self.endless_flag:
                continue

        print(f"Contador global: {self.global_counter}")
        print("Id\tOperacion\tResultado\tTLL\tTS\tTR\tTRES\tTES\tTE")
        for pro in self.done:
            if pro.id == "Proceso nulo":
                self.global_counter -= 10
            pro.show_end_program()
