import functools
import os

from flask import (
    Blueprint, render_template, abort, current_app
)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

blueprint = Blueprint('views', __name__)

@blueprint.context_processor
def base():
    return {'categories': categories}

@blueprint.route('/')
def home():
    return render_template('home.html')

@blueprint.route('/categories/<category>')
def category(category):
    if category not in categories.keys():
        abort(404)
    clubs = []

    creds = None
    if os.path.exists(current_app.config['TOKEN']):
        creds = Credentials.from_authorized_user_file(current_app.config['TOKEN'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(current_app.config['CREDENTIALS'], ['https://www.googleapis.com/auth/forms.responses.readonly'])
            creds = flow.run_local_server()
        with open(current_app.config['TOKEN'], 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('forms', 'v1', credentials=creds)
        with open(current_app.config['FORM_ID'], 'r') as f:
            print(service.forms().responses().list(formId=f.read()).execute())
    except HttpError as err:
        print(err)

    # TODO: Gather club data
    return render_template('category.html', clubs=clubs, category=category)