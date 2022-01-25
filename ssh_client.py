import paramiko
import time
import yaml
import pprint
from threading import Thread

class Device:
    conn = ''
    responce = ''

    def __init__(self, ip, user, password, port=22):
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port

        self.connect()

    
    def connect(self):      
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(self.ip, username=self.user, password=self.password, port=self.port, timeout=3)
        time.sleep(1)
        # remote_conn_pre.connect("73.215.176.112", username = "nkobaidze", password = "nikakobaidze1", port=4010, look_for_keys = False, allow_agent = False)# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


    def command(self, command_list, save_csv=False):
        for command in command_list:
            print(">> {}".format(command))
            self.connect()

            stdin, stdout, stderr = self.conn.exec_command("{}\n".format(command))
            time.sleep(.5)

             # FOR CSV 
            self.responce = stdout.readlines()
            # print(self.responce)
            
            print( ''.join(stdout) )

            if save_csv:
                self.get_csv()
        


    def get_csv(self):
        '''
        CSV FORMAT GENERATOR
        '''
        print(self.responce)

        for output in self.responce:
            output.replace(",", "")
            output.replace("\n","")
            output.replace("\r","")
            print("{},{}".format(self.ip, output))

    




if __name__ == "__main__":

    # print("\n==============================CISCO========================================\n")

    # cisco = Device("73.215.176.112", "nkobaidze", "nikakobaidze", 4009)
    
    # # COMMAND LIST
    # command_list = ["show ip int br"]
    # cisco.command(command_list, True)



    # print("\n==============================JUNIPER======================================\n")

    # juniper = Device("73.215.176.112", "nkobaidze", "nikakobaidze1", 4010)

    # # COMMAND LIST
    # command_list = ["show version", "show version"]
    # juniper.command(command_list)

    # print("\n================================END========================================\n")


    def get_device_by_name(data, device_name):
        for group in data:
            
            dev_list = data[group]
            for device in dev_list:
                # print(device)
                if device['device'] == device_name:
                    print(device)


    def get_groups(data):
        for group in data:
            print(group)


    def get_all_devs(data):
        for group in data:
            for device in data[group]:
                print("{} -- {}".format(device['device'], device['ip']))
    

    def get_group_devs(data, group_name):
        for group in data:
            if group == group_name:
                print(data[group])


    with open("devlist.yaml", 'r') as devs:
        parsed_yaml = yaml.safe_load(devs)



    # print("--------------------------------------------------")
    # print("PRINT ALL GROUPS")
    # print("--------------------------------------------------")
    # get_groups(parsed_yaml)
    # print()
    
    # print("--------------------------------------------------")
    # print("GET DEVICE DATA BY NAME")
    # print("--------------------------------------------------")
    # get_device_by_name(parsed_yaml, 'cisco801')
    # print("--------------------------------------------------")
    # print()

    # print("--------------------------------------------------")
    # print("GET GROUP DEVICES")
    # print("--------------------------------------------------")
    # get_group_devs(parsed_yaml, "juniper")


    print("===================================================")
    print(">> SELECT OPTION ")
    print("1. select category")
    print("2. select device")
    print("===================================================")
    
    start_option = int(input("Enter value: "))

    if start_option == 1:
        get_groups(parsed_yaml)
        group = input("Enter Group Name: ")

        get_group_devs(parsed_yaml, group)

        
    elif start_option == 2:
        get_all_devs(parsed_yaml)
        device = input("Enter device name: ")

        get_device_by_name(parsed_yaml, device)

    print("===================================================")
    print(">> ACTION ")
    print("1. Run Command")
    print("2. Make Backup")
    print("===================================================")

    action_option = int(input("Enter value: "))


    if action_option == 1:
        command = ''
        print("print exit to exit command mode")
        while command != 'exit':
            command = input("command >> ")
            print(command)
            print('....command output...')
    
    if action_option == 2:
        print("GET GROUP OR DEVICE")
        print("Run Backup action")
    
    

   
    
    

    

    
    
