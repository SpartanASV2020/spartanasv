#retrieve signal data for each channel of receiver 

 

import serial 

import time 

import sys 

from time import sleep 

 

#Huy's note: similar to samfok's method 

#Huy's note: This function is used to allign the dataframe 

def align_serial(ser): 

    ser.read(1) 

    dt = 0.0 

    # wait for the next long delay between reads 

    dt_threshold = 0.005 # pick some threshold between 8.69us and 9.89ms 

    while dt < dt_threshold: 

        start = time.time() 

        ser.read() 

        dt = time.time()-start 

    # consume the rest of the packet 

    ser.read(15) 

    # should be aligned with protocol now 

 

#Huy's note: Config info according to  "Remote Receiver Interfacing" data manual 

MASK_CH_ID = 0b01111000 # 0x78 

SHIFT_CH_ID = 3 

MASK_SERVO_POS_HIGH = 0b00000111 # 0x07 

 

#Huy's note: Similar to samfok's method 

#Huy's note: Function to decode the 2 bytes dataframe 

def parse_channel_data(data): 

    ch_id = (data[0] & MASK_CH_ID) >> SHIFT_CH_ID 

    ch_data = ( 

        ((data[0] & MASK_SERVO_POS_HIGH) << 8) | data[1]) 

    ch_data = 988 + (ch_data >> 1) 

    return ch_id, ch_data 

 

#Huy's note: Modify this line to fit the DX8 receiver !? 

#Huy's note: Apparently you can reassign these channel on the controller 

print("Throttle     Aile    Elev      Rud") 

 

#Huy's note: Initialize the uart 

ser = serial.Serial( 

    port="/dev/serial0", baudrate=115200, 

    bytesize=serial.EIGHTBITS, 

    parity=serial.PARITY_NONE, 

    stopbits=serial.STOPBITS_ONE) 

N_CHAN = 16 

data = None 

servo_position = [0 for i in range(N_CHAN)] 

try: 

    align_serial(ser) 

    while True: 

#Huy's note: Read all 16 bytes as stated in data manual 

        data_buf = ser.read(16) 

        data = data_buf[2:] 

        ch_id, s_pos = parse_channel_data(data[4:8]) 

        for i in range(7): 

            ch_id, s_pos = parse_channel_data(data[2*i:2*i+2]) 

            servo_position[ch_id] = s_pos 

 

#Huy's note: Add this line to print out whole dataframe 

        sys.stdout.write("    {:4d}     {:4d}     {:4d}     {:4d}\r".format(*servo_position[:4])) 

        sys.stdout.flush() 

        ser.write(data_buf) 

 

except(KeyboardInterrupt, SystemExit): 

    ser.close() 

except(Exception) as ex: 

    print (ex) 

    ser.close() 