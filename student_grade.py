#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
from datetime import datetime

student_list = []
subject_list = []
Test_1 = {}
Test_2 = {}
Final = {}
results = {
    "Test_1": Test_1,
    "Test_2": Test_2,
    "Final": Final
}
current_year = datetime.now().strftime("%Y")
student_archive = {}
DATA_FILE = "students.json"
total_student = 0
class_avg = 0

def load_data():
    global results, student_archive, total_student, class_avg, student_list, subject_list, Test_1, Test_2, Final, current_year
    try:
        with open(DATA_FILE,"r") as f:
            data = json.load(f)
            last_year = data.get("year",current_year)
            class_avg = data.get("class_average",0)
            total_student = data.get("total_student",0)
            results = data.get("results",{
                "Test_1" : {},
                "Test_2" : {},
                "Final" : {}
            })
            student_list = data.get('student_list',[])
            subject_list = data.get('subject_list',[])
            student_archive = data.get('student_archive',{})
            Test_1 = results["Test_1"]
            Test_2 = results["Test_2"]
            Final = results["Final"]

            if last_year != current_year:
                student_archive[last_year] = {
                    "results":results,
                    "student_list" : student_list,
                    "subject_list" : subject_list
                }
                Test_1 = {}
                Test_2 = {}
                Final = {}
                results = {
                    "Test_1":Test_1,
                    "Test_2":Test_2,
                    "Final":Final
                }
                total_student = len(student_list)
                class_avg = 0

    except (FileNotFoundError,json.JSONDecodeError):
        student_list = []
        subject_list = []
        total_student = 0
        class_avg = 0
        Test_1 = {}
        Test_2 = {}
        Final = {}
        results = {
            "Test_1" : Test_1,
            "Test_2" : Test_2,
            "Final" : Final
        }
        student_archive = {}

def save_data():
    global student_list, class_avg, total_student, current_year, results, subject_list, student_archive
    saved_data = {
        "year" : current_year,
        "class_average" : class_avg,
        "total_student" : total_student,
        "student_list" : student_list,
        "subject_list" : subject_list,
        "results" : results,
        "student_archive":student_archive
    }
    with open(DATA_FILE,"w") as f:
        json.dump(saved_data,f,indent = 4)

def display_student_list():
    print()
    print(f"-"*90)
    print(f"{'Student list':^90}")
    print(f"{current_year:^90}")
    print(f"-"*90)
    for num,name in enumerate(student_list,start=1):
        print(f"{num:<5}{name:<20}")
    print(f"-"*90)

def display_subject_list():
    print()
    print(f"-"*90)
    print(f"{'Subject list':^90}")
    print(f"{current_year:^90}")
    print(f"-"*90)
    for num,subject in enumerate(subject_list,start=1):
        print(f"{num:<5}{subject:<20}")
    print(f"-"*90)

def total_number_student():
    global total_student
    total_student = len(student_list)
    return total_student

def individual_avg_score(test):
    global results
    excluded_name = {'class_average','total_student','top_student'}
    for student_name,info in results[test].items():
        if student_name not in excluded_name:
            total_mark = 0
            total = 0
            avg = 0
            excluded = {"Average","Grade"}
            for subject,mark in info.items():
                if subject not in excluded:
                    total_mark += mark
                    total += 1
            avg = total_mark/total
            info.update({"Average":round(avg,2)})

def individual_grade(test):
    global results
    excluded_name = {'class_average','total_student','top_student'}
    for name,subject in results[test].items():
        if name not in excluded_name:
            avg_score = subject.get("Average")
            if 90 <= avg_score <= 100:
                grade = "A+"
            elif 80 <= avg_score < 90:
                grade = "A"
            elif 75 <= avg_score < 80:
                grade = "B+"
            elif 70 <= avg_score < 75:
                grade = "B"
            elif 60 <= avg_score < 70:
                grade = "C"
            elif 50 <= avg_score < 60:
                grade = "D"
            elif avg_score < 50:
                grade = "Fail"
            subject.update({"Grade":grade})

