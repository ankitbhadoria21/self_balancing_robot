#!/usr/bin

import RPi.GPIO as GPIO
import smbus
import time
smb=smbus.SMBus(1)
addr=0x68
x_a=0;y_a=0;z_a=0;
x_g=0;y_g=0;z_g=0;
gyro_offset_x=0;gyro_offset_y=0;gyro_offset_z=0;
fifo_l=0
accel_offset_x=0;accel_offset_y=0;accel_offset_z=0;

def read_word_data_s(smb,addr,reg):
    	val=smb.read_word_data(addr,reg)
    	if val>32767:
        	return -1*(65535-val+1)
    	else:
        	return val

"""
MPU 6050 is in sleep, it is done to wake it up & clock selection
change bit 0 &1 for clock selection 0x00 select internal 8Mhz Oscillator
set bit 7 for resetting all the registers
set bit 6 to put device to sleep
set bit 3 to disable temperature sensor
"""
def init_power(smb,addr,mode=0x00):
        smb.write_byte_data(addr,0x6B,mode)

"""
sample rate=gyro o/p(8 khz when dlpf is disabled else 1 khz)/1+divider
"""
def change_sample_rate_divider(smb,addr,divider):
	smb.write_byte_data(addr,0x17,divider)

def accelerometer_read(smb,addr=0x68,sensitivity=16384):
	global x_a
	global y_a
	global z_a
        x_a=read_word_data_s(smb,addr,0x3B)/sensitivity
        y_a=read_word_data_s(smb,addr,0x3D)/sensitivity
        z_a=read_word_data_s(smb,addr,0x3F)/sensitivity

def gyro_read(smb,addr=0x68,sensi=131):
	global x_g
	global y_g
	global z_g
        x_g=read_word_data_s(smb,addr,0x43)/sensi
        y_g=read_word_data_s(smb,addr,0x45)/sensi
    	z_g=read_word_data_s(smb,addr,0x47)/sensi	

"""
change bits 3 & 4 to change config
bits 5 to 7 are for z,y,x accel. self test
0=2g+-
1=4g+-
2=8g+-
3=16g+-
"""
def change_sensi_accel(smb,addr,sensi):
	smb.write_byte_data(addr,0x1C,sensi)

"""
change bits 3 & 4 to change config
bits 5 to 7 are for z,y,x accel. self test
0 250 degree/s
1 500 degree/s
2 1000 degre/s
3 2000 degree/s
"""
def change_sensi_gyro(smb,addr,sensi):
	smb.write_byte_data(addr,0x1B,sensi)

"""
change bits 0 to 2 for resetting temp,acclerometer & gyro respectively

"""
def signal_path_reset(smb,addr,value):
        smb.write_byte_data(addr,0x68,value)

def print_accel_value():
	print("x_a y_a z_a",x_a,y_a,z_a)

def print_gyro_value():
	print("x_g y_g z_g",x_g,y_g,x_g)

def FIFO_data_length(smb,addr):
	fifo_l=read_word_data(smb,addr,0x72)

def who_am_i():
	addr=read_word_data_s(smb,addr,0x75)>>1

def caliberate(smb,addr):
	global accel_offset_x
	global accel_offset_y
	global accel_offset_z
	init_power(smb,addr)
	for i in range(150):
		accelerometer_read(smb,addr)
		accel_offset_x+=x_a
		accel_offset_y+=y_a
		accel_offset_z+=z_a
		time.sleep(.1)
	accel_offset_x/=100
	accel_offset_y/=100
	accel_offset_z/=100

caliberate(smb,addr)
