from time import sleep
import requests
import threading

try:   

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    url = input("[?] URL: ")

    directory = input("[?] Directory [default]: ")
    if directory == "":
        directory = "directory/directory-list-2.3-medium.txt"

    error_code = input("[?] Error-Code [404]: ")
    if error_code == "":
        error_code = 404
    else:
        error_code = int(error_code)

    thread_number = input("[?] Number of Threads [10]: ")
    if thread_number == "":
        thread_number = 10
    else:
        thread_number = int(thread_number)

    start_line = input("[?] Start-Line in Directory [optional]: ")
    if start_line == "":
        start_line = 0
    else:
        start_line = int(start_line)

    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'

    def search_engine(start_line, tries, thread_number, sleep_time):
        with open(directory) as dir:
            i = 0
            d = 0
            line_counter = 0
            for agent in dir:

                if start_line <= line_counter and start_line + tries >= line_counter:
                    
                    agent.strip()
                    agent = agent.split("\n")[0]
                    user_agent = {'User-Agent': "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36"}
                    try:
                        response  = requests.get("{}{}".format(url, agent), headers = user_agent)
                        code = response.status_code
                        if code == error_code:
                            col = bcolors.WARNING
                            print(f"{bcolors.ENDC}[*] Directory-Try: {agent} - Thread {thread_number} - Code: {col}{response.status_code}")
                            print(LINE_UP,end=LINE_CLEAR)
                        elif code != error_code:
                            col = bcolors.OKGREEN
                            print(f"{bcolors.ENDC}[+] DIR-Match: No.{line_counter}: /{agent} - Code: {col}{response.status_code}")
                        
                        sleep(sleep_time)
                        line_counter += 1
                        i += 1
                    except Exception as f:
                        print("{}[!] Exception: {}".format(bcolors.FAIL, f))
                        d += 1
                        if d >= 3:
                            print(f"{bcolors.FAIL}[!] Too many errors, exiting...")
                            exit()

                elif start_line + tries < line_counter:
                    print(f"{bcolors.WARNING}[*] Thread {thread_number} finished.")
                    quit()
                else:
                    line_counter += 1
        dir.close()
    
    def line_counter(file_name):
        file = open(file_name, "r")
        line_count = 0
        for line in file:
            if line != "\n":
                line_count += 1
        file.close()
        return line_count
    
    len_lines = line_counter(directory)
    lines_per_thread = len_lines // thread_number

    for i in range(thread_number):
        if start_line == 0:
            starting_at = i*lines_per_thread
        else:
            len_lines = len_lines - start_line
            lines_per_thread = len_lines // thread_number
            starting_at = i*lines_per_thread + start_line

        x = threading.Thread(target=search_engine, args=(starting_at, lines_per_thread, i, i*0.1))
        print(f"{bcolors.OKCYAN}[*]Started Thread No." + str(i))
        x.start()


except KeyboardInterrupt:
    print(f"{bcolors.BOLD}{bcolors.WARNING}\n[*] Keyboard-Interrupt. Exiting...")