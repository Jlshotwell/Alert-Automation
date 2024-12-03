import csv

organizations = []
customer_names = []

class device:
    def __init__(self, ninja_name= None):
        self.ninja_name = ninja_name
        self.disk_active = 0
        self.memory = 0
        self.storage = 0
    def memory_count(self):
        self.memory += 1
    def storage_count(self):
        self.storage += 1
    def report(self):
        print(self.ninja_name)
        print(f'Memory: {self.memory}')
        print(f'Storage: {self.storage}')
        print()
        

class organization:
    def __init__(self, devices= None, name= None):
        self.name = name
        self.devices = devices
    def system_filter(self, alert):
        for user in self.devices:
            if user.ninja_name in alert:
                if 'Memory Utilization' in alert:
                    user.memory_count()
                elif 'Disk Volume' in alert:
                    user.storage_count()
    def show_report(self):
        for user in self.devices:
            print(self.name)
            user.report()

def sort_csv(file):
    with open(file, 'r') as device_list:
        reader = csv.reader(device_list)
        for row in reader:
            if row[1] not in customer_names:
                customer_names.append(row[1])
        for c in customer_names:
            customer = organization(devices= [], name= c)
            organizations.append(customer)

def create_device_list(file):
    with open(file, 'r') as device_list:
        reader = csv.reader(device_list)
        for x in reader:
            for o in organizations:                
                if x[1] == o.name:
                    d = device(x[3])
                    o.devices.append(d)
            
            


