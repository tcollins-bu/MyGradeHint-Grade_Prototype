import pandas as pd
import time as t
import random as r
import statistics

data = pd.read_csv("100 student dataset.csv")

##GET RID OF UNIMPORTANT DATA
data = data.drop(columns='Credit')

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


##GETS LIST OF UNIQUE ATTRIBUTES FOR ALL FEATURES OF DATASET, SOME ARE REFERENCED IN PROGRAM
def getDatasetInfo(df):
    for index, row in df.iterrows():
        if (row['SID']) not in SID_LIST:
            SID_LIST.append(row['SID'])

        if (row['Year']) not in YEARS:
            YEARS.append(row['Year'])

        if (row['Course Title']) not in COURSES:
            COURSES.append(row['Course Title'])

##TAKES 2 STUDENT IDS AND A FILTERED DATAFRAME AS INPUT, COMPARES BOTH STUDENTS COURSE HISTORY FOR SIMILARITY AND
##RETURNS A DECIMAL FROM 0 TO 1
def compareStudents(SID1, SID2, df_student):
    SID1_LIST = []
    SID2_LIST = []

    for index, row in df_student.iterrows():

        if row['SID'] == SID1:
            SID1_LIST.append(row['Course Title'])
        elif row['SID'] == SID2:
            SID2_LIST.append(row['Course Title'])

    similarCourses = 0

    if (len(SID1_LIST) > len(SID2_LIST)):
        for course in SID2_LIST:
            if course in SID1_LIST:
                similarCourses += 1
        try:
            return float(round(similarCourses / len(SID2_LIST), 2))
        except:
            return 0.0

    else:
        for course in SID1_LIST:
            if course in SID2_LIST:
                similarCourses += 1
        try:
            return float(round(similarCourses / len(SID1_LIST), 2))
        except:
            return 0.0


##CHECKS IF A SPECIFIC STUDENT IN THE COMPARE LIST PARAMETER HAS TAKEN A SPECIFIC COURSE, RETURNS TRUE OR FALSE
def CheckCourse(studentID, compareList, course, df):

    for index,row in df.iterrows():
        if row['SID'] == compareList[1]:
            if (row['Course Title'] == course):
                return True
    return False


##INPUTS A STUDENT ID AND A COURSE TITLE, RETURNS THE GRADE THE STUDENT GOT IN THAT SPECIFIC COURSE
def LookupGrade(SID, SID_Course, df):

    for index, row in df.iterrows():
        if row['SID'] == SID and row['Course Title'] == SID_Course:
            return df['Grade'].iloc[index]


##INPUTS TWO STUDENT IDS AND A SPECIFIC YEAR AND SEMESTER, FILTERS A DATAFRAME TO ONLY RECORDS FOR EITHER STUDENT BEFORE
##THE SPECIFIED YEAR AND SEMESTER AND OUTPUTS A DECIMAL FROM 0 TO 1 THAT DESCRIBES HOW SIMILAR THE TWO STUDENTS GRADE
##HISTORY IS
def dissimilarity(SID1, SID2, year, semester, df):
    filteredFrame = df.copy()

    ##FILTER DATAFRAME TO JUST RECORDS FOR TWO STUDENTS
    filteredFrame = filteredFrame[(filteredFrame['SID'] == SID1) | (filteredFrame['SID'] == SID2)]


    ##FILTER DATAFRAME TO RECORDS ONLY BEFORE THE YEAR AND SEMESTER
    filteredFrame = filteredFrame[(filteredFrame['Year'] < year) |
                                  ((filteredFrame['Year'] == year) & (filteredFrame['Semester'] < semester))]

    SID1_Grade = ""
    SID2_Grade = ""
    SID1_Grade_Num = 0
    SID2_Grade_Num = 0
    SID1_Course = []
    SID2_Course = []
    similarCourses = []

    for index, row in filteredFrame.iterrows():
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
        for index, row in filteredFrame.iterrows():
            if row['SID'] == SID1 and row['Course Title'] == i:
                SID1_Grade = row['Grade']
            elif row['SID'] == SID2 and row['Course Title'] == i:
                SID2_Grade = row['Grade']


        for j in grade_points:
            if j[0] == SID1_Grade and j[0] == SID2_Grade:
                SID1_Grade_Num = j[1]
                SID2_Grade_Num = j[1]
            elif j[0] == SID1_Grade:
                SID1_Grade_Num = j[1]
            elif j[0] == SID2_Grade:
                SID2_Grade_Num = j[1]

        sum += abs(int(SID1_Grade_Num) - int(SID2_Grade_Num))

    try:
        return round(sum / (len(similarCourses) * 12), 2)
    except:
        ##DIV BY 0
        return 0