def calculate_class_avg(test):
    global class_avg,results
    total_mark = 0
    excluded_name = {'class_average','total_student','top_student'}
    for name,info in results[test].items():
        if name not in excluded_name:
            marks = info.get("Average")
            total_mark += marks
    class_avg = total_mark / len(student_list)
    results[test]["class_average"] = round(class_avg,2)

def update_student_score():
    print()
    print(f"="*90)
    print(f"{"Update student's score":^90}")
    print(f"="*90)
    if len(student_list) == 0:
        print(f"\nThere are no student recorded in the system, please update the student list first.")
    else:
        print(f"1. Test 1")
        print(f"2. Test 2")
        print(f"3. Final")
        print(f"4. Save and exit")
        print(f"-"*90)
        selection = {"1": "Test_1", "2" : "Test_2", "3" : "Final"} 
        choice = input(f"Please select from (1-4): ")
        if choice == '4':
            save_data()
            print(f"\nSuccessfully saved all the data!")
            print(f"Returning to homepage...")
        elif choice in selection:
            selected_choice = selection[choice] #"Test_1" - string only
            test_selection = {"Test_1": Test_1, "Test_2" : Test_2, "Final" : Final}
            selected_test = test_selection[selected_choice] #Test_1 - the dictionary
            #add students_name to test
            for name in student_list:
                if name not in results[selected_choice]:
                    selected_test[name] = {}
            #print student list with the status
            while True:
                print()
                print(f"-"*60)
                print(f"{selected_choice:^60}")
                print(f"-"*60)
                print(f"{"No.":<5}{"Student name":<25}{"Status":^10}{"Remaining":^13}")
                print(f"-"*60)
                excluded = {"Average","Grade"}
                excluded_name = {'class_average','top_student','total_student'}
                counter = 0
                for student_name,info in sorted(selected_test.items()):
                    if student_name not in excluded_name:
                        number_subject = 0
                        for subject,mark in info.items():
                            if subject not in excluded:
                                number_subject += 1
                        counter += 1
                        if number_subject == len(subject_list):
                            status = f'\u2714' #✔
                        else:
                            status = f'\u2717' #✘
                        remain_subject = f"{number_subject}/{len(subject_list)}"
                        print(f"{counter:<5}{student_name:<25}{status:^10}{remain_subject:^13}")
                print(f"-"*60)
                print(f"Please select (1-{len(student_list)}) to choose the corresponding student OR 'q' to quit.")
                choice = input(f"")
                if choice.lower() == 'q':
                    try:
                        individual_avg_score(selected_choice)
                        individual_grade(selected_choice)
                        calculate_class_avg(selected_choice)
                        save_data()
                        print(f"\nSuccessfully save and update all the results.")
                        print(f"Returning to previous page...")
                        break
                    except ZeroDivisionError:
                        print(f"\nReturning to previous page...")
                        break
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(student_list):
                        student_name = student_list[idx]
                        while True:
                            print()
                            print(f"-"*60)
                            print(f"Student : {student_name}")
                            for num,subject in enumerate(subject_list,start=1):
                                if subject in selected_test[student_name]:
                                    print(f"{num:<5}{subject:<15}:{selected_test[student_name].get(subject):>6}")
                                else:
                                    print(f"{num:<5}{subject:<15}:{"":>6}")
                            print(f"-"*60)
                            print(f"Please select (1-{num}) to update the corresponding subject OR 'q' to quit.")
                            choice = input(f"")
                            if choice.lower() == 'q':
                                print(f"\nReturning to previous page...")
                                break
                            elif choice.isdigit():
                                idx_subject = int(choice)-1
                                if 0<= idx_subject < len(subject_list):
                                    subject_name = subject_list[idx_subject]
                                    marks = input(f"\nPlease enter the mark for {subject_name}: ")
                                    if marks.isdigit():
                                        if int(marks) >= 0:
                                            selected_test[student_name].update({subject_name:int(marks)})
                                        else:
                                            print(f"\n{marks} is an invalid prompt! Please enter a positive value.")
                                else:
                                    print(f"\nInvalid prompt! Please select (1-{counter}) to update the corresponding subject.")
                                    continue

                    else:
                        print(f"\nInvalid prompt! Please select from (1-{len(student_list)}).")
                else:
                    print(f"\nInvalid prompt! Please select from (1-{len(student_list)}).")
        else:
            print(f"\nInvalid prompt! Please select from (1-4).")

def option_1():
    global total_student, student_list, subject_list, Test_1, Test_2, Final, results
    while True:
        print()
        print(f"="*90)
        print(f"{'Add or update student scores':^90}")
        print(f"{current_year:^90}")
        print(f"="*90)
        print(f"1. Add student name")
        print(f"2. Add new subject")
        print(f"3. Update student's score")
        print(f"4. Remove student name")
        print(f"5. Remove subject")
        print(f"6. View student and subject list")
        print(f"7. Save and exit")
        print(f"-"*90)
        choice = input(f"Please select from (1-7): ")
        if choice == '7':
            total_number_student()
            save_data()
            print(f"\nThe students and subjects has been updated!")
            break
        elif choice == '1':
            print()
            print(f"="*90)
            print(f"{'Add student name':^90}")
            print(f"="*90)
            while True:
                student_name = input(f"\nPlease enter the student's name or 'q' enter to quit: ")
                if student_name.lower() == 'q':
                    total_number_student()
                    save_data()
                    print(f"Returning to home page...")
                    break
                elif student_name == "" or student_name == " ":
                    print(f"Unable to save empty prompt to student list")
                    continue
                elif student_name in student_list:
                    print(f"{student_name} already exist.")
                    continue
                elif student_name not in student_list:
                    student_list.append(student_name.title())
                    print(f"Successfully added {student_name.title()} into system!")
                    student_list.sort()
                else:
                    print(f"\nInvalid prompt! Please select from the provided range.")
        elif choice == '2':
            print()
            print(f"="*90)
            print(f"{"Add new subject":^90}")
            print(f"="*90)
            print(f"{'Subject list':^90}")
            print(f"-"*90)
            for num,subjects in enumerate(subject_list,start=1):
                print(f"{num:<5}{subjects:<15}")
            print(f"-"*90)
            while True:
                subject_name = input(f"Please enter the name of the subject OR 'q' to quit: ")
                if subject_name.lower() == 'q':
                    save_data()
                    print(f"Returning to home page...")
                    break
                elif subject_name in subject_list:
                    print(f"{subject_name} already exist in the system!")
                elif subject_name == "" or subject_name == " ":
                    print(f"Unable to save empty prompt to subject list.")
                    continue
                else:
                    subject_list.append(subject_name.title())
                    subject_list.sort()
                    print(f"{subject_name.title()} has successfully added into the system!")
                    print()
        elif choice == '3':
            update_student_score()
            print()
        elif choice == "4":
            print()
            print(f"="*90)
            print(f"{'Remove student name':^90}")
            print(f"="*90)
            if len(student_list) == 0:
                print(f"\nUnable to remove any students, since there are no student recorded in the system.")
            elif len(student_list) == 1:
                print(f"{'No.':<5}{'Student name':<20}")
                print(f"-"*90)
                for index, name in enumerate(student_list,start = 1):
                    print(f"{index:<5}{name:<20}")
                print(f"-"*90)
                print(f"\nPlease enter (1) to remove the corresponding student's name from the system.")
                print(f"Press 'q' to quit")
                value = input(f"")
                if value.isdigit():
                    idx = int(value)-1
                    student_name = student_list[idx]
                    student_list.remove(student_name)
                    print(f"{student_name} has been removed from the system.")
                else:
                    print(f"Invalid Prompt! Please try again.")
            elif len(student_list) > 1:
                print(f"{'No.':<5}{'Student name':<20}")
                print(f"-"*90)
                for index, name in enumerate(student_list,start = 1):
                    print(f"{index:<5}{name:<20}")
                print(f"-"*90)
                print(f"Please select (1-{len(student_list)}) to remove the corresponding student's name.")
                print(f"Press 'q' to quit")
                value = input(f"")
                if value.isdigit():
                    if 0<= int(value)-1 < len(student_list):
                        idx = int(value) - 1
                        student_name = student_list[idx]
                        student_list.remove(student_name)
                        print(f"{student_name} has been removed from the system.")
                    else:
                        print(f"Invalid prompt! The value selected is not within the range.")
                else:
                    print()
                    print(f"Invalid prompt! Please select from (1-{len(student_list)})")
        elif choice == '5':
            print()
            print(f"="*90)
            print(f"{"Remove subject":^90}")
            print(f"="*90)
            if len(subject_list) == 0:
                print(f"\nUnable to remove any subjects, since there are no record of subject in the system!")
            else:
                print(f"{'Subject list':^90}")
                print(f"-"*90)
                for num,subjects in enumerate(subject_list,start=1):
                    print(f"{num:<5}{subjects:<15}")
                print(f"-"*90)
                if len(subject_list) == 1:
                    print(f"Please enter (1) to remove the corresponding subject.")
                    print(f"Press 'q' to quit.")
                    subject_value = input(f"")
                    if subject_value.isdigit() and int(subject_value) == 1:
                        subject_idx = int(subject_value) - 1
                        subject_name = subject_list[subject_idx]
                        subject_list.remove(subject_name)
                        print(f"\n{subject_name} has successfully removed from the system.")
                elif len(subject_list) > 1:
                    print(f"Please select (1-{len(subject_list)}) to remove the corresponding subject.")
                    print(f"Press 'q' to quit.")
                    subject_value = input(f"")
                    if subject_value.isdigit() and 0<= int(subject_value)-1 < len(subject_list):
                        subject_idx = int(subject_value) - 1
                        subject_name = subject_list[subject_idx]
                        subject_list.remove(subject_name)
                        print(f"\n{subject_name} has successfully removed from the system.")
        elif choice == '6':
            while True:
                print()
                print(f"="*90)
                print(f"{"Reveal student and subject list":^90}")
                print(f"="*90)
                print(f"1. Student list")
                print(f"2. Subject list")
                print(f"3. Exit")
                print(f"-"*90)
                choice = input(f"Please select (1-3): ")
                if choice == '1':
                    display_student_list()
                elif choice == '2':
                    display_subject_list()
                elif choice == '3':
                    break
                else:
                    print(f"Invalid prompt! Please select (1-3).")
        else:
            print()
            print(f"Invalid prompt! Please select from (1-7)")

#View individual Report
def option_2():
    while True:
        print()
        print(f"="*90)
        print(f"{'View individual report':^90}")
        print(f"="*90)
        student_name = input(f"Please enter the student name OR 'q' to quit: ")
        if student_name.lower() == 'q':
            print(f"Returning to homepage...")
            break
        elif student_name.title() in student_list:
            while True:
                print()
                print(f"-"*60)
                print(f"Student name: {student_name.title()}")
                print(f"-"*60)
                print(f"1. Test 1")
                print(f"2. Test 2")
                print(f"3. Final")
                print(f"4. Exit")
                print(f"-"*60)
                choice = input(f"Please select (1-4): ")
                if choice.isdigit():
                    if choice == '4':
                        break
                    elif 0<= int(choice)-1 <len(results.keys()):
                        idx_test = int(choice)-1
                        test_list = list(results.keys())
                        try:
                            results_data = results[test_list[idx_test]][student_name.title()]
                            print()
                            print(f"="*60)
                            print(f"{'Individual Report of':^60}")
                            print(f"{student_name.title():^60}")
                            print(f"="*60)
                            print(f"{'No.':<5}{'Subject name':<20}{'Score':^9}")
                            print(f"-"*60)
                            counter = 0
                            excluded = {"Average","Grade"}
                            for subject,mark in results_data.items():
                                if subject not in excluded:
                                    counter += 1
                                    print(f"{counter:<5}{subject:<20}{mark:^9}")
                            print(f"-"*60)
                            print(f"Average mark : {results_data.get("Average"):.2f}")
                            print(f"Grade        : {results_data.get("Grade")}")
                            print()
                        except KeyError:
                            print()
                            print(f"{student_name.title()} did not participate in {test_list[idx_test]}.")
                    else:
                        print(f"\nInvalid prompt! Please select from (1-4).")
                else:
                    print(f"\nInvalid prompt! Please enter a positive whole number.")
                    continue
        elif student_name.title() not in student_list:
            print(f"\n{student_name.title()} not found in the system.\n")
            continue

#View class performance
def option_3():
    while True:
        test_list = list(results.keys())
        print()
        print(f"="*90)
        print(f"{'View class performance':^90}")
        print(f"="*90)
        print(f"1. Test 1")
        print(f"2. Test 2")
        print(f"3. Final")
        print(f"4. Exit")
        print(f"-"*90)
        choice = input(f"Please select (1-4): ")
        if choice.isdigit():
            if choice == '4':
                print(f"\nReturning to homepage...")
                break
            elif 0<= int(choice)-1 < len(test_list):
                idx_test = int(choice)-1
                result_data = results[test_list[idx_test]]
                counter = 0
                if not result_data.values():
                    print(f"\nUnable to display class performance result since there are no records for {test_list[idx_test]}")
                else:
                    print()
                    print(f"="*60)
                    print(f"{test_list[idx_test]:^60}")
                    print(f"="*60)
                    print(f"{'No':<5}{'Student name':<20}{'Average score':^17}{'Grade':^9}")
                    top = ""
                    best_avg = 0
                    excluded_name = {"class_average","top_student","total_student"}
                    for name,info in result_data.items():
                        if name not in excluded_name:
                            counter += 1
                            print(f"{counter:<5}{name:<20}{info.get("Average"):^17}{info.get("Grade"):^9}")
                            if info.get("Average") > best_avg:
                                best_avg = info.get("Average")
                                top = name
                    print(f"-"*60)
                    print(f"Total student : {total_student}")
                    print(f"Class average : {class_avg:.2f}")
                    print(f"Top student   : {top} with {best_avg} average mark")
                    result_data["class_average"] = round(class_avg,2)
                    result_data["top_student"] = top
                    result_data["total_student"] = total_student
            else:
                print(f"\nInvalid prompt! Please select from (1-4).")
        else:
            print(f"\nInvalid prompt! Please enter a positive whole number.")

#View subject ranking
def option_4():
    while True:
        print()
        print(f"="*90)
        print(f"{'View subject ranking':^90}")
        print(f"="*90)
        print(f"1. Test 1\n2. Test 2\n3. Final\n4. Exit")
        print(f"-"*90)
        choice = input(f"Please select (1-4): ")
        if choice.isdigit():
            if choice == '4':
                print(f"\nReturning to homepage...")
                break
            elif 0 <= int(choice)-1 < len(results.keys()):
                idx_test = int(choice)-1
                test_list = list(results.keys())
                selected_test = results[test_list[idx_test]] # Test_1 dictionary
                if not selected_test.values():
                    print(f"\nUnable to reveal subject ranking since there are no relevant data.")
                else:
                    rank_set = {}
                    excluded = {"Average","Grade"}
                    print()
                    print(f"-"*60)
                    print(f"{'Best scrorer':^60}")
                    print(f"-"*60)
                    print(f"{'Subject':<20}{'Student name':<20}{'Score':^9}")
                    print(f"-"*60)
                    excluded_name = {"class_average","top_student",'total_student'}
                    for name,info in selected_test.items():
                        if name not in excluded_name:
                            for subject,marks in info.items():
                                if subject not in excluded:
                                    if subject not in rank_set:
                                        rank_set[subject] = {name:marks}
                                    elif subject in rank_set:
                                        rank_set[subject].update({name:marks})
                    for subject,info in rank_set.items():
                        top_scrorer = ""
                        best_mark = 0
                        for name,mark in info.items():
                            if mark > best_mark:
                                best_mark = mark
                                top_scrorer = name  
                        print(f"{subject:<20}{top_scrorer:<20}{best_mark:^9}")
                    print(f"-"*60)
                    print(f"{'Student required improvement':^60}")
                    print(f"-"*60)
                    print(f"{'Subject':<20}{'Student name':<20}{'Score':^9}")
                    print(f"-"*60)
                    for subject,info in rank_set.items():
                        least_scrorer = ""
                        least_mark = 100
                        for name,mark in info.items():
                            if mark < least_mark:
                                least_mark = mark
                                least_scrorer = name
                        print(f"{subject:<20}{least_scrorer:<20}{least_mark:^9}")
                    print(f"-"*60)
            else:
                print(f"\nInvalid prompt! Please select from (1-4).")
        else:
            print(f"\nInvalid prompt! Please select from (1-4).")

#Reveal archive
def option_5():
    global student_archive
    year_list = list(student_archive.keys())
    print()
    print(f"="*90)
    print(f"{'Reveal archive':^90}")
    print(f"="*90)
    print(f"{'No.':<5}{'Academic year':<18}")        
    print(f"-"*90)
    for num,year in enumerate(year_list,start=1):
        print(f"{num:<5}{year}")
    print(f"-"*90)
    if len(year_list) == 1:
        choice = input(f"Please select (1) to reveal the archive: ")
        if choice.isdigit():
            if choice == '1':
                selected_year = year_list[0]
                print()
                print(f"-"*60)
                print(f"{selected_year:^60}")
                print(f"-"*60)
                print(f"1. Test 1")
                print(f"2. Test 2")
                print(f"3. Final")
                print(f"-"*60)
                choice_2 = input(f"Please select (1-3): ")
                if choice_2.isdigit():
                    idx_test = int(choice_2) - 1
                    if 0<= idx_test < 3:
                        test_list = list(student_archive[selected_year]["results"].keys())
                        selected_test = student_archive[selected_year]["results"][test_list[idx_test]]# Test_1 dictionary
                        excluded_name = {'class_average','total_student','top_student'}
                        actual_students = {k:v for k,v in selected_test.items() if k not in excluded_name}
                        if actual_students:
                            print()
                            print(f"-"*60)
                            print(f"{test_list[idx_test]:^60}")
                            print(f"{selected_year:^60}")
                            print(f"-"*60)
                            print(f"{'No.':<5}{'Student name':<20}{'Average score':^17}{'Grade':^9}")
                            print(f"-"*60)
                            total_marks = 0
                            top_student = ""
                            highest_avg = -1.0
                            for counter, (name,info) in enumerate(actual_students.items(),start = 1):
                                avg = info.get("Average",0.0)
                                grade = info.get("Grade","")
                                print(f"{counter:<5}{name:<20}{avg:^17}{grade:^9}")

                                total_marks += avg
                                if avg>highest_avg:
                                    highest_avg = avg
                                    top_student = name
                            class_avg = total_marks / len(actual_students) if actual_students else 0.0
                            print(f"-"*60)
                            print(f"Total student : {len(actual_students)}")
                            print(f"Class average : {class_avg:.2f}")
                            print(f"Top student   : {top_student} with {highest_avg:.2f} average mark")
                            print()
                        else:
                            print(f"\nNo historical data for {test_list[idx_test]}")
                    else:
                        print(f"\nInvalid prompt! Please select from (1-3).")
                else:
                    print(f"\nInvalid prompt! Please select from (1-3).")
            else:
                print(f"\nInvalid prompt! Please select (1) to reveal the archive.")
        else:
            print(f"\nInvalid prompt! Please select (1) to reveal the archive.")
    elif len(year_list) > 1:
        choice = input(f"Please select (1-{len(year_list)}) to reveal the archive: ")
        if choice.isdigit():
            idx_year = int(choice) - 1
            if 0<= idx_year < len(year_list):
                selected_year = year_list[idx_year]
                print()
                print(f"-"*60)
                print(f"{selected_year:^60}")
                print(f"-"*60)
                print(f"1. Test 1")
                print(f"2. Test 2")
                print(f"3. Final")
                print(f"-"*60)
                choice_2 = input(f"Please select (1-3): ")
                if choice_2.isdigit():
                    idx_test = int(choice_2) - 1
                    if 0<= idx_test < 3:
                        test_list = list(student_archive[selected_year]["results"].keys())
                        selected_test = student_archive[selected_year]["results"][test_list[idx_test]]# Test_1 dictionary
                        excluded_name = {'class_average','total_student','top_student'}
                        actual_students = {k:v for k,v in selected_test.items() if k not in excluded_name}
                        if actual_students:
                            print()
                            print(f"-"*60)
                            print(f"{test_list[idx_test]:^60}")
                            print(f"{selected_year:^60}")
                            print(f"-"*60)
                            print(f"{'No.':<5}{'Student name':<20}{'Average score':^17}{'Grade':^9}")
                            print(f"-"*60)
                            total_marks = 0
                            top_student = ""
                            highest_avg = -1.0
                            for counter, (name,info) in enumerate(actual_students.items(),start = 1):
                                avg = info.get("Average",0.0)
                                grade = info.get("Grade","")
                                print(f"{counter:<5}{name:<20}{avg:^17}{grade:^9}")

                                total_marks += avg
                                if avg>highest_avg:
                                    highest_avg = avg
                                    top_student = name
                            class_avg = total_marks / len(actual_students) if actual_students else 0.0
                            print(f"-"*60)
                            print(f"Total student : {len(actual_students)}")
                            print(f"Class average : {class_avg:.2f}")
                            print(f"Top student   : {top_student} with {highest_avg:.2f} average mark")
                            print()
                        else:
                            print(f"\nNo historical data for {test_list[idx_test]}")
                    else:
                        print(f"\nInvalid prompt! Please select from (1-3).")
                else:
                    print(f"\nInvalid prompt! Please select from (1-3).")
            else:
                print(f"\nInvalid prompt! Please select from (1-3).")
        else:
            print(f"\nInvalid prompt! Please select (1-{len(year_list)}) to reveal the archive.")
    else:
        print(f"\nNo historical data to be displayed.")
def main():
    load_data()
    while True:
        print(f"="*90)
        print(f"{'Student Grade Program (CLI)':^90}")
        print(f"{current_year:^90}")
        print(f"="*90)
        print(f"1. Add or update student scores")
        print(f"2. View individual student report")
        print(f"3. View class performance summary")
        print(f"4. View subject rankings")
        print(f"5. Reveal archive")
        print(f"6. Exit")
        print(f"-"*90)
        choice = input(f"Please select from (1-6): ")
        if choice.isdigit():
            if choice == '6':
                print(f"\nThank you for using this program!")
                save_data()
                break
            elif choice == '1':
                option_1()
                print()
            elif choice == '2':
                option_2()
                print()
            elif choice == '3':
                option_3()
                print()
            elif choice == '4':
                option_4()
                print()
            elif choice == '5':
                option_5()
                print()
            else:
                print(f"\nInvalid prompt! Please select from (1-5).")
        else:
            print(f"\nInvalid prompt! Please select from (1-5).")
            continue

if __name__ == "__main__":
    main()


# In[ ]:




