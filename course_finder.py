#!/usr/bin/python
#course_finder.py
import cPickle
import re

DB_FILENAME = "db.txt"

QUIT_PROGRAM = "0"
ADD_COURSE = "1"
REMOVE_COURSE = "2"
GET_INFO = "3"
SHOW_TIMETABLE = "4"

def greet_user():
	'''Greets the user when they start up the application.'''
	print """
	--**************--
	*    ===========  *
	*   / ========/  *
	*  / /   _ ___   *
	* / /   /_  |    *
	* | |   \_  |    *
	* \ \            *
	*  \ ========\   *
	*   ==========   *
	--**************--
	Welcome to CoursET! Helping you choose your classes at U of T.
	"""

def show_options():
	'''Shows the user their options for using the program.'''

	print ADD_COURSE + ": Add a course to your timetable."
	print REMOVE_COURSE + ": Remove a course from your timetable."
	print GET_INFO + ": Get info on a course."
	print SHOW_TIMETABLE + ": Display your timetable."
	print QUIT_PROGRAM + ": Quit the program."

def get_choice(options):
	
	choice = str(raw_input("What do you want to do? "))
	while choice not in options:
		print "Invalid choice; your options are: "
		show_options()
		choice = str(raw_input("What do you want to do? ")
	
	return choice

def get_db():
	'''Gets the database of courses. Generates a new database if the database
	cannot be found.'''
	
	db = {}
	try:
		with open(DB_FILENAME, "r") as f:
			db = cPickle.load(f)
	except IOError, UnpicklingError:
		import make_course_db
		print "Couldn't load courses."
		print "Generating new course database..."
		db = make_course_db.make_course_db()
		with open(DB_FILENAME, "w") as f:
			cPickle.dump(db, f)
	
	return db
