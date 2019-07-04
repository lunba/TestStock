import os
with open("d:/teststock/stockpools.txt",'r') as file_to_read:
    while True:
        lines = file_to_read.readline()
        if not lines:
           break
        else:
           ts_code,name = lines.split()
           print(ts_code)
           print(name)
           print(os.path.abspath(__file__))