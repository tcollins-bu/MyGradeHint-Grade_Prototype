import pandas as pd
import operator
import time

df = pd.read_csv("C:\\Users\\Dillon\\Desktop\\data_cleaned.csv")


SID_LIST = []
YEARS = []
COURSES = []

grade_points = [
    ['A+', '12'],
    ['A0', '11'],
    ['A-', '10'],
    ['B+', '9'],
    ['B0', '8'],
    ['B-', '7'],
    ['C+', '6'],
    ['C0', '5'],
    ['C-', '4'],
    ['D+', '3'],
    ['D0', '2'],
    ['D-', '1'],
    ['F', '0']
]


def create_grade_history():
    grade_history = {
        'A+' : 0,
        'A0': 0,
        'A-': 0,
        'B+': 0,
        'B0': 0,
        'B-': 0,
        'C+': 0,
        'C0': 0,
        'C-': 0,
        'D+': 0,
        'D0': 0,
        'D-': 0,
        'F': 0
    }

    return grade_history


def getDatasetInfo():
    for index, row in df.iterrows():
        if (row['SID']) not in SID_LIST:
            SID_LIST.append(row['SID'])

        if (row['Year']) not in YEARS:
            YEARS.append(row['Year'])

        if (row['Course Title']) not in COURSES:
            COURSES.append(row['Course Title'])

    #print('\nTotal Students: ' + str(len(SID_LIST)))
    #print('Number of Years: ' + str(len(YEARS)))
    print('Number of Courses: ' + str(len(COURSES)))
    print(COURSES)


def getGradePoints(student_grades_history):
    student_grade_points = 0
    index = 0

    for i in student_grades_history:
        student_grade_points += (student_grades_history[i] * int(grade_points[index][1]))
        index += 1
    return student_grade_points


def makeGradePrediction(data, SID, grading_scale):
    student_grade_points = 0
    student_courses_taken = 0
    student_grade_avg = 0
    grade_history = create_grade_history()

    for index, row in data.iterrows():
        if row['SID'] == SID:
            grade_history[row['Grade']] += 1
            student_courses_taken += 1

    #print(student_grades.grade_history)
    #print(student_courses_taken)
    student_grade_points = getGradePoints(grade_history)


    student_grade_avg = round(student_grade_points / student_courses_taken)
    #print(student_grade_avg)

    #FIND LETTER GRADE
    for i in grading_scale:
        if int(i[1]) == student_grade_avg:
            return i[0]

   # del student_grades
    return('Error')


def compareStudents(SID1, SID2, df_matrix):
   for index, row in df_matrix.iterrows():
        if index == (SID1-1):
            return row[str(SID2)]



def CheckCourse(studentID, compareList, course, df):
    for index,row in df.iterrows():
        if row['SID'] == compareList[1]:
            if (row['Course Title'] == course):
                return True
    return False


def dissimilarity(SID1, SID2, grade_points, data):
    SID1_Grade = ""
    SID2_Grade = ""
    STD1_Grade_Num = 0
    SID2_Grade_Num = 0
    SID1_Course = []
    SID2_Course = []
    similarCourses = []

    for index, row in data.iterrows():
        if row['SID'] == SID1:
            SID1_Course.append(row['Course Title'])
        elif row['SID'] == SID2:
            SID2_Course.append(row['Course Title'])

    SID1_Course.sort()
    SID2_Course.sort()

    if (len(SID1_Course) < len(SID2_Course)):    #CHECK IF STUDENT 1 OR 2 HAS MORE COURSES,
        for i in SID1_Course:
            if i in SID2_Course:
                similarCourses.append(i)
    else:
        for i in SID2_Course:
            if i in SID1_Course:
               similarCourses.append(i)

    sum = 0

    for i in similarCourses:
        for index, row in data.iterrows():
            if row['SID'] == SID1 and row['Course Title'] == i:
                SID1_Grade = row['Grade']
            elif row['SID'] == SID2 and row['Course Title'] == i:
                SID2_Grade = row['Grade']

        for i in grade_points:
            if i[0] == SID1_Grade:
                STD1_Grade_Num = i[1]
            elif i[0] == SID2_Grade:
                SID2_Grade_Num = i[1]

        sum += abs(int(STD1_Grade_Num) - int(SID2_Grade_Num))

    return round(sum / (len(similarCourses) * 12), 2)


### SIMILARITY TEST CASE
#TARGET STUDENT: 1
#TARGET COURSE: Object-Oriented Programming
#print("Similarity Ratio: " + str(compareStudents(1,99,df)))

df_matrix = pd.read_csv("C:\\Users\\Dillon\\Desktop\\studentMatrix.csv")
course = 'Numerical Analysis'
student = 10
correlationList = []
tic = time.time()
print("Read matrix")
#print(df_matrix.head(5))
#getDatasetInfo()

for index, row in df.iterrows():

    if (index == 0):
        last_student = 1
    elif (row['SID'] == student):
        pass
    else:
        if row['SID'] != last_student:
            correlationList.append([compareStudents(student, int(row['SID']), df_matrix), row['SID']])    ##STUDENT 1 HARDCODED HERE
            last_student = int(row['SID'])


correlationList.sort(key=lambda x: x[0])
correlationList.reverse()


## GET LIST OF STUDENTS WHO HAVE TAKEN COURSE c AND HAVE THE HIGHEST CORRELATION TO STUDENT s
dissimilarityList = []
for i in correlationList:
    if (len(dissimilarityList) < 5):
        if (CheckCourse(student, i, course, df)):          # i = [correlation, SID]
            dissimilarityList.append(i[1])
    else:
        break

#print(dissimilarityList)


## FIND STUDENT WITH LOWEST DISSIMILARITY TO STUDENT s
lowestDissimilarity = 1.0
for i in dissimilarityList:
    dissimilarityRatio = 1.0
    selected_student = 0.0
    dissimilarityRatio = dissimilarity(student, i, grade_points, df)

    if dissimilarityRatio < lowestDissimilarity:
        selected_student = i
        lowestDissimilarity = dissimilarityRatio

for index, row in df.iterrows():
    if row['SID'] == i and row['Course Title'] == course:
        print('Predicted grade in course, ' + course + ", is : " + str(row['Grade']))
        print('Prediction obtained using Student ' + str(i))
        #print('Estimated accuracy of prediction: ' + str(1 - round(lowestDissimilarity, 2)))


toc = time.time()
print("This operation took " + str(toc-tic) + " seconds.")




def gradePredict():
    print("Grade Prediction System.")
    SID = ''

    while (SID != 0):
        SID = int(input("\nEnter Student ID (0 to stop): "))
        if (SID == 0):
            pass
        else:
            print("Student " + str(SID) + " is predicted to get a(n): " + makeGradePrediction(df, SID, grade_points))


