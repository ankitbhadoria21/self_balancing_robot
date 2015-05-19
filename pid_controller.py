#!/usr/bin

import time
import RPi.GPIO as GPIO

kp=0;ki=0;kd=0;
error_ttl=0;last_input=0;set_value=0;
last_time=0
sample_time=100
out_max=0;out_min=0;
pid_activate=1
direction=0

def set_Tunables(a,b,c):
	if kp<0 or kd<0 or ki<0:
		print("Wrong Values")
		return
	kp=a;ki=b*sample_time;kd=c/sample_time;
	if direction==1:
		kp=-1*kp
		ki=-1*ki
		kd=-1*kd
def intialize():
	last_input=input
	error_ttl=output
	if error_ttl<out_min: error_ttl=out_min
	elif error_ttl>out_max: error_ttl=out_max

def set_control_direction(val):
	direction=val	

def set_SampleTime(s_time):
	if s_time<=0:
		print("Wrong Values")
		return
	ratio=sample_time/s_time
	ki*=ratio
	kd/=ratio
	sample_time=s_time

def compute():
	if pid_activate==0:
		return
	curr_time=int(round(time.time()*1000))
	time_change=curr_time-last_time
	if time_change>=sample_time:
		error=set_value-input
		error_ttl+=ki*error
		if error_ttl>out_max:
			error_ttl=out_max
		elif error_ttl<out_min:
			error_ttl=out_min
		input_change=input-last_input;
		output=kp*error+error_ttl-kd*input_change;	
		if(output>out_max):
			output=out_max
		elif output<out_min:
			output=out_min
		last_input=input
		last_time=curr_time
"""
out_max and min should be the values accepted by PWM

"""

def out_limit(max,min):
	if(min>max):
		print ("wrong values")
		return
	out_max=max
	out_min=min
	if error_ttl>out_max:
		error_ttl=out_max
	elif error_ttl<out_max:
		error_ttl=out_min
	if output>out_max:
		output=out_max
	elif output<out_min:
		output=out_min
			
def set_PID_status(val):
	if pid_activate and val==0:
		intialize()
	pid_activate=val
