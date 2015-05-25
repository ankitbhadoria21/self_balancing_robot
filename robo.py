#!usr/bin
import read_sensor_data
import pid_controller
import math

pitch=0;roll=0
g_pitch_x=0;g_pitch_y=0;
sample_time=.01
angle_change_x=0;angle_change_y=0;
weight_gyro=.98;weight_accel=.02;

def calc_angle_accl(ax,ay,by):
	pitch=math.atan(ax,math.sqrt(ay*ay+az*az))
	roll=math.atan(ay,math.sqrt(ax*ax+az*az))

def calc_angle_gyro(gx,gy,gz,x_stable,y_stable):
	g_pitch_x=(gx-x_stable)*sample_time
	g_roll_y=(gy-y_stable)*sample_time


def complimentary_filter():
	angle_change_x=weight_gyro*g_pitch_x+weight_accel*pitch
	angle_change_y=weight_gyro*g_roll_y+weight_accel*roll

def change_filter_values(gyro_v,accel_v):
    weight_gyro=gyro_v
    weight_accel=accel_v

def balance():
	caliberate()
	accelerometer_read(smb,addr)
	gyro_read(smb,addr)
	calc_angle_accl(x_a,y_a,z_a)
    	calc_angle_gyro(x_g-gyro_offset_x,y_g-gyro_offset_y,z_g-gyro_offset_z)
	complimentary_filter()
	desired_angle=angle_chage_x
	# TODO: main loop to keep the robot balaced
		
