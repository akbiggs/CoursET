#!/usr/bin/python
#make_course_db.py
#Writes info on all the courses to a text file.

from BeautifulSoup import BeautifulSoup
from course import Course
import os
import re

def make_course_db():
	'''Writes info on all courses to a text file.'''

	course_pagepath = os.getcwd() + '/course_pages/'
	#the course_db maps lists of class objects to their category names
	course_db = {}
	for course_page in os.listdir(course_pagepath):
		#open course listing, add course info to database
		print "Now adding courses from " + course_page
		with open(course_pagepath + course_page, 'r') as courses:
			add_courses(course_db, courses)
	
	print "Done!"
	return course_db

def add_courses(db, courses):
	'''Adds course objects to the db.

	pre: db is a dictionary, courses is an opened HTML page with
	course info.
	post: all classes from courses added to db.'''

	soup = BeautifulSoup(courses.read())
	table = soup.find("table")
	rows = table.findAll('tr')
	cur_course = None
	for row in rows:
		cols = row.findAll('td')
		course = cols[0].a
		if is_valid(course):
			add_course(db, course.string)
			cur_course = course.string
			add_course_info(db, cur_course, cols)	
			add_lecture(db, cur_course, cols)
		else:
			#if we've hit a class before in this table, assume this
			#row has another lecture for that class and add its info.
			if cur_course:
				add_lecture(db, cur_course, cols)

def add_course(db, course_name):
	'''Adds course to the db.

	pre: db is a dictionary, course_name is a valid course name string.'''
	
	course = Course(course_name)
	if course.category in db:
		db[course.category].append(course)
	else:
		db[course.category] = []
		db[course.category].append(course)

def add_course_info(db, course_name, cols):
	'''Adds info from cols about the course indicated by course_name to db.

	pre: db is a dictionary, course_name is the name of a course, row is an 
	HTML table row containing info about the course.
	post: info added to db.'''
	
	course = find_course(db, course_name)
	course.session = cols[1].font.string
	course.name = cols[2].font.string

def add_lecture(db, course_name, cols):
	'''Adds a lecture, tutorial or practical from cols to the course 
	indicated by course_name to db.

	pre: db is a dictionary, course_name is the name of a course, row is an
	HTML table.
	post: lecture from row added to course.'''

	course = find_course(db, course_name)

	#is the course canceled?
	if cols[4].font:
		if "Cancel" in [x.string for x in cols[4].findAll("font")]: return
	
	#grab the lecture name from the lecture column
	lecture_name = ""
	try:
		lecture_name = cols[3].font.string
	except AttributeError:
		#not there; possibly a blank space surrounded by <font>, so let's 
		#check on that instead.
		lecture_name = cols[3].font
 
	#if there's no text in the lecture column, assume we're updating
	#the previous lecture with another time
	if lecture_name == None:
		try:
			course.lectures[course.last_lecture_updated].append(
				cols[5].font.string)
		except KeyError:
			#Something's wrong with the lecture column formatting; skip it
			pass
	else:
		
		if lecture_name[0] == "L":
			course.lectures[lecture_name] = []
			course.lectures[lecture_name].append(cols[4].font.string
				if cols[4].font else None)
			course.lectures[lecture_name].append(cols[5].font.string)
		elif lecture_name[0] == "T":
			course.tutorials[lecture_name] = []
			course.tutorials[lecture_name].append(cols[4].font.string
				if cols[4].font else None)
			course.tutorials[lecture_name].append(cols[5].font.string)
		else:
			course.practicals[lecture_name] = []
			course.practicals[lecture_name].append(cols[4].font.string
				if cols[4].font else None)
			course.practicals[lecture_name].append(cols[5].font.string)
		course.last_lecture_updated = lecture_name

def find_course(db, course_name):
	'''Finds the course called course_name in the db.
	
	pre: db is a dictionary and course_name is the valid name of a course in 
	db.
	post: returns the course called course_name or None if no such course is
	found.'''
	
	category = course_name[0:3]
	for course in db[category]:
		if course.get_codename() == course_name:
			return course
	
	return None

def is_valid(course):
	'''Checks if the course is valid. Returns True if valid, false otherwise.

	Valid course name examples: MAT137Y1, csc240h1'''

	if course != None:
		if re.match("[a-z]{3}\d{3}[a-z]\d", course.string.lower()):
			return True
	
	return False

if __name__ == "__main__":
	make_course_db()
