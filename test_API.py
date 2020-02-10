
import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, Program, Section, Activity, init_app

# All endpoints have been tested on Postman

class FlaskTests(unittest.TestCase):
    def setUp(self):

        # create a test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def test_all_programs(self):
        """Test POST request for all programs"""
        result = self.client.post("/program",data =
                                        {"all_programs_key": [
                                        {
                                          "description": "hi",
                                          "id": 1,
                                          "name": "Linh",
                                          "sections": []
                                        },
                                       {
                                          "description": "1st program description",
                                          "id": 2,
                                          "name": "1st program from SeHwan",
                                          "sections": []
                                        },
                                        {
                                          "description": "2nd program description",
                                          "id": 3,
                                          "name": "2nd program from SeHwan",
                                          "sections": []
                                        },
                                        {
                                          "description": "3rd program description",
                                          "id": 4,
                                          "name": "3rd program from SeHwan",
                                          "sections": []
                                        },
                                        {
                                          "description": "helll yeah!!!",
                                          "id": 5,
                                          "name": "haha finally working",
                                          "sections": [
                                            "Section POST REQUEST",
                                            "Section POST REQUEST2",
                                            "Section POST REQUEST3",
                                            "Section POST REQUEST4",
                                            "Section POST REQUEST 5"
                                          ]
                                        },
                                        {
                                          "description": "please work",
                                          "id": 6,
                                          "name": "this is name",
                                          "sections": []
                                        }
                                      ]
                                    })

        self.assertEqual(result.status_code, 200)
        self.assertIN(b'Woah! Working', result.data)


    def test_program(self):
        """Test POST request for one program"""
      
        result = self.client.post('/program/Linh', data={
                                        "description": "hi",
                                        "id": 1,
                                        "name": "Linh",
                                        "sections": []
                                        })
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Woah! Working', result.data)

    def test_one_section(self):
        """Test POST request for one section in one program"""

        result = self.client.post('/program/Linh/section', data ={
                                            "section_name": "section_1_name",
                                            "description": "section_1_detail",
                                            "overview_Image_url": "http://awesome.io",
                                            "activities": []
                                            })


        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Woah! Working', result.data)

    def test_activity(self):
        """Test POST request for all activity for one section in one program"""

        result = self.client.post('/program/Linh/section/section_1_name/activity', data={
                                                                            "all_activities_key": []
                                                                             })
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Woah! Working', result.data)







init_app()
if __name__ == "__main__":
    
    unittest.main()       
    # init_app()