##INPUTS A SEMESTER, STUDENT ID, AND YEAR AND RETURNS A LIST OF THE SPECIFIED STUDENTS SIMILARITY OF COURSE WORK TO ALL
##OTHER STUDENTS IN THE DATASET
def getCorrelationList(course, semester, student, year, df):
    correlationList = []

    for SID in SID_LIST:
        if (student == SID):
            ##SKIP THEMSELF
            pass
        else:
            ##NOT STUDENT 1
            filteredFrame = df.copy()

            ##FILTER DATAFRAME TO JUST RECORDS FOR TWO STUDENTS
            filteredFrame = filteredFrame[(filteredFrame['SID'] == SID) | (filteredFrame['SID'] == student)]
            #print(filteredFrame.head())

            ##FILTER DATAFRAME TO RECORDS ONLY BEFORE THE YEAR AND SEMESTER
            filteredFrame = filteredFrame[(filteredFrame['Year'] < year) |
                                          ((filteredFrame['Year'] == year) & (filteredFrame['Semester'] < semester))]

            correlationList.append([compareStudents(student, SID, filteredFrame), SID])

    return correlationList


##MAIN FUNCTION OF PROGRAM, REQUIRES A LIST OF STUDENT INFO IN THE FOLLOWING ORDER, [SID, YEAR, SEMESTER, COURSE] AND
##AFTER_GRADE_INFO WHICH IS A LIST OF PREVIOUS STUDENTINFO
##OUTUTS THE LETTER GRADE PREDICTION FOR THE STUDENT IN THE COURSE
def makePrediction(studentInfo, data, after_grade_info = [], n_neighbors=5):
    df = data.copy()
    student = studentInfo[0]
    year = studentInfo[1]
    semester = studentInfo[2]
    course = studentInfo[3]


    ##ADDS STUDENT INFO FROM AFTER_GRADE_INFO TO DATAFRAME IN CASE OF AFTER GRADE PREDICTION
    if after_grade_info == []:
        pass
    else:
        for row in after_grade_info:
            df.append(row)

    correlationList = getCorrelationList(course, semester, student, year, df)

    correlationList.sort(key=lambda x: x[0])
    correlationList.reverse()


    ## GET LIST OF STUDENTS WHO HAVE TAKEN COURSE c AND HAVE THE HIGHEST CORRELATION TO STUDENT s
    dissimilarityList = []
    for i in correlationList:
        if (len(dissimilarityList) < (n_neighbors)):
            if (CheckCourse(student, i, course, df)):          # i = [correlation, SID]
                dissimilarityList.append(i[1])
        else:
            break

    dissimilarityRatios = []

    for i in dissimilarityList:
        dissimilarityRatio = dissimilarity(student, i, year, semester, df)
        dissimilarityRatios.append([1-dissimilarityRatio, i])

    grade = getWeightedAvg(dissimilarityRatios, course, df)

    for i in grade_points:
        if i[1] == str(int(grade)):
            prediction = (i[0])

    return prediction


