import os
import sys
import pprint

students = {}
_file_num = len(sys.argv)
for x in range(1, _file_num):
  print('Scanning file' + sys.argv[x])
  f = open(sys.argv[x], 'r')
  for line in f:
    if not line.isspace():
      res = line.split(" ")
      _id = res[0]
      _grade = res[1]
      _grade = _grade.rstrip('\n')
      # print(_id + " " + _grade)

      # if the student already in the map
      if _id in students:
        arr = students.get(_id)
        arr.append(_grade)
      # create a new entry for that id
      else:
        students[_id] = [_grade]
  # pprint.pprint(students)

print('final result')
pprint.pprint(students)