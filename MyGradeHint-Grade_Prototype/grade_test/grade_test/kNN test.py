##
## UPDATE FILE PATHS
##


import pandas as pd
import csv

def helper_function(course, df):
    for index, row in df.iterrows():
        if row['Course Title'] == course:
            return True

    return False

students = []
courses = []

df_grades = pd.read_csv("C:\\Users\\Dillon\\Desktop\\data_cleaned.csv")

for index, row in df_grades.iterrows():
    if (row['SID'] not in students):
        students.append(row['SID'])
    if (row['Course Title'] not in courses):
        courses.append(row['Course Title'])

print("Number of students: " + str(len(students)))
print("Number of courses: " + str(len(courses)))


big_list = []

heading = ['SID']
for i in courses:
    heading.append(i)
big_list.append(heading)



for student in students:
    course_history = []
    course_history.append(student)
    filtered_df = df_grades['SID'] == student
    filtered_df = df_grades[filtered_df]
    #print(filtered_df.shape)

    for course in courses:      ##LEN == 46

        if helper_function(course, filtered_df):
            course_history.append(1)
        else:
            course_history.append(0)

    big_list.append(course_history)



with open("C:\\Users\\Dillon\\Desktop\\cluster.csv", "w", newline='') as matrix_file:
        wr = csv.writer(matrix_file, dialect='excel')
        wr.writerows(big_list)






