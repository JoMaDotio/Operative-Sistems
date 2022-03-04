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


def capture_process(value, to):
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

    # Creamos el proceso que su propocito es entretener el procesador, a 10 seg, ya que si el bloqueo solo dura 8
    endless_process = Proceso(10, "Proceso nulo", "+", 1, 1)
    endless_flag = False

    # Where all process are stored
    news = []
    # Process that finish correctly or by error
    done = []
    # Queue of process ready on memory for execution
    ready = []
    # Queue of process that are bloked by interruption in memory
    bloked = []
    # Structure just for contain one process that its the procces will be on execution
    # I decide to use an array for been able to count the process insides, that of course, always goona be 1 or 0
    in_execution = []
    # Global counter to see the time on the program
    global_counter = 0
    # We capture how manny process want for the simulation
    num_procesos = int(input("Cuantos procesos quieres: "))
    capture_process(num_procesos, news)  # Create process ramdomly
    # flag for keyboard interruptions
    flag = "c"
    # Flag to indicate when the program ended
    flag_done = False

    # Flag to check if we change a process from bloked to readdy
    # the main reason of that, it's because the process that will
    # keep working the procesor meanwhile are process bloked
    # And cant enter any process to memory or there are no more process
    update = False

    # Calculate for first time how many process are in memory
    # initialy has to be 0, but for other reasons i had to doit here
    cont_ready = len(ready)
    cont_blocked = len(bloked)
    cont_inexecution = len(in_execution)
    # Add the numbers of process on each Queue
    on_memory = cont_ready + cont_inexecution + cont_blocked

    # Start the main execution of all the program
    while(not flag_done):  # If we have process on memory o to enter at memory, we continue
        # We calculate numbers or process again and each time
        cont_ready = len(ready)
        cont_blocked = len(bloked)
        cont_inexecution = len(in_execution)
        on_memory = cont_ready + cont_inexecution + cont_blocked

        # While we have space in memory and still existing process on start
        # We added to memory a process
        while (on_memory < 5 and len(news) > 0):
            # We take the first process from the queue to enter and save it temporaly
            temp_update = news.pop(0)
            temp_update.come_time = global_counter  # Set his comming time on memory
            ready.append(temp_update)  # We insert the process to readdy
            # Increse the counter of process in memory, the main rason of that are some validations
            # comming ahead
            on_memory += 1
            # Increse the counter of process readdy
            cont_ready += 1

        # We check if there is an process on memory and process in ready are different
        # of 0 (we have process in readdy)
        if on_memory > 0 and cont_ready != 0:
            # Check if the process to keep busy the procesor its, active
            if endless_flag:
                # In case of that, we move out off the procesor
                in_execution.pop()
                # Set his flag to flase
                endless_flag = False
            # We take of the first processo of the Queue of ready
            tmp = ready.pop(0)
            # Then set the response time
            if tmp.response_time == None:
                tmp.response_time = global_counter - tmp.come_time
            # and added to execution
            in_execution.append(tmp)
        else:
            # In case that there are process blocked or something like that
            # We send the endless process to the procesor to keeping him bussy
            in_execution.append(endless_process)
            # Set his flag to
            endless_flag = True
        # Obtaing the time left of the processo to execute
        time_left = in_execution[0].time
        # set up the time on for the process
        time_on = 0
        # In case that the process has been on the procesor
        if (in_execution[0].time_remainder != None):
            # change time left to the time remainder
            time_left = in_execution[0].time_remainder
            # Change time on to the difference of time from the process
            time_on = in_execution[0].time - in_execution[0].time_remainder
        # While time on is lower that time left
        while (time_on < time_left):
            # We need to check if there is running the endless process
            # And if we dont have any process to introduce at memory
            # and there are not any other process on memory
            # We need to finish the program
            if endless_flag and len(news) == 0 and on_memory == 1:
                endless_flag = False
                flag_done = True
                break
            # If we have the endless process running and we uptaded
            # from bloked process
            # We need to break the iteration
            if endless_flag and update:
                break
            # We handle the keaboar events
            flag = handle_keyboard_event(flag, endless_flag)
            # if we need to pause, just keep iterating
            if flag == "p":
                continue
            # If we raise an error, we set the result to "error"
            # the end time and the execution time, because it will not run anymore
            elif flag == "e":
                in_execution[0].result = "Error"
                in_execution[0].end_time = global_counter
                in_execution[0].execute_time = in_execution[0].time - time_on
                break
            # If we generate an iterruption, we set the time_remainder
            # Then added to Queue of bloked process and remove the process from execution
            elif flag == "i":
                in_execution[0].time_remainder = in_execution[0].time - time_on
                bloked.append(in_execution[0])
                in_execution.pop()
                break
            print("Procesos en cola de nuevos: " + str(len(news)))
            # Display the global counter
            print("Contador global: " + str(global_counter))
            # increment the time on of the process
            time_on += 1
            # increment the global time
            global_counter += 1
            # Update bloked process if there is any of them and return a Boolean
            update = update_bloked(bloked, ready)
            # We print the process on ready
            print("------------------procesos en listo----------")
            print("Id\tTMS\tTR")
            for p in ready:
                p.show_next()
            # We print the info of the process on execution
            print("\n-------proceso en ejecucion--------")
            in_execution[0].show_info()
            print("Tiempo restante: " + str(time_left))
            print("Tiempo avanzado: " + str(time_on))
            # We print the process that are blocked
            print("\n----------Procesos bloquedos-----------")
            print("Id\tTR\tTB")
            for p in bloked:
                p.show_bloked()
            # We print process finished, without times
            print("\n----------Procesos terminados----------")
            print("Id\tOperacion\tResultado")
            for pro in done:
                pro.show_end()
            # We sleep 0.1 second
            sleep(1)
            # If the flag of keyboar not is 'p', we clear the console
            if flag != "p":
                os.system("cls")
        # if flag is donde, break the loop
        if flag_done:
            break
        # if the flag for keyboard is diferent that I and negate endless flag
        if flag != "i" and not endless_flag:
            # Lo guardamos temporalmente, meaby i delete this or only use this
            temp_t = in_execution[0]
            # If not had end time, we set it to global counter
            # (This two conditional are for the process that not ended by error)
            if in_execution[0].end_time == None:
                in_execution[0].end_time = global_counter
            # if not had execute time, we adddes the normal time
            if in_execution[0].execute_time == None:
                in_execution[0].execute_time = in_execution[0].time
            #in_execution[0].return_time = aux1 - aux3
            #in_execution[0].wait_time = aux2-in_execution[0].execute_time
            # We added the process to ended process
            done.append(in_execution.pop(0))
        # We set the flag to "Continue(c)"
        flag = "c"
        # if endless flag repeat the iteration
        if endless_flag:
            continue

    # At the end print the global time, and al the times
    print("Contador global: " + str(global_counter))
    print("Id\tOperacion\tResultado\tTLL\tTS\tTR\tTRES\tTES\tTE")
    for pro in done:
        if pro.id == "Proceso nulo":
            continue
        pro.show_end_program()


main()
