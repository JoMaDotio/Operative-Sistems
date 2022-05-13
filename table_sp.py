from tkinter.tix import Select
import colorama
from numpy import true_divide
from colorama import *
import math


class Frame:
    def __init__(self):
        self._id = 0
        self.process_id = None
        self.status = None
        self.space_used = [None, None, None, None]

    def __init__(self, id, pro_id, status, size):
        self._id = id
        self.process_id = pro_id
        self.status = status
        self.space_used = [None, None, None, None]


class FramesPage:

    def __init__(self):
        self.MAX_SIZE = 200
        self.page = []
        self.free_space = self.MAX_SIZE - 15
        self.frame_size = 4
        self.num_frames = self.free_space // self.frame_size

        for i in range(50):
            tmp = Frame(i, None, None, self.frame_size)
            if (i <= 3):
                tmp.process_id = "S.O."
                tmp.status = "Running"
                for i in range(self.frame_size):
                    tmp.space_used[i] = tmp.process_id
            self.page.append(tmp)
            self.free_space -= 4

    def have_space(self, size):
        return self.num_frames >= math.ceil(size/4)

    def add_process(self, id, status, procc_size):
        if not self.have_space(procc_size):
            return False
        cont = 0
        frames_need = (math.ceil(procc_size/4))
        self.num_frames -= frames_need
        for i in range(50):
            if frames_need == 0:
                break
            if self.page[i].process_id == None:
                self.page[i].process_id = id
                self.page[i].status = status
                for j in range(self.frame_size):
                    if cont == procc_size:
                        break
                    self.page[i].space_used[j] = id
                    cont += 1
                frames_need -= 1

    def update_status(self, id, status):
        for i in range(50):
            if self.page[i].process_id == id:
                self.page[i].status = status

    def remove_frame(self, id):
        count = 0
        for i in range(50):
            if self.page[i].process_id == id:
                count += 1
                self.page[i].process_id = None
                self.page[i].status = None
                for j in range(self.frame_size):
                    self.page[i].space_used[j] = None
        self.num_frames += count
        self.free_space += count * 4

    def space_memory(self):
        return 50 - self.num_frames > 0

    def show_page(self):
        print(f"Id F | Id P | Status\t|segments")
        for i in range(50):
            if (self.page[i].process_id == "S.O."):
                print(
                    f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.BLUE + self.page[i].status}\t{self.page[i].space_used}")
            elif (self.page[i].status == "Ready"):
                print(
                    f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.GREEN + self.page[i].status}\t{self.page[i].space_used}")
            elif (self.page[i].status == "Exec"):
                print(
                    f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.YELLOW + self.page[i].status}\t{self.page[i].space_used}")
            elif (self.page[i].status == "Blocked"):
                print(
                    f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.MAGENTA + self.page[i].status}\t{self.page[i].space_used}")
            else:
                print(
                    f"{self.page[i]._id}\t{self.page[i].process_id}\t{self.page[i].status}\t{self.page[i].space_used}")

    # def __init__(self):
    #     self.MAX_SIZE = 200
    #     self.page = []
    #     self.free_space = self.MAX_SIZE - 15
    #     self.frame_size = 4
    #     self.num_frames = self.free_space // 4

    #     for i in range(self.MAX_SIZE):
    #         tmp = Frame(i, None, None, self.frame_size)
    #         if (i <= 15):
    #             tmp.process_id = "S.O."
    #             tmp.status = "Running"
    #         self.page.append(tmp)

    # def have_space(self, size):
    #     return self.free_space >= size

    # def add_process(self, id, status, procc_size):
    #     if not self.have_space(procc_size):
    #         return False
    #     cont = 0
    #     for i in range(15, self.MAX_SIZE):
    #         if (cont == procc_size):
    #             break
    #         if self.page[i].process_id == None:
    #             self.page[i].process_id = id
    #             self.page[i].status = status
    #             self.count_spaces()
    #             cont += 1

    # def update_status(self, id, status):
    #     for i in range(15, self.MAX_SIZE):
    #         if self.page[i].process_id == id:
    #             self.page[i].status = status

    # def remove_frame(self, id):
    #     for i in range(3, self.MAX_SIZE):
    #         if self.page[i].process_id == id:
    #             self.page[i].process_id = None
    #             self.page[i].status = None
    #             self.count_spaces()

    # def count_spaces(self):
    #     count = 0
    #     for f in self.page:
    #         if f.process_id == None:
    #             count += 1
    #     self.free_space = count

    # def show_page(self):
    #     print(f"Id F | Id P | Status")
    #     for i in range(self.MAX_SIZE):
    #         if (self.page[i].process_id == "S.O."):
    #             print(
    #                 f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.BLUE + self.page[i].status}")
    #         elif (self.page[i].status == "Ready"):
    #             print(
    #                 f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.GREEN + self.page[i].status}")
    #         elif (self.page[i].status == "Exec"):
    #             print(
    #                 f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.YELLOW + self.page[i].status}")
    #         elif (self.page[i].status == "Blocked"):
    #             print(
    #                 f"{self.page[i]._id}\t{self.page[i].process_id}\t{colorama.Fore.MAGENTA + self.page[i].status}")
    #         else:
    #             print(
    #                 f"{self.page[i]._id}\t{self.page[i].process_id}\t{self.page[i].status}")
