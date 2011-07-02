#!/bin/sh
wget -H -r --level=1 http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm
rm -rf "www.artsci.utoronto.ca"
mkdir course_pages/
cp www.artsandscience.utoronto.ca/ofr/timetable/winter/*.html course_pages/
rm -rf "www.artsandscience.utoronto.ca/" "course_pages/assem.html" "course_pages/sponsors.htm"



