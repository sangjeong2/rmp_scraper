'''

 ## RateMyProfessor Scraper 2014
 ## Created for SI365 by Sang-Jung Han (hansj@umich.edu)
 ## Copyleft

 '''

from __future__ import print_function
import urllib2
import json
import csv
import re


## Step 1: Getting IDs of all professors

univ_name = "University of Michigan" ## Replace this with whatever university you want (ex. University of California Los Angeles)
list_profs = []
page_num = 1

while True:
	url = "http://www.ratemyprofessors.com/find/professor/?department=&institution={0}&page={1}&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolDetails".format(univ_name.replace(' ', '+'), page_num)
	json_str = urllib2.urlopen(url).read()
	js = json.loads(json_str)
	print (page_num)

	if js["remaining"] == 0:
		break
	else:
		professors = js["professors"]
		for i in range(0, len(professors)):
			tid = professors[i]["tid"]
			fname = professors[i]["tFname"]
			lname = professors[i]["tLname"]
			number_of_ratings = professors[i]["tNumRatings"]
			rating_class = professors[i]["rating_class"]
			overall_rating = professors[i]["overall_rating"]
			dept = professors[i]["tDept"]
			temp = [tid, fname, lname, dept, number_of_ratings, rating_class, overall_rating]
			list_profs.append(temp)
		page_num += 1

print ("Step One: Finished!")

with open('id_profs_{0}.csv'.format(univ_name.replace(' ', '_')), 'wb') as output1:
	write_list = csv.writer(output1, delimiter = ',')
	for row in list_profs:
		write_list.writerow([row[0],])



## Step 2: Getting rating info of each professor
rate_my_professors = []
count = 1
# with open('list_of_professors_{0}.csv'.format(univ_name.replace(' ', '_')), 'rU') as source, open('ratings_professors_{0}.csv'.format(univ_name.replace(' ', '_')), 'wb') as output2:
with open('ratings_professors_{0}.csv'.format(univ_name.replace(' ', '_')), 'wb') as output2:
	# read_list = csv.reader(source, delimiter = ',')	
	# for row in read_list:
	for row in list_profs:		
		prof_id = row[0]
		url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid={0}".format(prof_id)
		print (count)
		html = urllib2.urlopen(url).read()

		avg_grade = re.search('Average Grade\s*.*?>(.*?)<', html).group(1)
		hotness = re.search('chilis/([a-z]*)-chili', html).group(1)
		helpfulness = re.search('Helpfulness</div>\s*.*?>(.*?)<', html).group(1)
		clarity = re.search('Clarity</div>\s*.*?>(.*?)<', html).group(1)
		easiness = re.search('Easiness</div>\s*.*?>(.*?)<', html).group(1)

		row = row + [avg_grade, hotness, helpfulness, clarity, easiness]
		rate_my_professors.append(row)
		count += 1

	write_ratings = csv.writer(output2, delimiter = ',')
	headings = ["id", "First Name", "Last Name", "Department", "Number of Ratings", "Rating Class",\
				"Overall Rating (Overall Quality)", "Average Grade", "Hotness", "Helpfulness",\
				"Clarity", "Easiness"]
	write_ratings.writerow(headings)
	rate_my_professors = [[x.encode('utf-8') if isinstance(x, unicode) else x for x in row] for row in rate_my_professors]
	write_ratings.writerows(rate_my_professors)

print ("Step Two: Finished!")

