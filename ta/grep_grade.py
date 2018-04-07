import os
import re
import sys

'''
Author:  Haotao Lai (Eric)
Contact: h_lai@encs.concordia.ca

This script is used for grep the grade from a directory where contains the assignment submited through EAS in ENCS department in Conconrdia University (Montreal).

The marker MUST used the "mark.txt" to give the grade and the grade must be put inside [].

A proper mark.txt should look like:

######################
1. feedback ....
2. feedback ....

[grade in number]
######################

'''

working_dir = "."
if len(sys.argv) is not 0:
	working_dir = sys.argv[1]
	print('Scanning directory: ' + working_dir)

counter = 0
for root, dirs, files in os.walk(working_dir, topdown=True):
	for name in files:
		if name == "mark.txt":
			counter += 1
			path = os.path.join(root, name)

			# open the mark.txt file and grep the grade
			mark_file = open(path, 'r')
			grade = "no_grade_or_demo"
			has_grade = False
			for line in mark_file:
				found_grade = re.match('(^\\[)[0-9a-z]*(\\]$)', line)
				if found_grade is not None:
					grade = found_grade
					has_grade = True

			# match the student id
			found = re.search(r'[0-9]{8}', path)
			if found is not None:
				if has_grade:
					print(found.group() + ' ' + grade.group()[1:-1])
				else:
					print(found.group() + ' ' + grade)

print("total number of assignment: " + str(counter))