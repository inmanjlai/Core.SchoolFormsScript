import os
import csv
from flask import Flask

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def all():
    exceptions = {
        "Previous School's Test Scores": ['4'],
        "Kindergarten Waiver": ['K', 'Full Day K', "Y5's", '4K'],
        "Initial Immunization Records": ['K', '7', '9'],
        "Vision Screening": ['K'],
        "ATS Kindergarten Registration": ['K'],
        "MS/HS Transcripts (Incoming Students Only)": ['7', '8', '9', '10', '11', '12'],
        "MS/HS Transcript (Incoming Students Only)": ['7', '8', '9', '10', '11', '12'],
        "MS/HS Course Request Form (Incoming Students Only)": ['9'],
        "Specialized Learning (MS/HS only)": ['6', '7', '8', '9', '10', '11', '12'],
        "Specialized Learning": ['6', '7', '8', '9', '10', '11', '12'],
        "Student Assessment/Screening": ['1', '2', '3', '4', '5', '6', '7', '8']
    }

    path_name = os.getcwd()

    files = []
    CI_formatted_data = {}
    QA_formatted_data = {}

    file_names = os.listdir(path_name)
    for file_name in file_names:
        if file_name.endswith('.csv'):
            files.append(file_name)

    for file in files:
        fileOpen = open(os.path.join(path_name, file), "r")
        reader = csv.reader(fileOpen, delimiter=',')
        if file.startswith('CI'):
            for row in reader:
                schoolName = row[14]
                gradeLevel = row[16]
                form = row[21]
                if schoolName in CI_formatted_data:
                    if gradeLevel in CI_formatted_data[schoolName]:
                        CI_formatted_data[schoolName][gradeLevel].append(form)
                    else:
                        CI_formatted_data[schoolName][gradeLevel] = [form]
                else:
                    CI_formatted_data[schoolName] = {gradeLevel: [form]}
        else:
            for row in reader:
                schoolName = row[13]
                form = row[17]
                if schoolName in QA_formatted_data:
                    QA_formatted_data[schoolName].append(form)
                else:
                    QA_formatted_data[schoolName] = [form]

    missing_forms = {}

    for school in CI_formatted_data:
        ci_school_forms = CI_formatted_data[school]
        if school == 'Queens Grant Community School':
            school = "Queen's Grant Community School"

        for gradeLevel in ci_school_forms:
            for form in QA_formatted_data[school]:
                if form == 'Specialized Learning (MS/HS only)':
                    form = 'Specialized Learning'
                # IF FORM IS MISSING
                if form not in ci_school_forms[gradeLevel]:
                    # CHECK IF THIS IS AN EXCEPTION FORM
                    if form in exceptions:
                        # CHECK IF THIS GRADE LEVEL IS IN THE EXCEPTION FORMS GRADE LEVEL LIST
                        # IF IT ISN'T, ADD IT TO THE LIST OF MISSING FORMS
                        if gradeLevel in exceptions[form]:
                            if school in missing_forms:
                                if gradeLevel in missing_forms[school]:
                                    missing_forms[school][gradeLevel].append(form)
                                else:
                                    missing_forms[school][gradeLevel] = [form]
                            else: 
                                missing_forms[school] = {gradeLevel: [form]}                            
                    else:
                        if school in missing_forms:
                            if gradeLevel in missing_forms[school]:
                                missing_forms[school][gradeLevel].append(form)
                            else:
                                missing_forms[school][gradeLevel] = [form]
                        else: 
                            missing_forms[school] = {gradeLevel: [form]}
            
    return {"Missing Forms": missing_forms}

@app.route('/ci')
def CI():
    path_name = os.getcwd()

    files = []
    CI_formatted_data = {}

    file_names = os.listdir(path_name)
    for file_name in file_names:
        if file_name.endswith('.csv'):
            files.append(file_name)

    for file in files:
        fileOpen = open(os.path.join(path_name, file), "r")
        reader = csv.reader(fileOpen, delimiter=',')
        if file.startswith('CI'):
            for row in reader:
                schoolName = row[14]
                gradeLevel = row[16]
                form = row[21]
                if schoolName in CI_formatted_data:
                    if gradeLevel in CI_formatted_data[schoolName]:
                        CI_formatted_data[schoolName][gradeLevel].append(form)
                    else:
                        CI_formatted_data[schoolName][gradeLevel] = [form]
                else:
                    CI_formatted_data[schoolName] = {gradeLevel: [form]}

    return CI_formatted_data
    
@app.route('/qa')
def QA():
    path_name = os.getcwd()

    files = []
    QA_formatted_data = {}

    file_names = os.listdir(path_name)
    for file_name in file_names:
        if file_name.endswith('.csv'):
            files.append(file_name)

    for file in files:
        fileOpen = open(os.path.join(path_name, file), "r")
        reader = csv.reader(fileOpen, delimiter=',')
        if file.startswith('QA'):
            for row in reader:
                schoolName = row[13]
                form = row[17]
                if schoolName in QA_formatted_data:
                    QA_formatted_data[schoolName].append(form)
                else:
                    QA_formatted_data[schoolName] = [form]

    return QA_formatted_data

