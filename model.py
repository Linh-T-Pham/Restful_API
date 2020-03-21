from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

# ORM: Object relational mappers. I used classes to model object which 
# were stored in a database. A table is more or less equivalent 
# to a class definition.Each coumn can be thought as of an attribute
# or property of that class. Each row is also analogous to an instantiation 
# of the class. The analogy allow us to constuct software through self-
# examination, can automatically write and execute SQL queries for us
# without the programmer having to stop and think about the SQL required
# to accomplish a task. The ORM helps to avoid to write significant 
# amount of repetitive code. Insted of writing a lot of code to handle
# SQL, it peeks at the class definition and uses the information 
# gathered to generate appropriate SQL 

class Program(db.Model):
    """Program. A program has many sections."""
   
    # Create programs table 
    __tablename__ = 'programs'

    program_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    program_name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printing"""
        #If you define this method on a class, when Python tries to “represent” an instance of this class 

        return f'<Program program_id={self.program_id} \
                program_name={self.program_name} \
                description={self.description}>'

class Section(db.Model):
    """Section. A sector has many activities"""
    
    # Create sections table 
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'))
    section_name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    overview_Image_url= db.Column(db.String(100), default=None, nullable=True) 
    # Nullable#That tells SQLAlchemy (and thus, PostgreSQL) that this column is optional
    

    # I think there is no need for order_index because sector_id is autoincrement
    # order_index = db.Colum(db.Integer)   
    
    program = db.relationship('Program', backref='sections')


    def __repr__(self):
        """Provide helpful representation when printing"""

        return f'<Section section_id={self.section_id}\
                    program_id={self.program_id} \
                    section_name={self.section_name}\
                    description={self.description}\
                    overview_Image_URL={self.overview_Image_URL}\
                    image_url={self.image_url}>'


class Activity(db.Model):
    """Activity."""

    # Create activities table 
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'))
    html_content = db.Column(db.String(200), unique = True)
    question = db.Column(db.String(300), unique = True)
    multiple_choice_answers = db.Column(db.String(200), unique=True)
    right_answer = db.Column(db.String(200), unique=True)
    section = db.relationship('Section', backref='activities')

    def __repr__(self):
        """Provide helpful representation when printing"""

        return f'<Activity activity_id={self.activity_id}\
                    section_id={self.section_id}\
                    question={self.question}\
                    multiple_choice_answers={self.multiple_choice_answers}\
                    html_content = {self.html_content}\
                    right_answer={self.right_answer}>'

        
#################################################
#Helper Functions 

def connect_to_db(app):
    """Connect the database to the Flask app"""
    # Configure to use the Postgres SQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dbprograms'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    

if __name__ == "__main__":
    # As a convenience, if you run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")

###########################################
#Helper function for testing

def init_app():
    from flask import Flask
    app = Flask(__name__)


    # connect_to_db(app, 'postgresql:///testdb')
    # print('Connected to DB.')

