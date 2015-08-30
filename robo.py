#!usr/bin

import read_sensor_data
import pid_controller
import smbus
import math
import time
import RPi.GPIO as GPIO
from read_sensor_data import s_time as sample_time

pitch=0;roll=0
g_pitch_x=0;g_roll_y=0;
angle_x=0;angle_y=0;
weight_gyro=.98;weight_accel=.02;
angle_x_init=0

def calc_angle_accel(ax,ay,az):
	global pitch
	global roll
	if ax!=0 or ay!=0 or az!=0:
		pitch=math.degrees(math.acos(math.sqrt(ay*ay+az*az)/math.sqrt(ax*ax+ay*ay+az*az)))
		roll=math.degrees(math.acos(math.sqrt(ax*ax+az*az)/math.sqrt(ax*ax+az*az+ay*ay)))

def calc_angle_gyro(gx,gy,gz):
	global g_pitch_x
	global g_roll_y
	g_pitch_x=gx*sample_time
	g_roll_y=gy*sample_time

def complimentary_filter():
	global angle_x
	global angle_y
	read_sensor_data.accelerometer_read(read_sensor_data.smb,read_sensor_data.addr)
	read_sensor_data.gyro_read(read_sensor_data.smb,read_sensor_data.addr)
	calc_angle_accel(read_sensor_data.x_a,read_sensor_data.y_a,read_sensor_data.z_a)
	calc_angle_gyro(read_sensor_data.x_g,read_sensor_data.y_g,read_sensor_data.z_g)
	angle_x=weight_gyro*(g_pitch_x+angle_x)+weight_accel*pitch
	angle_y=weight_gyro*(g_roll_y+angle_y)+weight_accel*roll

def change_filter_values(gyro_v,accel_v):
	global weight_gyro
	global weight_accel
	weight_gyro=gyro_v
	weight_accel=accel_v

def init_angle():
	global angle_x_init
	read_sensor_data.caliberate(read_sensor_data.smb,read_sensor_data.addr)
	for i in range(300):
		complimentary_filter()
		angle_x_init+=angle_x
		time.sleep(sample_time)
	angle_x_init/=300

init_angle()
print(angle_x_init)
raw_input()
angle_x=0;angle_y=0
#main loop
while 1:
	complimentary_filter()
	#TODO: use PID controller to control motor
	print("x_angle final",angle_x,angle_x-angle_x_init)
	time.sleep(sample_time)
