import requests
import pytest 
from server.py import app

# Required to use Flask sessions and the debug toolbar

url = 'http://0.0.0.0:5000'

@app.route('/program', methods=['GET'])
def test_program():
    response = jsonify({
  "all_programs_key": [
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
    response.status_code = 200
    return response 
