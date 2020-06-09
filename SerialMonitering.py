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
data_count = 3

def ambient_send(amb, datalist):
    """ 
        Function  : Send data to the ambient.
        Arguments : Ambient class (Ambient), data to be sent (list)
        return    : None
    """
    # Define the dictionary type to be sent to ambient.
    # The dictionary type used depends on the number of data.
    # (The minimum is 1, the maximum is 4)
    cmd_list = ("{'d1':{0}}",
                "{'d1':{0}, 'd2':{1}}",
                """{{"d1":{}, "d2":{}, "d3":{}}}""",
                "{'d1':{0}, 'd2':{1}, 'd3':{2}, 'd4': {3}}")

    # Creating the data to be sent
    senddata = cmd_list[len(datalist)- 1].format(*datalist)
    senddata = ast.literal_eval(senddata)

    # for debug
    # print(senddata)

    # ambient send execute.
    res = amb.send(senddata)
    # send Response. (HTTP stat code)
    print("Send Response : ", res)

def plot_data(plt_data, ax, line_obj_list):
    """
        Function  : Set the drawing area of a graph.
        Arguments : Plotting Graph Data (list), Drawing Control (Matlabplot's Axes class), Drawing Line Graphs(Matlabplot's Line object)
        return    : None
    """
    # Call the line object and set the data.
    for cnt, line_obj in enumerate(line_obj_list):
        line_obj.set_data(range(max_data), plt_data[cnt])

    # The drawing area of y-axis is set
    # by referring to the maximum and minimum values of the list.
    if data_count == 1:
        ax.set_xlim(min(plt_data) - 5, max(plt_data) + 5)
    elif data_count == 2:
        ax[0].set_ylim(min(plt_data[0]) - 5, max(plt_data[0]) + 5)
        ax[1].set_ylim(min(plt_data[1]) - 5, max(plt_data[1]) + 5)
    elif data_count == 3:
        ax[0, 0].set_ylim(min(plt_data[0]) - 5, max(plt_data[0]) + 5)
        ax[0, 1].set_ylim(min(plt_data[1]) - 5, max(plt_data[1]) + 5)
        ax[1, 0].set_ylim(min(plt_data[2]) - 5, max(plt_data[2]) + 5)
    elif data_count == 4:
        ax[0, 0].set_ylim(min(plt_data[0]) - 5, max(plt_data[0]) + 5)
        ax[0, 1].set_ylim(min(plt_data[1]) - 5, max(plt_data[1]) + 5)
        ax[1, 0].set_ylim(min(plt_data[2]) - 5, max(plt_data[2]) + 5)
        ax[1, 1].set_ylim(min(plt_data[3]) - 5, max(plt_data[3]) + 5)
    # for plot.
    plt.pause(0.01)

def main(): 
    """ Main sequence """
    # setting ambient info.
    amb = ambient.Ambient(amb_ch, amb_key)
    # Setting Serial info.
    ser = serial.Serial(ser_port, ser_speed)
    # fill 0 data
    write_data = [[0.0] * max_data for i in range(data_count)]

    # Create a graph plotting environment that suits the number of data.
    # Store line objects in a list. (You could write better than that... Lack of skill.)
    line_obj_list = []
    if data_count == 1:
        _, ax = plt.subplots()
        buff, = ax.plot(write_data, range(max_data))
        line_obj_list.append(buff)
    elif data_count == 2:
        _, ax = plt.subplots(2, 1, sharex="col", sharey="row")
        buff, = ax[0].plot(range(max_data), write_data[0])
        line_obj_list.append(buff)
        buff, = ax[1].plot(range(max_data), write_data[1])
        line_obj_list.append(buff)
    elif data_count == 3:
        _, ax = plt.subplots(2, 2, sharex="col", sharey="row")
        buff, = ax[0, 0].plot(range(max_data), write_data[0])
        line_obj_list.append(buff)
        buff, = ax[0, 1].plot(range(max_data), write_data[1])
        line_obj_list.append(buff)
        buff, = ax[1, 0].plot(range(max_data), write_data[2])
        line_obj_list.append(buff)
    elif data_count == 4:
        _, ax = plt.subplots(2, 2, sharex="col", sharey="row")
        buff, = ax[0, 0].plot(range(max_data), write_data[0])
        line_obj_list.append(buff)
        buff, = ax[0, 1].plot(range(max_data), write_data[1])
        line_obj_list.append(buff)
        buff, = ax[1, 0].plot(range(max_data), write_data[2])
        line_obj_list.append(buff)
        buff, = ax[1, 1].plot(range(max_data), write_data[3])
        line_obj_list.append(buff)
    else:
        print("It's a value we don't expect.")
        sys.exit(1)

    # read Serial (Endless.)
    while True:
        # plot initalize
        plt.cla()
        # read serial data.
        line = ser.readline()
        # Read the data as a comma-separated list.
        readdata = line.decode("utf-8").strip().split(",")
        # for debug.
        print("read data :",readdata)

        # Update the list.
        newlist = []
        for cnt, data in enumerate(readdata):
            write_data[cnt].append(float(data))
        for buff_list in write_data:
            del buff_list[0]
            newlist.append(buff_list)
        write_data = newlist
        del newlist

        # Check the length of the list. 
        # if : (0 < length < 5) => ok, else : program exit.
        if not len(readdata) == data_count:
            print("I'm afraid we received some unexpected data...")
            print("list length : ", readdata.len())
            print("The length of the expected list. expect data :", data_count)
            sys.exit(1)

        plot_data(write_data, ax, line_obj_list)

        ambient_send(amb, readdata)


if __name__ == "__main__":
    print("We're ready! Start monitoring...")
    main()