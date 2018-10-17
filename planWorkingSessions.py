import sys
import readchar
from calendarAPI import find_overlapping_event, add_event
from helpers import add_to_hour, timerange_to_datetime

desc = '''
Since, as the Internet says, and he is always right, that the optimal working sessions
	are 52 minutes and then 17 minutes break, and it's annoying to recalculate
	each and every time the working sessions starting at time X,
	this script does this for us.

Stops at midnight.
'''

SESS_TIME = 52
REST_TIME = 17

def append_zero(t):
	return str(t) if len(str(t)) == 2 else '0' + str(t)

def format_hour(hour, minutes):
	return append_zero(hour) + ":" + append_zero(minutes)

def get_hour(r_a):
	if len(r_a) != 4:
		print "Error: error in reading the hour."
		exit(1)
	if [True for x in r_a if not x.isdigit()]:
		print "Error: input must be numeric."
		exit(1)
	r_a = map(lambda n: int(n), r_a)
	hours = r_a[0]*10 + r_a[1]
	if hours < 0 or hours > 23:
		print "Error: hours our of range 00-23"
		exit(1)
	minutes = r_a[2]*10 + r_a[3]
	if minutes < 0 or minutes > 59:
		print "Error: minutes our of range 00-59"
		exit(1)

	return (hours, minutes)

def read_start_hour():
	sys.stdout.write("Please insert the starting hour as HH:MM: ")
	read_arr = []
	read_arr.append(readchar.readchar())
	sys.stdout.write(read_arr[-1])
	read_arr.append(readchar.readchar())
	sys.stdout.write(read_arr[-1])
	sys.stdout.write(":")
	read_arr.append(readchar.readchar())
	sys.stdout.write(read_arr[-1])
	read_arr.append(readchar.readchar())
	sys.stdout.write(read_arr[-1])
	sys.stdout.write("\n")

	return get_hour(read_arr)

def handle_overlap(hour, minutes, overlap_event):
	'''
	Asks the user if he wants to skip this hour because of the overlap.
	Returns True/False.
	hour/minutes is the time of the original hour.
	'''
	end_hour, end_minutes = add_to_hour(hour, minutes, SESS_TIME)
	print "Overlap: the session " + format_hour(hour, minutes) + " - " + format_hour(end_hour, end_minutes) + \
			" overlaps with the event \"" + overlap_event["summary"] + "\"."
	ans = ""
	while ans.lower() not in ["y", "n"]:
		ans = raw_input("Would you like to skip setting this session? [Y/n]:")
		if not ans.strip():
			ans = "y"
	return ans == "y"


def handle_hour(hour, minutes):
	start_datetime, end_datetime = timerange_to_datetime(hour, minutes, SESS_TIME)

	overlap_event = find_overlapping_event((start_datetime, end_datetime))
	if overlap_event and handle_overlap(hour, minutes, overlap_event):
		return

	summary = raw_input("Summary of the event at " + format_hour(hour, minutes) + " - " + format_hour(end_datetime.hour, end_datetime.minute) + ": ").strip()
	if not summary.strip():
		print "(Skipped. Write \"Done\" for exit)"
		return
	elif summary.lower() == "done":
		print "Exit."
		exit(0)
	add_event((start_datetime, end_datetime), summary)

def main():
	print "Welcome to the session calculator!"
	print desc
	print "============================="

	hours, minutes = read_start_hour()

	while hours < 23 or minutes < 60-SESS_TIME:
		handle_hour(hours, minutes)

		hours, minutes = add_to_hour(hours, minutes, SESS_TIME + REST_TIME)


if __name__ == "__main__":
	main()
