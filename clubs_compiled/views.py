import functools
import os

from flask import (
    Blueprint, render_template, abort, current_app
)

from google.oauth2 import service_account
from googleapiclient.discovery import build

categories = {
    'academic': {
        'name': 'Academic',
        'description': 'Academic Clubs'
    }, 'arts': {
        'name': 'Arts',
        'description': 'Arts Clubs'
    }, 'business': {
        'name': 'Business',
        'description': 'Business Clubs'
    }, 'stem': {
        'name': 'STEM & Technology',
        'description': 'STEM Clubs'
    }, 'health': {
        'name': 'Health & Wellness',
        'description': 'Health Clubs'
    }, 'leadership': {
        'name': 'Community Service & Leadership',
        'description': 'Leadership Clubs'
    }, 'culture': {
        'name': 'Culture & Diversity',
        'description': 'Culture Clubs'
    }, 'sports': {
        'name': 'Sports',
        'description': 'Sports Clubs'
    }, 'honorsocieties': {
        'name': 'Honor Societies',
        'description': 'Honor Societies Clubs'
    }
}

questions = {
    'sponsor_email': '3909c38a',
    'name': '65494c2a',
    'description': '27617192',
    'sponsor': '5604a1cb',
    'category': '3c12dca8',
    'meeting_times': '0d8d7cd2',
    'room_number': '314c7950',
    'president_name': '11ccbcb7',
    'website': '5bca57e6',
    'president_email': '205cfdea',
    'how_to_join': '0ede8215'
}

blueprint = Blueprint('views', __name__)

@blueprint.context_processor
def base():
    return {'categories': categories}

@blueprint.route('/')
def home():
    return render_template('home.html')

@blueprint.route('/categories/<category>')
def category(category):
    clubs = []

    f = open(current_app.config['FORM_ID'], 'r')
    form_id = f.read()
    f.close()

    credentials = service_account.Credentials.from_service_account_file(current_app.config['API_KEY'], scopes=['https://www.googleapis.com/auth/forms.responses.readonly'])
    service = build('forms', 'v1', credentials=credentials)

    request = service.forms().responses().list(formId=form_id)
    responses = request.execute()
    clubs = []
    for response in responses['responses']:
        if categories[category]['name'] in [value['value'] for value in response['answers'][questions['category']]['textAnswers']['answers']]:
            club = {}
            for question, id in questions.items():
                answers = [value['value'] for value in response['answers'][id]['textAnswers']['answers']]
                club[question] = answers if len(answers) > 1 else answers[0]
            clubs.append(club)
            print(club)
    
    print(clubs)

    # TODO: Gather club data
    return render_template('category.html', clubs=clubs, category=category)