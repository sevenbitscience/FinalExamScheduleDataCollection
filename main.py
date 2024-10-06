# This is the SoC session cookie
cookie = {'ASP.NET_SessionId': '2je3xcwnq5ido4oibcybd2mm'}

# Define what labels will be used for each exam block
dayOne = "Wednesday December 11th"
dayTwo = "Thursday December 12th"
dayThree = "Friday December 13th"
dayFour = "Saturday December 14th"
dayFive = "Monday December 16th"

BLOCK1 = "8:00am - 10:30am"
BLOCK2 = "11:00am - 1:30pm"
BLOCK3 = "2:00pm - 4:30pm"
BLOCK4 = "5:00pm - 7:30pm"

import requests
from bs4 import BeautifulSoup
import datetime
import json

print("[STATUS] Downloading SoC")
response = requests.get('https://navigator.cnu.edu/StudentScheduleofClasses/socresults.aspx', cookies=cookie)
print("[STATUS] Done!")

print("[STATUS] Parsing document into soup")
soup = BeautifulSoup(response.text, 'html.parser')
#soup = BeautifulSoup(open("test.html", 'r'), 'html.parser')        # [DEBUG] Read data from file
print("[STATUS] Done!")

print("[STATUS] Begining class parsing")
try:
    all_classes_raw = soup.find_all("tbody")[0].find_all("tr")
except:
    print("[ERROR] Session Timed Out! Make a legit call to https://navigator.cnu.edu/StudentScheduleofClasses/ fix it")
    quit()

SoC = []

#i = 0

for course in all_classes_raw:
    courseData = course.getText().split('\n')
    #courseData[4].replace(',','').repalace('"','')
    if courseData[2] == "SA 300":
        #print("[DEBUG] SA 300 Handled!")
        SoC.append({'CRN': courseData[1],
                    #'Code': courseData[2],
                    #'Section': courseData[3],
                    'Title': courseData[4],
                    #'LLC Area': courseData[8],
                    #'Type': courseData[9],
                    'Days': '',
                    'Time': '',
                    #'Location': courseData[11][20:],
                    #'Instructor': courseData[12][20:],
                    #'Seats Available': int(courseData[14]),
                    #'Status': courseData[16]
                    })

    elif len(courseData) == 21:
        #print(f"[DEBUG] {i}, {courseData[1]} {courseData[2]}: Class Without Date/Time Handled!")
        SoC.append({'CRN': courseData[1],
                    #'Code': courseData[2],
                    #'Section': courseData[3],
                    'Title': courseData[4],
                    #'Title': courseData[4],
                    #'LLC Area': courseData[8],
                    #'Type': courseData[9],
                    'Days': '',
                    'Time': '',
                    #'Location': courseData[12][20:],
                    #'Instructor': courseData[14][20:],
                    #'Seats Available': int(courseData[16]),
                    #'Status': courseData[18]
                    })

    else:
        SoC.append({'CRN': courseData[1],
                    #'Code': courseData[2],
                    #'Section': courseData[3],
                    'Title': courseData[4],
                    #'LLC Area': courseData[8],
                    #'Type': courseData[9],
                    'Days': courseData[10][20:],
                    'Time': courseData[12][20:],
                    #'Location': courseData[14][20:],
                    #'Instructor': courseData[16][20:],
                    #'Seats Available': int(courseData[18]),
                    #'Status': courseData[20]
                    })
    #i += 1
print("[STATUS] Done!")

# Open the file with the exam schedule in a json format
examScheduleFile = open('exam_schedule.json', 'r')
exam_schedule = json.loads(examScheduleFile.read())
examScheduleFile.close()

# Look up an class time and find what time the exam is
def FindExamTime(ClassTime):
    if ClassTime in exam_schedule["Wednesday"]["1"]:
        return dayOne + " at " + BLOCK1
    if ClassTime in exam_schedule["Wednesday"]["2"]:
        return dayOne + " at " + BLOCK2
    if ClassTime in exam_schedule["Wednesday"]["3"]:
        return dayOne + " at " + BLOCK3
    if ClassTime in exam_schedule["Wednesday"]["4"]:
        return dayOne + " at " + BLOCK4
    
    if ClassTime in exam_schedule["Thursday"]["1"]:
        return dayTwo + " at " + BLOCK1
    if ClassTime in exam_schedule["Thursday"]["2"]:
        return dayTwo + " at " + BLOCK2
    if ClassTime in exam_schedule["Thursday"]["3"]:
        return dayTwo + " at " + BLOCK3
    if ClassTime in exam_schedule["Thursday"]["4"]:
        return dayTwo + " at " + BLOCK4

    if ClassTime in exam_schedule["Friday"]["1"]:
        return dayThree + " at " + BLOCK1
    if ClassTime in exam_schedule["Friday"]["2"]:
        return dayThree + " at " + BLOCK2
    if ClassTime in exam_schedule["Friday"]["3"]:
        return dayThree + " at " + BLOCK3
    if ClassTime in exam_schedule["Friday"]["4"]:
        return dayThree + " at " + BLOCK4

    if ClassTime in exam_schedule["Saturday"]["1"]:
        return dayFour + " at " + BLOCK1
    if ClassTime in exam_schedule["Saturday"]["2"]:
        return dayFour + " at " + BLOCK2
    if ClassTime in exam_schedule["Saturday"]["3"]:
        return dayFour + " at " + BLOCK3
    if ClassTime in exam_schedule["Saturday"]["4"]:
        return dayFour + " at " + BLOCK4

    if ClassTime in exam_schedule["Monday"]["1"]:
        return dayFive + " at " + BLOCK1
    if ClassTime in exam_schedule["Monday"]["2"]:
        return dayFive + " at " + BLOCK2
    if ClassTime in exam_schedule["Monday"]["3"]:
        return dayFive + " at " + BLOCK3
    return "NA"

output = "{\n"
for line in SoC:
    print(line)
    if line['CRN'] == "8549":   # There are two courses that have specific instructions
        output += "\"8549\": \"Thursday December 11th at 8:00pm - 10:30pm\",\n"
        continue
    if line['CRN'] == "8333":
        output += "\"8333\": \"Monday December 16th at 5:00pm - 7:30pm\",\n"
        continue
    datetime = (FindExamTime(line['Days'] + " " + line['Time']))
    output += "\"" + line['CRN'] + "\": [\"" + line['Title'] + "\",\"" + datetime + "\"],\n"
output = output[:-2] + "\n}\n"

with open('CRNsAndExams.json', 'w') as out:
    out.write(output)
