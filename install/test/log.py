import time
 
timestamp = str(time.time()).split('.')[0]
with open("log.txt", "a") as f:
    f.write(f"{timestamp} INFO New Error\n")
