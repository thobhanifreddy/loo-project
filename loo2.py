from flask import Flask, render_template
from flask-socketio import socketIO, send

import mraa 
import time

from datetime import datetime
import random

import serial


IR_GPIO = 0               # The ir GPIO   pinout ->"D7"

ir = mraa.Gpio(IR_GPIO)   # Get the ir pin object
ir.dir(mraa.DIR_IN)           # Set the direction as input

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = socketIO(app)

end_time = 0
start_time = 0

quotes = [
		"How long a minute is depends on which side of the bathroom door you are!", 
		"Do not RUSH, remember to FLUSH!", 
		"What happens in the bathroom remains in the bathroom",
		"Don't WORRY...Don't HURRY...Do your BEST...And FLUSH...the REST",
		"Boys aim well to keep bathroom clean!",
		"Hope everything comes out!",
		"Be a sweetie...Close the seatie !",
		"GENTLEMEN: Your aim will help...stand closer; it's shorter than you think.",
		"Reading Room - Appointment Needed!!",
		"It matters not how long u stay,just flush before you go away.",
		"If it is yellow, let it mellow. If it is brown flush it down.",
		"SHIT HAPPENS",
		"Ready...Aim...Fire",
		"Shit is about to go down!!",
		"You never know what you have until it's gone.",
		"Aim like a JEDI not like a STROMTROOPER",
		"Some goes to SIT and THINK...others just to SHIT and STINK",
		"Diapers were so much better...",
		"PLEASE...No selfies in the toilet",
		"Let it rain",
		"Don't leave without givng 100%",
		"Toilet camera is only for research use only",
		]

@socketio.on('status')
@app.route('/status')
def loo():

	
	global end_time, start_time, flag, quotes 
	
	state = ir.read()
	print(state)

	with serial.Serial("/dev/ttylS0", 57600, timeout = 1) as ser:
		timer = ser.readline()

	print(timer)
	timer = timer / 60
	quote = random.choice(quotes)


	if state == 0:
		color = "red";
		status = "Not Available"
	
	if state == 1:
		color = "green"	
		status = "Available"	
		
	
	return render_template('loo.html', color = color, status = status, quote = quote, timer = timer) 

if __name__ = 'main':
	socketio.run(app)
	# app.run(host='0.0.0.0', port= 8090)