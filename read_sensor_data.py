#!/usr/bin

import RPi.GPIO as GPIO
import smbus
import time
smb=smbus.SMBus(1)
addr=0x68
x_a=0;y_a=0;z_a=0;
x_g=0;y_g=0;z_g=0;

def init(smb,addr):
        smb.write_byte_data(addr,0x6b,0x00)


def accelerometer_read(smb,addr,sensitivity):
        x_a=smb.read_byte_data(addr,0x3B)/sensitivity
        y_a=smb.read_byte_data(addr,0x3D)/sensitivity
        z_a=smb.read_byte_data(addr,0x3F)/sensitivity

def gyro_read(smb,addr,sensi):
        x_g=smb.read_byte_data(addr,0x43)/sensi
        y_g=smb.read_byte_data(addr,0x45)/sensi
	z_g=smb.read_byte_data(addr,0x47)/sensi	

def print_accel_value():
	print("x_a y_a z_a",x_a,y_a,z_a)

def print_gyro_value():
	print("x_g y_g z_g",x_g,y_g,x_g)

try:
	init(smb,addr)
	while 1:
		accelerometer_read(smb,addr,16348)
		print_accel_value()
		gyro_read(smb,addr,131)
		print_gyro_value()	
		time.sleep(.1)	
except KeyboardInterrupt:
	exit()
