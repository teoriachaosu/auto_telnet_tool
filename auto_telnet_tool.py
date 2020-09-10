from telnetlib import Telnet
import time, os, re
from datetime import datetime

class AutoTelnet:
    def __init__(self, filename1, filename2, filename3):
        self.login_data = []
        self.new_settings = []
        self.filename1 = filename1
        self.filename2 = filename2
        self.filename3 = filename3

    def txt_to_arr(self, filename):
        arr = []
        file_dir = os.path.join(os.getcwd(), filename)
        with open(file_dir, 'r') as login:
            lines = login.readlines() # list of all lines from txt file
            for i in range(0, len(lines)):
                if lines[i] == '\n': # stop when empty line encountered
                    break
                if lines[i].find('///') == -1: # omit lines with description
                    arr.append(lines[i].rstrip()) # remove '\n' from every line (restored later on if needed)
        return arr

    def router_setup(self):
        log_dir = os.path.join(os.getcwd(), self.filename3)
        with open(log_dir, 'a') as log_file:
            print('Auto Telnet Tool by Maciej Bialowas')
            print('Session started:', datetime.now().strftime('%d-%m-%Y %X'))
            log_file.write('\n' + 'Session started: '+ datetime.now().strftime('%d-%m-%Y %X') + '\n')
            login_data = self.login_data # no need to type 'self.login_data' later on
            new_settings = self.new_settings

            # read router login and settings
            try:
                login_data = self.txt_to_arr(self.filename1)
                new_settings = self.txt_to_arr(self.filename2)
            except IOError as e:
                print('Error reading from file:', e)
                log_file.write('Error reading from file: ' + str(e) + '\n')
                os.system('pause')
                return # stop when 1st incorrect value found

            # check if valid values were provided where required
            try:
                match = re.search("^[1-9]{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$", login_data[0])
                if not match:
                    print('incorrect IP address:',login_data[0])
                    log_file.write('incorrect IP address: '+ login_data[0])
                    os.system('pause')
                    return
                int(login_data[1]) # port
                float(login_data[2]) # read timeout
            except ValueError as v:
                print("Invalid value in 'router_login.txt':", v)
                log_file.write("Invalid value in 'router_login.txt': " + str(v) + '\n')
                os.system('pause')
                return  # stop when 1st incorrect value found

            # telnetlib needs byte objects, string must be converted: encode(), or b'string
            # connect to router
            print('Connecting to router...')
            log_file.write('Connecting to router...' + '\n')
            try:
                conn = Telnet(login_data[0], int(login_data[1])) # connect: ip, port. Will wait until Windows timeout.
            except TimeoutError as t:
                print(t)
                log_file.write(str(t) + '\n')
                os.system('pause')
                return
            except ConnectionError as p:
                print(p)
                log_file.write(str(p) + '\n')
                os.system('pause')
                return
            # Log in
            print('Logging in...')
            log_file.write('Logging in...' + '\n')
            router_output = conn.read_until(login_data[6].encode('ASCII'), float(login_data[2]))  # read login prompt & login entered
            conn.write(login_data[3].encode('ASCII') + b'\n') # enter username, needs \n!; convert to byte obj and add new line char (as byte obj)
            print(router_output.decode('ascii'))
            log_file.write(router_output.decode('ascii'))

            router_output = conn.read_until(login_data[7].encode('ASCII'), float(login_data[2])) # read password prompt
            print(router_output.decode('ascii'))
            log_file.write(router_output.decode('ascii'))
            time.sleep(float(login_data[2]))  # read timeout, wait for response
            conn.write(login_data[4].encode('ASCII') + b'\n')  # enter password, needs \n!

            # check if router config prompt appeared = login was successful
            router_output = conn.read_until(login_data[5].encode('ASCII'), float(login_data[2]))  # encode rt_cfg_prompt, read timeout
            print(router_output.decode('ascii'))
            log_file.write(router_output.decode('ascii'))
            if (router_output.decode('ASCII')).find(login_data[5]) == -1:
                msg = 'Login error. Possible reasons: incorrect username, password, router config prompt or too short read timeout'
                print(msg)
                log_file.write('\n' + msg + '\n')
                conn.close() # must be closed even if login failed
                os.system('pause')
                return

            # apply settings
            for i in new_settings:
                conn.write(i.encode('ascii') + b'\n') # enter commands from txt file, needs \n
                router_output = conn.read_until(login_data[5].encode('ASCII'), float(login_data[2]))
                time.sleep(float(login_data[2])) # wait for router response (read timeout)
                print(router_output.decode('ascii'))
                log_file.write(router_output.decode('ascii'))
            conn.close()
            print('--End of session--')
            log_file.write('\n' + '--End of session--' + '\n')
            os.system('pause')


if __name__ == '__main__':
    configure_router = AutoTelnet('router_login.txt', 'router_setup.txt', 'session_log.txt')
    configure_router.router_setup()





