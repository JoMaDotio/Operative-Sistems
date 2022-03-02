from asyncore import read
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


def capture_process(value, to, cont_p):
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
        cont_p += 1
        value -= 1
        tmp = Proceso(tms, id, operador, num1, num2)
        tmp.do_operation()
        to.append(tmp)
        os.system("cls")
        id_control += 1
    return


def handle_keyboard_event(flag, flag_endless):

    if flag_endless:
        return flag
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


def update_bloked(block, ready_arg):
    if len(block) == 0:
        return
    for i in range(len(block)):
        block[i].blocked_time += 1
        if block[i].blocked_time == 8:
            block[i].blocked_time = 0
            ready_arg.append(block.pop(i))
            return True
    return False


def main():

    endless_process = Proceso(100, "Proceso nulo", "+", 1, 1)
    endless_flag = False

    news = []
    done = []
    ready = []
    bloked = []
    in_execution = []
    global_counter = 0
    cont_process = 0
    num_procesos = int(input("Cuantos procesos quieres: "))
    capture_process(num_procesos, news, cont_process)
    flag = "c"
    flag_done = False
    update = False
    cont_ready = len(ready)
    cont_blocked = len(bloked)
    cont_inexecution = len(in_execution)
    on_memory = cont_ready + cont_inexecution + cont_blocked
    while(not flag_done):
        cont_ready = len(ready)
        cont_blocked = len(bloked)
        cont_inexecution = len(in_execution)
        on_memory = cont_ready + cont_inexecution + cont_blocked

        while (on_memory < 5 and len(news) > 0):
            temp_update = news.pop(0)
            temp_update.come_time = global_counter
            print("----Aqui todo bien----", temp_update.come_time)
            ready.append(temp_update)
            on_memory += 1
            cont_ready += 1

        if on_memory > 0 and cont_ready != 0:
            if endless_flag:
                in_execution.pop()
                endless_flag = False
            tmp = ready.pop(0)
            tmp.response_time = global_counter - tmp.come_time
            in_execution.append(tmp)
        else:
            in_execution.append(endless_process)
            endless_flag = True
        time_left = in_execution[0].time
        time_on = 0
        if (in_execution[0].time_remainder != None):
            time_left = in_execution[0].time_remainder
            time_on = in_execution[0].time - in_execution[0].time_remainder
        while (time_on < time_left):
            if endless_flag and len(news) < 1 and on_memory < 1:
                endless_flag = False
                break
            if endless_flag and update:
                break
            flag = handle_keyboard_event(flag, endless_flag)
            if flag == "p":
                continue
            elif flag == "e":
                in_execution[0].result = "Error"
                in_execution[0].end_time = global_counter
                in_execution[0].execute_time = in_execution[0].time - time_on
                break
            elif flag == "i":
                in_execution[0].time_remainder = in_execution[0].time - time_on
                bloked.append(in_execution[0])
                in_execution.pop()
                break
            print(time_left, time_on)
            print("Contador global: " + str(global_counter))
            time_on += 1
            global_counter += 1
            update = update_bloked(bloked, ready)
            print("------------------procesos en listo----------")
            print("Id\tTMS\tTR")
            for p in ready:
                p.show_next()
            print("\n-------proceso en ejecucion--------")
            in_execution[0].show_info()
            print("Tiempo restante: " + str(time_left))
            print("Tiempo avanzado: " + str(time_on))
            print("\n----------Procesos bloquedos-----------")
            print("Id\tTR\tTB")
            for p in bloked:
                p.show_bloked()
            print("\n----------Procesos terminados----------")
            print("Id\tOperacion\tResultado")
            for pro in done:
                pro.show_end()
            sleep(0.1)
            if flag != "p":
                os.system("cls")

        if flag != "i" and not endless_flag:
            temp_t = in_execution[0]
            if in_execution[0].end_time == None:
                in_execution[0].end_time = global_counter
            if in_execution[0].execute_time == None:
                in_execution[0].execute_time = in_execution[0].time
            aux1 = temp_t.end_time
            aux3 = temp_t.come_time
            print("Bug: ", in_execution[0].come_time)
            #in_execution[0].return_time = aux1 - aux3
            aux2 = in_execution[0].return_time
            #in_execution[0].wait_time = aux2-in_execution[0].execute_time
            done.append(in_execution.pop(0))
        flag = "c"
        if endless_flag:
            continue
        if (len(news) == 0 and on_memory == 0):
            flag_done = True

    print("Contador global: " + str(global_counter))
    print("Id\tOperacion\tResultado\tTLL\tTS\tTR\tTRES\tTES\tTE")
    for pro in done:
        if pro.id == "Proceso nulo":
            continue
        pro.show_end_program()


main()
