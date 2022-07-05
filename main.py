import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import dataclass

load_dotenv()
QUERY_URL = 'https://trackapi.nutritionix.com/v2/natural/exercise'
ADD_ROW = 'https://api.sheety.co/6695f9f435690001de1e27c4d016b1eb/workoutTracker/sheet1'


@dataclass
class Exercise:
    date: str
    time: str
    name: str
    duration: str
    calories: str


def get_workout():
    query = input('Tell me which exercises you did today: ')
    headers = {
        'x-app-id': os.getenv('APP_ID'),
        'x-app-key': os.getenv('API_KEY')
    }
    data = {'query': query}
    response = requests.post(
        url=QUERY_URL,
        headers=headers,
        json=data
    )

    workout = []
    data = response.json()['exercises']
    for entry in data:
        exercise = Exercise(
            date=datetime.today().strftime('%d/%m/%Y'),
            time=datetime.now().strftime('%H:%M:%S'),
            name=entry['name'],
            duration=entry['duration_min'],
            calories=entry['nf_calories']
        )
        workout.append(exercise)

    return workout


def add_row(exercise):
    body = {'sheet1': {
        'date': exercise.date,
        'time': exercise.time,
        'exercise': exercise.name,
        'duration': exercise.duration,
        'calories': exercise.calories,
    }}
    headers = {
        'Authorization': f'Basic {os.getenv("AUTH_HEADER")}'
    }
    requests.post(
        url=ADD_ROW,
        json=body,
        headers=headers
    )


def main():
    workout = get_workout()

    for exercise in workout:
        add_row(exercise)


if __name__ == '__main__':
    main()
