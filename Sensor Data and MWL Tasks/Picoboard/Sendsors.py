import board
import time
from time import monotonic
from analogio import AnalogIn
from yui import Button
from ydata import SDcard, BSU, Ydt
import usb_cdc




#User Config |-----------------------------------
adjustable_rate = 1/400   # rate at which sensor data is sampled in hertz (
#DATA_RATE = 0.25         # data read rate in secs
#----------------------------------------------------

#Some variables
btn_1 = Button(pins = board.GP20)
GSR_Data = []
Answer = []
potentiometer_in3 = AnalogIn(board.A2)#potentiometer connected to A1, power & ground 
analog_in1 = AnalogIn(board.GP26) #measurement device input for first plot
analog_in2 = AnalogIn(board.GP27) #measurement device input for second plot
time_tag1 = time_tag2 = time_tag3 = time.monotonic()
dataset = []

btn_1.connect()

# check that USB CDC data has been enabled
if usb_cdc.data is None:
   print("Need to enable USB CDC serial data in boot.py.")
   while True:
       pass

# CSV output to send to PC
def send_csv_data(values):
    usb_cdc.data.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n".format(*values).encode())

def get_voltage(pin):
    return (((pin.value / 65535)*3.3))

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    current_time = time.monotonic()
    if current_time - time_tag1 >= adjustable_rate:
        GSR = get_voltage(analog_in2) #gets voltage from first sensor
        Answer.append(GSR)
        time_tag1 = current_time
    elif current_time - time_tag2 >= adjustable_rate: 
        EMG = get_voltage(analog_in1) #gets voltage from second sensor
        Answer.append(EMG)
        time_tag2 = current_time
    elif current_time - time_tag3 >= adjustable_rate: 
        mapped_value = map_value(get_voltage(potentiometer_in3), 0.01, 3.3, 1, 21)
        LIKERT_Rounded = round(mapped_value)
        LIKERT = LIKERT_Rounded #gets voltage from third sensor
        Answer.append(LIKERT)
        Answer.append(monotonic())
        time_tag3 = current_time
        dataset.append(Answer)
        
        if len(dataset) == 100: 
            usb_cdc.data.reset_output_buffer()
            send_csv_data(dataset)
            print('packet of 100 datpoints is sent')
            dataset = []
        Answer = []

    
