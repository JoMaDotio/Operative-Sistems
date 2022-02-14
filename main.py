import msvcrt
from operator import le
import os
import random
from time import sleep
from proceso import *


def unique_id(procces, id):
    for pro in procces:
        if pro.id == id:
            return False
    return True


def valid_time(value):
    return value > 0


def valid_operation(num1, ope, num2):
    if ope == "/" or ope == "%":
        if num2 == 0:
            return False
    return True


def capture_process(value, to, cont_p, num_l):
    operators = ["+", "-", "*", "/", "%"]
    id_control = 1
    while(value > 0):
        tms = random.randint(6, 16)
        while (not valid_time(tms)):
            tms = random.randint(6, 16)
            if (valid_time(tms)):
                break
            continue
        id = id_control
        while (not unique_id(to, id)):
            id = id_control
            if (unique_id(to, id)):
                break
            continue
        num1 = random.randint(-100, 100)
        operador = operators[random.randint(0, 4)]
        num2 = random.randint(-100, 100)
        while (not valid_operation(num1, operador, num2)):
            print("Operacion invalida, vuelva a ingresar los valores")
            num1 = random.randint(-100, 100)
            operador = operators[random.randint(0, 4)]
            num2 = random.randint(-100, 100)
            if (valid_operation(num1, operador, num2)):
                break
            continue
        if cont_p % 5 == 0:
            num_l += 1
        cont_p += 1
        value -= 1
        tmp = Proceso(tms, id, operador, num1, num2)
        tmp.num_lote = num_l
        tmp.do_operation()
        to.append(tmp)
        os.system("cls")
        id_control += 1
    return num_l


def handle_keyboard_event(flag):
    if msvcrt.kbhit():
        leter = msvcrt.getch().decode("ASCII")

        if flag == "p":
            if leter != "c":
                flag = "p"
            else:
                flag = "c"
        elif leter == "p":
            flag = "p"
            print("Programa en pausa")
        elif leter == "i":
            flag = "i"
        elif leter == "e":
            flag = "e"
        elif leter == "c":
            flag = "c"
    return flag


def main():
    to_do = []
    in_execution = None
    done = []
    pack = []
    global_counter = 0
    num_lotes = 0
    cont_process = 0
    num_procesos = int(input("Cuantos procesos quieres: "))
    num_lotes = capture_process(num_procesos, to_do, cont_process, num_lotes)
    flag = "c"
    while(len(to_do) > 0):

        how_many_left = len(to_do)
        if (how_many_left > 5):
            for i in range(5):
                pack.append(to_do.pop(0))
        else:
            for i in range(how_many_left):
                pack.append(to_do.pop(0))
        num_lotes -= 1

        while(len(pack) > 0):
            in_execution = pack.pop(0)
            time_left = in_execution.time
            time_on = 0
            if (in_execution.time_remainder != None):
                time_left = in_execution.time_remainder
                time_on = in_execution.time - in_execution.time_remainder
            while(time_on != in_execution.time):
                flag = handle_keyboard_event(flag)
                if flag == "p":
                    continue
                elif flag == "e":
                    in_execution.result = "Error"
                    break
                elif flag == "i":
                    in_execution.time_remainder = in_execution.time - time_on
                    pack.append(in_execution)
                    break
                print("Lotes restantes: " + str(num_lotes))
                print("Contador global: " + str(global_counter))
                time_left -= 1
                time_on += 1
                global_counter += 1
                print("------------------procesos del lote----------")
                print("Id\tTMS")
                for p in pack:
                    p.show_next()
                print("\n-------proceso en ejecucion--------")
                in_execution.show_info()
                print("Tiempo restante: " + str(time_left))
                print("Tiempo avanzado: " + str(time_on))
                print("\n----------Procesos terminados----------")
                print("Id\tOperacion\tResultado\tNum Lote")
                for pro in done:
                    pro.show_end()
                sleep(1)
                if flag != "p":
                    os.system("cls")
            if flag != "i":
                done.append(in_execution)
            flag = "c"
    print("Contador global: " + str(global_counter))
    print("Id\tOperacion\tResultado\tNum Lote")
    for pro in done:
        pro.show_end()


main()
