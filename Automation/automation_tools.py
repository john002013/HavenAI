from langchain.tools import Tool
from datetime import datetime
import time
import serial
port = '/dev/ttyACM0'
ser = serial.Serial(port, 9600, timeout=1)



def main(action: str):
    if action == "turn_on":
        ser.write(f"1\n".encode())
        time.sleep(2)
    elif action == "turn_off":
        ser.write(f"2\n".encode())
        time.sleep(2)

main_light = Tool(
    name = "main_light",
    func = main,
    description = "turns on the main light in the home automation system. Takes 'action' argument: 'turn_on' or 'turn_off'"
)


def lamp(action: str):
    if action == "turn_on":
        ser.write(f"3\n".encode())
        time.sleep(2)
    elif action == "turn_off":
        ser.write(f"4\n".encode())
        time.sleep(2)

control_lamp = Tool(
    name = "control_lamp",
    func = lamp,
    description = "turns on and turns off the control_light in the home automation system. Takes 'action' argument: 'turn_on' or 'turn_off'"
)


def fan(action: str):
    if action == "turn_on":
        ser.write(f"5\n".encode())
        time.sleep(2)
    elif action == "turn_off":
        ser.write(f"6\n".encode())
        time.sleep(2)

control_fan = Tool(
    name = "control_fan",
    func = fan,
    description = "turns on and turns off the fan in the home automation system. Takes 'action' argument: 'turn_on' or 'turn_off'"
)