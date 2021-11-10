import pandas as pd
import csv

##TODO: WRITE STUDENT IDS TO MATRIX CSV


def compareStudents(SID1, SID2, data):
    SID1_Course = []
    SID2_Course = []
    similarCourses = 0

    for index, row in data.iterrows():
        #if row['SID'] < SID1 and row['SID'] < SID2:        ##I THOUGHT THIS WOULD MAKE THE PROGRAM FASTER, SPOILER ALERT, NO
        #    pass
        #elif row['SID'] > SID1 and row['SID'] > SID2:
         #   pass
        if row['SID'] == SID1:
            SID1_Course.append(row['Course Title'])
        elif row['SID'] == SID2:
            SID2_Course.append(row['Course Title'])

    SID1_Course.sort()
    SID2_Course.sort()

    if (len(SID1_Course) < len(SID2_Course)):    #CHECK IF STUDENT 1 OR 2 HAS MORE COURSES,
        for i in SID1_Course:
            if i in SID2_Course:
                similarCourses += 1
    else:
        for i in SID2_Course:
            if i in SID1_Course:
                similarCourses += 1


    #print("STUDENT " + str(SID1) + ": " + str(len(SID1_Course)))
    #print("STUDENT " + str(SID2) + ": " + str(len(SID2_Course)))

    if (len(SID1_Course) < len(SID2_Course)):
        return round(similarCourses / len(SID1_Course), 2)
    else:
        try:
            return round(similarCourses / len(SID2_Course), 2)
        except:
            print("Error at student " + str(SID2))

NUM_OF_STUDENTS = 100

df = pd.read_csv("C:\\Users\\Dillon\\Desktop\\100 student dataset.csv")
##Matrix creation test

matrix = []

#for index, row in df.iterrows():


def create_matrix():

    for i in range(NUM_OF_STUDENTS):
        sublist = []

        for j in range(NUM_OF_STUDENTS):

            if i != j:
                sublist.append(compareStudents(i + 1, j + 1, df))
            else:
                sublist.append(0)
        print("STUDENT " + str(i+1) + " DONE!")
        matrix.append(sublist)

    with open("C:\\Users\\Dillon\\Desktop\\studentMatrix.csv", "w", newline='') as matrix_file:
        wr = csv.writer(matrix_file, dialect='excel')
        wr.writerows(matrix)


#create_matrix()

df_matrix = pd.read_csv("C:\\Users\\Dillon\\Desktop\\studentMatrix.csv")
