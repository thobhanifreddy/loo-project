from flask import Flask, render_template

import mraa 
import time

from datetime import datetime
import random


IR_GPIO = 0               # The ir GPIO   pinout ->"D6"

ir = mraa.Gpio(IR_GPIO)   # Get the ir pin object
ir.dir(mraa.DIR_IN)           # Set the direction as input

app = Flask(__name__)

time = 0
flag = 0

end_time = 0
start_time = 0

quotes = ["How long a minute is depends on which side of the bathroom door you are!", 
		"Do not RUSH, remember to FLUSH!", 
		"What happens in the bathroom remains in the bathroom",
		"Don't WORRY. \n Don't HURRY.\n Do your BEST.\n And FLUSH \n the REST",
		"Boys aim well to keep bathroom clean!",
		"Hope everything comes out!"
		]

@app.route('/status')
def loo():

	
	global end_time, start_time, flag, quotes
	state = ir.read()

	quote = random.choice(quotes)

	if flag == 0 and state == 0:					#flag = 0 and red
		start_time = datetime.now()
		flag = 1

	if flag == 1 and state == 1:					#flag = 1 and green 
		end_time = datetime.now()
		
		if end_time != 0 and start_time != 0:
			global time 
			time += (end_time - start_time).seconds
			flag = 0

	if state == 0:
		color = "red";
		status = "Not Available"
	
	if state == 1:
		color = "green"	
		status = "Available"	
		
	
	return render_template('loo.html', color = color, time = time, unit = unit, status = status, quote = quote) 

app.run(host='0.0.0.0', port= 8090)