from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Program, Section, Activity
import os 

app = Flask(__name__)

# ****Program*****

def serialize_program(program):
    # print('\n\n\n\t\t INSIDE SERIALIZE\n\n\n')
    """Helper function"""
    program_dict = {
        'id': program.program_id,
        'program_name': program.program_name,
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

# POST /program
@app.route('/program', methods=['POST'])
def create_programs():
    """ Make request to /program endpoint"""
    request_data = request.get_json()
    program_name = request_data['program_name']
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
    # print(f'\n\n\n\t\t"""""\n{program}\n""""""\n\n\n')
    if program is not None:
        program_dict = serialize_program(program)
        return jsonify(program_dict)
    else:
        return 'Can not find the program', 404

# DELETE /program/<string:name>
@app.route('/program/<string:program_name>', methods=['DELETE'])
def delete_program(program_name):
    delete_program = Program.query.filter_by(program_name=program_name).first()
    db.session.delete(delete_program)
    db.session.commit()
    return 'Deleted', 200

# ****Section********

def serialize_section(section):
    """Helper Function"""
    section_dict = {
        'id': section.section_id,
        'name': section.section_name,
        'description': section.description,
        'overview_Image_url': section.overview_Image_url,
        'activities': [],
        }
    for activity in section.activities:
        section_dict['activities'].append(section.serialize_activity(activity))

    return section_dict

def serialize_activity(activity):
    """Helper Function"""
    activity_dict = {
        'html_content': activity.html_content,
        'question': activity.question,
        'multiple_choice_answers': activity.multiple_choice_answers,
        'right_answer': activity.right_answer,
        }

    return activity_dict

# GET /program/<string:name>/section
@app.route('/program/<string:program_name>/section')
def get_sections_in_program(program_name):
    """Get method for all the sections in a program"""
    program = Program.query.filter_by(program_name=program_name).first()
    if program is not None:
        sections = Section.query.filter_by(program_id=program.program_id)
        # print(f'\n\n\n\t\t"""""\n{sections}\n""""""\n\n\n')
        all_sections = []
        for each_section in sections:
            section_dict = serialize_section(each_section)
            all_sections.append(section_dict)
        return jsonify({'all_sections': all_sections})
    else:
        return 'Can not find the program', 404

# GET /program/<string:name>/section/<string:section_name>
@app.route('/program/<string:program_name>/section/<string:section_name>')
def get_section_in_program(program_name, section_name):
    """Get method for one section in a program"""
    section = Section.query.filter_by(section_name=section_name).first()
    if section is not None:
        return jsonify(serialize_section(section))
    else:
        return 'Cannot find the section', 404

# POST /program/<string:name>/section/<string:section_name>
@app.route('/program/<string:program_name>/section', methods=['POST'])
def create_section_in_program(program_name):
    """ Make request to section endpoint """
    program = Program.query.filter_by(program_name=program_name).first()
    # print(f'\n\n\n\t\t{program} \n\n\n')

    if program is not None:
        request_data = request.get_json()
        section_name = request_data['section_name']
        description = request_data['description']
        overview_Image_url = request_data['overview_Image_url']
        new_section = Section(
                        program_id = program.program_id,
                        section_name = section_name,
                        description = description,
                        overview_Image_url = overview_Image_url
                        )

        db.session.add(new_section)
        db.session.commit()
        return jsonify(serialize_section(new_section))
    else:
        return 'Cannot find the program', 404 

# DELETE /program/<string:program_name>/section
@app.route('/program/<string:program_name>/section', methods=['DELETE'])
def delete_sections_in_program(program_name):
    """Delete all sections in one program"""
    program = Program.query.filter_by(program_name=program_name).first()
    if program is not None:
        delete_all_sections = Section.query.filter_by(program_id=program.program_id)
        db.session.delete(delete_all_sections)
        db.session.commit()

        return 'Deleted', 200


# *******Activity*******

# GET /program/<string:name>/section/<string:section_name>/activity
@app.route('/program/<string:program_name>/section/<string:section_name>/activity')
def get_activities_in_section(program_name, section_name):
    """Get method for all activities in section for one program"""
    program = Program.query.filter_by(program_name=program_name).first()
    if program is not None:
        section = Section.query.filter_by(section_name=section_name).first()
        if section is not None: 
            # I can pass activities json to jinja later and display 
            #either question or html content on the front end 
            all_activities = Activity.query.filter_by(section_id=section.section_id)
            activities_list = []
            for each_activity in all_activities:
                activities_dict = serialize_activity(each_activity)
                activities_list.append(activities_dict)     
            return jsonify({ 'all_activities_key': activities_list })
        
        else:
            return 'Can not find', 404
    else:
        return 'Can not find', 404


# POST /program/<string:name>/section/<string:section_name>/activity
@app.route('/program/<string:program_name>/section/<string:section_name>/activity', methods=['POST'])
def create_activity_in_section(program_name, section_name):
    """Make request to activity endpoint"""
    program = Program.query.filter_by(program_name=program_name).first()
    if program is not None: 
        section = Section.query.filter_by(section_name=section_name).first()
        if section is not None: 
            request_data = request_data.get_json()
            html_content = request_data['html_content']
            question = request_data['question']
            multiple_choice_answers = request_data['multiple_choice_answers']
            right_answer = request_data['right_answer']
            new_activity = Activity(
                                    html_content = html_content,
                                    question = question,
                                    multiple_choice_answers = multiple_choice_answers,
                                    right_answer = right_answer
                                    )
               
            db.session.add(new_activity)
            db.session.commit()
            return jsonify(serialize_activity(activity_dict))
        else:
            return 'Can not find the section', 404
    else:
        return 'Can not find the program', 404


# DELETE /program/<string:name>/section/<string:section_name>/activity
@app.route('/program/<string:program_name>/section/<string:section_name>/activity', methods=['DELETE'])
def delete_all_activities(program_name, section_name):
    """Delete all activities"""
    program = Program.query.filter_by(program_name=program_name).first()
    if program is not None:
        section = Section.query.filter_by(section_name=section_name).first()
        if section is not None: 
            delete_all_activities = Activity.query.filter_by(section_id=section.section_id)
            db.session.delete(delete_all_activities)
            db.session.commit()
            return 'Deleted', 200


    









if __name__ == "__main__":

 
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")