##INPUTS A LIST WEIGHTS AND STUDENT IDS AND A SPECIFIC COURSE TITLE
##WEIGHTED_AVG = SUM(WEIGHT * NUMERICAL_GRADE) / SUM(WEIGHTS
##RETURNS THE WEIGHTED AVERAGE WHICH IS THE NUMERICAL REPRESENTATION OF A GRADE
def getWeightedAvg(lst, course, df):
    numerator = 0.0
    weightSum = 0.0

    for student in lst:
        grade = LookupGrade(student[1], course, df)

        weightSum += student[0]

        for i in grade_points:

            if i[0] == grade:
                gradeNum = int(i[1])

                numerator += (student[0] * gradeNum)

    try:
        return (numerator / weightSum)

    except:
        ##DIV BY ZERO
        ##LIST OF SIMILAR STUDENTS COULD BE EMPTY
        return 0


##RUNS A CUSTOMIZABLE TEST CASE, CAN HARDCODE A SPECIFIC STUDENT ID, NUMBER OF PREDICTIONS, NUMBER OF NEIGHBORS, ETC
##RETURNS THE ACCURACY FOR THE SET OF PREDICTIONS GENERATED AND THE NUMBER OF NEIGHBORS USED
def testCase(df):
    N_TRIALS = 5
    n_neighbors = 6
    target_SID = r.randint(1, len(SID_LIST))

    total_distance = 0.0

    for i in range(N_TRIALS):
        filteredDF = df.copy()
        sublist = []

        try:
            filteredDF = filteredDF[filteredDF['SID'] == target_SID]

            rowIndex = r.randint(0, len(filteredDF)-1)

        except:
            print('Issue with Dataframe creation')
            print("SID: " + str(target_SID))
            print(filteredDF.head())
            print(filteredDF.shape)
            break

        try:
            row = filteredDF.iloc[rowIndex]
        except:
            print("Issue with record lookup")
            print(rowIndex, len(filteredDF))
            break

        sublist.append(row[0])
        sublist.append(row[1])
        sublist.append(row[2])
        sublist.append(row[3])

        prediction = (makePrediction(sublist, df, n_neighbors=n_neighbors))
        actual = row[4]

        prediction_num = 0
        actual_num = 0

        for i in grade_points:
            if prediction == i[0] and actual == i[0]:
                prediction_num = i[1]
                actual_num = i[1]
            elif (prediction == i[0]):
                prediction_num = i[1]
            elif (actual == i[0]):
                actual_num = i[1]

        ##DETERMINES THE MANHATTAN DISTANCE FROM THE ACTUAL ANSWER
        total_distance += abs(int(actual_num) - int(prediction_num))

        del filteredDF

    ##DETERMINES THE ACCURACY OF THE PREDICTION BASED ON THE FOLLOWING FORMULA
    ## ACCURACY = ( 1 - ( SUM(MANHATTAN_DISTANCE) / (NUMBER_OF_TRIALS * HIGHEST_NUMERIC_GRADE) ) ) * 100
    accuracy = round(1 - (total_distance / (N_TRIALS * 12)), 2) * 100
    return [accuracy, n_neighbors]


####                    ####
##    TESTING PORTION     ##
####                    ####

NUMBER_OF_TESTS = 10


getDatasetInfo(data)
accuracy_list = []
variance_list = []

tic = t.time()

for i in range(NUMBER_OF_TESTS):
    returnList = testCase(data)
    accuracy = returnList[0]
    accuracy_list.append(accuracy)
    n_neighbors = returnList[1]
    print(f"TEST {i}: \tAccuracy: {round(accuracy, 2)}% \n\t\t\tk_neighbors: {n_neighbors}")
    print()

accuracy_mean = statistics.mean(accuracy_list)

print(f"Average accuracy over {NUMBER_OF_TESTS} trials: {accuracy_mean}%")
print(f"Variance of accuracy from mean: {round(statistics.variance(accuracy_list), 2)}")
print(f"Standard Deviation from the mean: {round(statistics.stdev(accuracy_list), 2)}")
print(f"Time to complete: {str(round(t.time() - tic, 2))} seconds.")
