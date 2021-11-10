###TRANSFORM DATASET INTO A NEW CSV THAT CAN BE USED FOR UNSUPERVISED CLUSTERING

##USE STRUCTURE

## SID COURSE1 COURSE2 ... COURSE n (WHERE COURSE n IS 1 OR 0 TO REPRESENT IF A STUDENT HAS TAKEN A COURSE)

import pandas as pd

df_grades = pd.read_csv("C:\\Users\\Owner\\Desktop\\100 student dataset.csv")

class student_record:
    course_history = {
        'Chemistry' : 0,
        'Computer Programming' : 0,
        'Personal Computer Lab' : 0,
        'Physics' : 0,
        'Linear Algebra' : 0,
        'Assembly Programming' : 0,
        'Discrete Math' : 0,
        'Engineering Math' : 0,
        'Computer Organization' : 0,
        'Data Structures' : 0,
        'C Programming' : 0,
        'Systems Programming' : 0,
        'Intro Data Processing' : 0,
        'Programming Languages' : 0,
        'Computer Graphics' : 0,
        'Data Base' : 0,
        'Operating System' : 0,
        'Algorithm Design & Analysis' : 0,
        'Parallel Processing' : 0,
        'Distributed Computing' : 0,
        'Computer Network' : 0,
        'Logics' : 0,
        'Object-Oriented Programming' : 0,
        'CS Seminar' : 0,
        'System Analysis' : 0,
        'Numerical Analysis' : 0,
        'Intro Info Systems' : 0,
        'Multimedia Systems' : 0,
        'Intro Analysis' : 0,
        'Formal Languages' : 0,
        'Data Communication' : 0,
        'Simulation' : 0,
        'Computer & Society' : 0,
        'Compiler' : 0,
        'Software Engineering' : 0,
        'Artificial Intelligence' : 0,
        'Statistics' : 0,
        'Microprocessor' : 0,
        'Intro Internet' : 0,
        'Engineering Lab' : 0,
        'Intro Digital Eng' : 0,
        'Digital Eng' : 0,
        'Image Processing' : 0,
        'Data Processing' : 0,
        'Modern Programming' : 0
    }


print(df_grades.head())

headingRow = []
headingRow.append('SID')


##GET COURSE LIST
for index, row in df_grades.iterrows():
    if (row['Course Title']) not in headingRow:
        headingRow.append(row['Course Title'])

print(headingRow)

