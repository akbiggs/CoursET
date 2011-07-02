#!/usr/bin/python
#course.py
#Represents a course at U of T.

import re

class InvalidNameException(Exception):
	pass

class Course(object):
	'''Represents a course at U of T.'''

	category = ''
	code = ''
	credit = ''
	session = ''
	name = ''
	lectures = {}
	practicals = {}
	tutorials = {}
	last_lecture_updated = ''

	def __init__(self, name):
		'''Makes a new course with the course name.'''
		try:		
			self.category, self.code, self.credit = self.read_codename(name)
		except InvalidNameException:
			print "Unable to make a course called " + name + "; are you " \
				"sure you spelled the course name correctly?"
	
	def read_codename(self, name):
		'''Returns a three-tuple of course category, code number and credit
		type based on supplied name. Raises an InvalidNameException if the
		given name is unacceptable.

		Example course names: MAT137Y1, CSC240H1, ANT100Y1'''
		
		#is the course name valid?
		if re.match("[a-z]{3}\d{3}[a-z]\d", name.lower()):
			category, code, credit = name[0:3], name[3:6], name[6:8]
			return (category, code, credit)
		else:
			raise InvalidNameException

	def get_codename(self):
		return self.category + self.code + self.credit

if __name__ == '__main__':
	course = Course("blah")
	print course.category, course.code, course.credit
