import os
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
    while(value > 0):
        nombre = input("Nombre: ")
        tms = int(input("Tiempo estimado: "))
        while (not valid_time(tms)):
            print("Tiempo invalido, vuelva a intentarlo")
            tms = int(input("Tiempo estimado: "))
            if (valid_time(tms)):
                break
            continue
        id = int(input("Id de proceso: "))
        while (not unique_id(to, id)):
            print("Id ya en uso, ingrese otro.")
            id = int(input("Id de proceso: "))
            if (unique_id(to, id)):
                break
            continue
        num1 = int(input("Numero 1: "))
        operador = input("Operacion a realizar: ")
        num2 = int(input("Numero 2:"))
        while (not valid_operation(num1, operador, num2)):
            print("Operacion invalida, vuelva a ingresar los valores")
            num1 = int(input("Numero 1: "))
            operador = input("Operacion a realizar: ")
            num2 = int(input("Numero 2:"))
            if (valid_operation(num1, operador, num2)):
                break
            continue
        if cont_p % 5 == 0:
            num_l += 1
        cont_p += 1
        value -= 1
        tmp = Proceso(nombre, tms, id, operador, num1, num2)
        tmp.num_lote = num_l
        tmp.do_operation()
        to.append(tmp)
        os.system("cls")
    return num_l


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
            for i in range(in_execution.time):
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
                sleep(1.5)
                os.system("cls")
            done.append(in_execution)
    print("Contador global: " + str(global_counter))
    print("Id\tOperacion\tResultado\tNum Lote")
    for pro in done:
        pro.show_end()


main()
