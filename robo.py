#!usr/bin
import read_sensor_data
import pid_controller
import math

pitch_accl=0;roll=0,g_pitch_x=0,g_pitch_y=0;
sample_time=.01
def calc_angle_accl(ax,ay,by):
	pitch=math.atan(ax,math.sqrt(ay*ay+az*az))
	roll=math.atan(ay,math.sqrt(ax*ax+az*az))

def calc_angle_gyro(gx,gy,gz,x_stable,y_stable):
	g_ptch_x=(gx-x_stable)*sample_time
	g_roll_y=(gy-y_stable)*sample_time


def complimentary_filter(weight_gyro,weight_accel):
	angle_change_x=weight_gyro*g_pitch_x+weight_accel*pitch
	angle_change_y=weight_gyro*g_roll_y+weight_accel*roll
	
