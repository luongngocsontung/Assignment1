from io import TextIOWrapper
import numpy as np
import pandas as pd

ANSWER_KEY = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')
FILE_NAME = ""

# Check if line is Valid
def check_valid(line: str):
    valid = True
    values = line.split(',')
    if(len(values) != 26):
        valid = False
        print("!!! Invalid line of data: does not contain exactly 26 values:")
        print(line)
    isHasN = values[0][0] == 'N'
    isLen9 = len(values[0]) == 9

    if(not isHasN or not isLen9 or not values[0][1:].isdigit()):  
        valid = False
        print("!!! Invalid line of data: N# is invalid:")
        print(line)

    return valid

def get_grade(line: str):
    grade = 0
    values = line.split(',')
    for index, value in enumerate(values):
        if(index == 0): continue
        else:
            if(value == ANSWER_KEY[index-1]): grade += 4
            elif(value): grade -= 1

    return [values[0], grade]
    
def analyze_grades(grades: list):
    grade_np = np.array(grades)
    grade_np = np.sort(grade_np)
    mean = grade_np.mean()
    max = grade_np.max()
    min = grade_np.min()
    range_score = max - min
    median = pd.Series(grades).median()
    
    print("Mean (average) score: ", mean)
    print("Highest score: ", max)
    print("Lowest score: ", min)
    print("Range of scores: ", range_score)
    print("Median score: ", median)

def write_student_grade(grades: list, students: list):
    try:
        with open(f"{FILE_NAME}_grades.txt", 'w') as wf:
            for i in range(len(grades)):
                wf.write(f"{students[i]},{grades[i]}\n")
    except IOError:
        print("Error: Couldn't write to file")

def analyze(file: TextIOWrapper):
    errors = False
    grades = []
    students = []
    print("**** ANALYZING ****")
    data = file.readlines()
    file.close()

    total_lines = len(data)
    total_valid_lines = 0
    total_invalid_lines = 0

    for line in data:
        line = line.rstrip() # remove "\n" at the end of string

        if(check_valid(line)):
            total_valid_lines += 1
            student, grade = get_grade(line)
            # Store Student Id and his/her grade
            students.append(student)
            grades.append(grade)
        else: 
            errors = True
            total_invalid_lines += 1
    if(not errors): 
        print("No errors found!")

    print("**** REPORT ****")
    print("Total lines of data: ", total_lines)
    print("Total valid lines of data: ", total_valid_lines)
    print("Total invalid lines of data: ", total_invalid_lines)
    # Grades Infos
    analyze_grades(grades)

    # Write student's grade
    write_student_grade(grades, students)
    
    
def main():
    while(True):
        global FILE_NAME
        FILE_NAME = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
        file = None
        try:
            file = open(FILE_NAME+'.txt', 'r')
            print(f"Successfully opened {FILE_NAME}.txt")
        except:
            print("File cannot be found.")

        if(file):
            analyze(file)

main()