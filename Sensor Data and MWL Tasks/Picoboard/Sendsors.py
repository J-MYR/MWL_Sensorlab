import board
import time
from time import monotonic
from analogio import AnalogIn
from yui import Button
from ydata import SDcard, BSU, Ydt
import usb_cdc
import busio
import sdcardio
import storage

#SD card stuff
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs = board.GP15
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')


#User Config |-----------------------------------
adjustable_rate = 1/400   # rate at which sensor data is sampled in hertz (
#DATA_RATE = 0.25         # data read rate in secs
#----------------------------------------------------

#Some variables
last_data = time.monotonic()
btn_1 = Button(pins = board.GP20)
EMG_Data = []
GSR_Data = []
LIKERT_Data = []
LIKERT = []
timestamp = []
Answer = []
potentiometer_in3 = AnalogIn(board.A2)#potentiometer connected to A1, power & ground 
analog_in1 = AnalogIn(board.GP26) #measurement device input for first plot
analog_in2 = AnalogIn(board.GP27) #measurement device input for second plot
time_tag1 = time_tag2 = time_tag3 = time.monotonic()
row_counter = 0
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

# def write_csv(Answer, filename="/sd/Results.csv"): 
#     csv_file = open(filename, "a") 
#     for row in range(0, len(Answer[0])):  
#         new_row = [Answer[0][row], Answer[1][row], Answer[2][row], Answer[3][row]]  
#         new_row_string = str(new_row[0]) + "\t" + str(new_row[1]) + "\t" + str(new_row[2]) + "\t" + str(new_row[3]) + "\n"
#         csv_file.write(new_row_string)
#     csv_file.close()

def get_voltage(pin):
    return (((pin.value / 65535)*3.3))

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

GSR = get_voltage(analog_in1) #gets voltage from first sensor
EMG = get_voltage(analog_in2) #gets voltage from second sensor
Likert = get_voltage(potentiometer_in3)

while True:
    current_time = time.monotonic()
    if current_time - time_tag1 >= adjustable_rate:
        GSR = get_voltage(analog_in2) #gets voltage from first sensor
#         print("\nSensor GSR:", GSR)
        GSR_Data.append(GSR)
        Answer.append(GSR)
        time_tag1 = current_time
    elif current_time - time_tag2 >= adjustable_rate: 
        EMG = get_voltage(analog_in1) #gets voltage from second sensor
#         print("Sensor EMG:", EMG)
        EMG_Data.append(EMG)
        Answer.append(EMG)
        time_tag2 = current_time
    elif current_time - time_tag3 >= adjustable_rate: 
        mapped_value = map_value(get_voltage(potentiometer_in3), 0.01, 3.3, 1, 21)
        LIKERT_Rounded = round(mapped_value)
        LIKERT = LIKERT_Rounded #gets voltage from third sensor
#         print("Sensor LIKERT:", LIKERT)
        LIKERT_Data.append(LIKERT)
        timestamp.append(time.time())
        Answer.append(LIKERT)
        Answer.append(time.time())
        time_tag3 = current_time
#       if row_counter >= 1: # only print once for every 200 rows
#             print("\nWriting data to CSV constantly, but only once in Thonny Plotter for every 500 rows:...")
#             print("Sensor GSR:", GSR)
#             print("Sensor EMG:", EMG)
#             print("Sensor LIKERT:", LIKERT)
#         if row_counter >= 1:
#             row_counter = 0
#         for row in range(0, len(Answer[0])):  
#             new_row = [Answer[0][row], Answer[1][row], Answer[2][row], Answer[3][row]]  
#             new_row_string = str(new_row[0]) + "\t" + str(new_row[1]) + "\t" + str(new_row[2]) + "\t" + str(new_row[3]) + "\n"
#         write_csv(Answer)
        dataset.append(Answer)
        
        
        if len(dataset) == 100: #and current_time - last_data > DATA_RATE
            usb_cdc.data.reset_output_buffer()
            print(len(dataset))
            send_csv_data(dataset)
            last_data = current_time
            print('packet of 100 datpoints is sent')
            dataset = []
            
        row_counter += 1
        EMG_Data = []
        GSR_Data = []
        LIKERT_Data = []
        timestamp = []
        Answer = []

#         if len(GSR_Data) % (DATA_RATE/adjustable_rate) == 0: # every 0.5 sec, write data to SD card and send over USB CDC
#             Answer = [timestamp, GSR_Data, EMG_Data, LIKERT_Data]
#             write_csv(Answer)
#             send_csv_data(Answer)
#             EMG_Data = []
#             GSR_Data = []
#             LIKERT_Data = []
#             timestamp = []
#             Answer = [timestamp, GSR_Data, EMG_Data, LIKERT_Data]
    

        
