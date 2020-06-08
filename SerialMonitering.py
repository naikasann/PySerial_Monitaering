import ast
import sys

import serial
import ambient
import numpy as np
import matplotlib.pyplot as plt

""" User Input. """
# ambient chanel
amb_ch = ""
# ambient key
amb_key = ""

# Serial port.
ser_port = ""
# Serial speed.
ser_speed = 115200

# plot data max size
max_data = 100
# data count(max : 4)
data_count = 4

def ambient_send(amb, datalist):
    """ 
        Send data to the ambient.
        Arguments : Ambient class (Ambient), data to be sent (list)
        return    : None
    """
    # Define the dictionary type to be sent to ambient.
    # The dictionary type used depends on the number of data.
    # (The minimum is 1, the maximum is 4)
    cmd_list = ("{'d1':{}}",
                "{'d1':{}, 'd2':{}}",
                "{'d1':{}, 'd2':{}, 'd3':{}}",
                "{'d1':{}, 'd2':{}, 'd3':{}, 'd4': {}}")

    # Creating the data to be sent
    senddata = cmd_list[datalist.len() - 1].format(datalist)
    senddata = ast.literal_eval(senddata)
    # for debug
    print(senddata)

    # ambient send execute.
    res = amb.send(senddata)
    # send Response. (HTTP stat code)
    print("Send Response : ", res)

def plot_data(plt_data, axe):
    data_count = plt_data.len()

    if data_count == 1:
        axe.plot(plt_data, range(max_data))
    elif data_count == 2:
        axe[0].plot(range(max_data), plt_data[0])
        axe[1].plot(range(max_data), plt_data[1])
    elif data_count == 3:
        axe[0, 0].plot(range(max_data), plt_data[0])
        axe[0, 1].plot(range(max_data), plt_data[1])
        axe[1, 0].plot(range(max_data), plt_data[2])
    elif data_count == 4:
        axe[0, 0].plot(range(max_data), plt_data[0])
        axe[0, 1].plot(range(max_data), plt_data[1])
        axe[1, 0].plot(range(max_data), plt_data[2])
        axe[1, 1].plot(range(max_data), plt_data[3])

    plt.draw()
    plt.pause(1)
    plt.cla()

def main(axe, write_data): 
    """ Main sequence """
    # setting ambient info.
    amb = ambient.Ambient(amb_ch, amb_key)
    # Setting Serial info.
    ser = serial.Serial(ser_port, ser_speed)

    # read Serial (Endless.)
    while True:
        # plot initalize
        plt.cla()
        # read serial data.
        line = ser.readline()
        # Read the data as a comma-separated list.
        readdata = line.decode("utf-8").split(",")
        # for debug.
        print(readdata)
        # Check the length of the list. 
        # if : (0 < length < 5) => ok, else : program exit.
        if not readdata.len() == data_count:
            print("I'm afraid we received some unexpected data...")
            print("list length : ", readdata.len())
            print("The length of the expected list. expect data :", data_count)
            sys.exit(1)

        ambient_send(amb, readdata)


if __name__ == "__main__":
    if data_count == 1:
        _, axe = plt.subplots()
    elif data_count == 2:
        _, axe = plt.subplots(2, 1, sharex="col", sharey="row")
    elif data_count == 3:
        _, axe = plt.subplots(2, 2, sharex="col", sharey="row")
    elif data_count == 4:
        _, axe = plt.subplots(2, 2, sharex="col", sharey="row")
    else:
        print("It's a value we don't expect.")
        sys.exit(1)
    """ Const value """
    write_data = [[0] * max_data for i in range(data_count)]
    main(axe, write_data)