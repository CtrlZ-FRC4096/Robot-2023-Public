import time
import socket
# import readline # just importing this modifies behavior
import ntcore
import uuid

local_ip = socket.gethostbyname(socket.gethostname())

remote_ip = '10.40.96.2' if '40.96' in local_ip else '127.0.0.1'

# logging.basicConfig(level=logging.DEBUG)

inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("Remote Shell DS" + str(uuid.uuid1()))
inst.setServer(remote_ip)

while not inst.isConnected():
    pass

print("---------------------------")
print("---------------------------")
if remote_ip == '127.0.0.1':
    print("Connected to SIMULATOR")
else:
    print("Connected to ROBOT")
print("---------------------------")
print("You are now in a pseudo python shell within the robot.")
print("Your robot is located at 'robot' or at 'r'.")
print("Ex. 'robot.oi' is the OI object of your robot.")
print("---------------------------")
print("---------------------------")

table = inst.getTable("Remote Shell")
stdout_sub = table.getStringTopic("stdout")

def r():
    user_input = input(">>> ")
    if user_input == "exit()":
        exit()
    user_input += f" T{time.time_ns():<20}"
    table.putString("stdin", user_input)
    # print("sent ->", user_input)

def pr(event: ntcore.Event):
    print(event.data.value.getString()[:-22]) # type: ignore
    r()

inst.addListener(stdout_sub, ntcore.EventFlags.kValueAll, pr)

r()

while True: pass
