from proceso import *
from process_admin import *
from table_sp import *
from colorama import *


def main():
    colorama.init(autoreset=True)
    myAdmin = Process_Admin()
    myAdmin.administrator()


if __name__ == "__main__":
    main()
