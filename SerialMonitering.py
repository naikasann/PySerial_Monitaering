import serial
import ambient
import ast
import sys

""" User Input. """
# ambient chanel
amb_ch = ""
# ambient key
amb_key = ""

# Serial port.
ser_port = ""
# Serial speed.
ser_speed = 115200

""" Const value setting. """
# Define the dictionary type to be sent to ambient.
# The dictionary type used depends on the number of data.
# (The minimum is 1, the maximum is 4)
cmd_list = ("{'d1':{}}",
            "{'d1':{}, 'd2':{}}",
            "{'d1':{}, 'd2':{}, 'd3':{}}",
            "{'d1':{}, 'd2':{}, 'd3':{}, 'd4': {}}")

def main(): 
    """ Main sequence """
    # setting ambient info.
    amb = ambient.Ambient(amb_ch, amb_key)
    # Setting Serial info.
    ser = serial.Serial(ser_port, ser_speed)

    # read Serial (Endless.)
    while True:
        line = ser.readline()
        # Read the data as a comma-separated list.
        readdata = line.decode("utf-8").split(",")
        # for debug.
        print(readdata)
        # Check the length of the list. 
        # if : (0 < length < 5) => ok, else : program exit.
        if not 0 < readdata.len() < 5:
            print("I'm afraid we received some unexpected data...")
            print("list length : ", readdata.len())
            print("The length of the expected list. 0 < list < 5")
            sys.exit(1)



if __name__ == "__main__":
    main()