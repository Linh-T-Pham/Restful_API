from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Program, Section, Activity
import os 

app = Flask(__name__)

# ****program*****

def serialize_program(program):
    print('\n\n\n\t\t INSIDE SERIALIZE\n\n\n')
    program_dict = {
        'id': program.program_id,
        'name': program.program_name,
        'description': program.description,
        'sections': [],
    }

    for section in program.sections:
        program_dict['sections'].append(section.section_name)

    return program_dict


# GET /program
@app.route('/program')
def get_programs():
    """Get method for all the programs"""
    all_programs = Program.query.all()
    result = []
    for program in all_programs:
        program_dict = serialize_program(program)
        result.append(program_dict)
    return jsonify({ 'all_programs_key': result })

# POST /program data
@app.route('/program', methods=['POST'])
def create_programs():
    # Make request to /program endpoint 
    request_data = request.get_json()
    program_name =  request_data['program_name']
    description = request_data['description']
    new_program = Program(
                    program_name = program_name, 
                    description = description
                    )

    db.session.add(new_program)
    db.session.commit()
    program_dict = serialize_program(new_program)
    return jsonify(program_dict)


# GET /program/<string:name>
@app.route('/program/<string:program_name>')
def get_program(program_name):
    """Get method for one program"""
    program = Program.query.filter_by(program_name=program_name).first()
    print(f'\n\n\n\t\t"""""\n{program}\n""""""\n\n\n')
    if program is not None:
        program_dict = serialize_program(program)
        return jsonify(program_dict)
    else:
        return 'Can not find the program', 404


# ****Section********

# Still fixing the codes 

def serialize_program(section):
    section_dict = {
        'id': section.section_id,
        'name': section.section_name,
        'description': section.description,
        'overview_Image_URL': request_data['overview_Image_URL']
        'activity': [],
        }
    for activity in 
    return section_dict


@app.route('/program/<string:program_name>/section', methods=['POST'])
def create_sector_in_program(program_name):
    request_data = request_data.get_json()
    for program in programs:
        if program['program_name'] == program_name:
            new_section = {
                'section_name': request_data['section_name'],
                'description': request_data['description'],
                'overview_Image_URL': request_data['overview_Image_URL'],
                'activity': []
            }

            program['section'].apppend(new_section)
            # db.session.add(new_section)
            # db.session.commit()
            return jsonify(new_section)
    return jsonify({'message': 'program not found'})



# GET /program/<string:name>/section
@app.route('/program/<string:program_name>/section/<string:section_name>')
def get_sector_in_program(program_name, section_name):
    for program in programs:
        if program['program_name'] == program_name:
            for section in program['sections']:
                if section['section_name'] == section_name: 
                    return jsonify({'sections':program['sections']})
    return jsonify({'message':'Can not find the program'})


# POST /program/<string:name>/section/activity
@app.route('/program/<string:program_name>/section/<string:section_name>/activity', methods=['POST'])
def create_activity_in_sector(program_name, section_name):
    request_data = request_data.get_json()
    for program in programs:
        if program['program_name'] == program_name:
            for section in program['section']:
                if section['activity'] == activity:
                    new_activity = {
                    'html_content': request_data['html_content'],
                    'question': request_data['question'],
                    'multiple_choice_answers': request_data['multiple_choice_answers'],
                    'right_answer': request_data['right_answer']
                    }          
                    section['activity'].append(new_activity)
                    # db.session.add(new_activity)
                    # db.session.commit()
                    return jsonify(new_activity)
    return jsonify({'message': 'can not be found'})


# GET /program/<string:name>/section/activity
@app.route('/program/<string:program_name>/section/<string:section_name>/activity')
def get_activity_in_sector(program_name, section_name):
    for program in programs:
        if program['program_name'] == program_name:
            for section in program['sections']:
                if section['section_name'] == section_name:  
                    # I can pass activities list to jinja later and display 
                    #either question or html content on the front end        
                    return jsonify({'activities': section['activities']})
    return jsonify({'message':'Can not find the activity'})












if __name__ == "__main__":

 
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")