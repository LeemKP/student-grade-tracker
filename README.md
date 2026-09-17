# Student grade tracker
A lightweight CLI student gradebook and performance analyzer written in Python. Stores all data locally on your machine in a `.json` file.

For your information, this python script is a personal mini project done by the author. It is not recognized by any school, university or government sector. 

---

## Prerequisites: Installing Python
Ensure you have Python 3 installed on your machine before running the application.

### Windows
Install Python via the Windows Package Manager directly from PowerShell:
```powershell
#To search available python to be installed
winget search Python.Python

#To install the selected python, Eg: Python version 3.14 is selected to be installed
winget install Python.Python.3.14
```
After python successfully installed, close the PowerShell and reopen it. This is to refresh the PowerShell.

### Linux / Ubuntu (via Mamba)
If you are working in an Ubuntu or WSL environment using Mamba, you can install Python with the following coding:
```bash
#To search available python to be installed
mamba search python

#To install selected python, Eg: Python version 3.14.7
mamba install python=3.14.7
#Take note that you must not have any spacing for ('python=3.14.7').
```

### MacOS
Unfortunately, the author does not have any experience with MacOS 🥲. But as long as python is installed in the machine, this expenses_tracker.py will be able to work.

---

## How to Run
1. Download the student_grade.py file from this repository.
2. Open your machine's terminal (PowerShell/Ubuntu/so on).
3. Navigate to the folder containing `student_grade.py`.
4. Copy the path of the folder and paste it in your terminal like this.

Windows (PowerShell)
```powershell
#For example, I saved `student_grade.py` in Downloads.
cd C:\Users\User\Downloads
```
Ubuntu/WSL:
```bash
#For example, I saved `student_grade.py` in Downloads.
cd /mnt/c/Users/User/Downloads 

#Or I saved `student_grade.py` in mamba's environment.
cd path
```
5. Launch the script:

Windows (PowerShell)
```powershell
python student_grade.py
#OR using the Windows launcher:
py student_grade.py
```
Ubuntu/WSL:
```bash
python student_grade.py
```

---

## Features
* **Student & Subject Management:** Add or remove students and subjects dynamically.
* **Score Tracking:** Input marks across multiple terms (Test 1, Test 2, and Final exams).
* **Automated Statistics:** Calculates individual averages, letter grades (A+ to Fail) and overall class averages.
* **Performance Insights:** Identifies top performers, subject rankings and students requiring improvement per subject.
* **Yearly Archiving:** Persists data locally via `students.json` and automatically archives historical records when the calendar yeara advances.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
