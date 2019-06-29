from flask import Flask, request, jsonify
from slackclient import SlackClient
import urllib
import os
import requests
import ast


SLACK_TOKEN = os.getenv('SLACK_TOKEN', None)
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN', None)

app = Flask(__name__)
sc = SlackClient(SLACK_TOKEN)

open_messages = {}
base_url = 'http://chart.googleapis.com/chart?cht=tx&chl='

@app.route('/latex', methods=['POST'])
def receive_latex_command():
    if request.form['token'] == VERIFICATION_TOKEN:
        app.logger.info('Command received: /latex\n')
        text = request.form['text']
        app.logger.info('Command text: ' + text + '\n')
        if text == 'help':
            response = jsonify(help_text())
        else:
            response = jsonify(build_response(text))
    else:
        app.logger.info('Command received: bad token\n')
        response = ('error', 403)

    return response

@app.route('/latexedit', methods=['POST'])
def receive_edit_command():
    if request.form['token'] == VERIFICATION_TOKEN:
        app.logger.info('Command received: /latexedit\n')
        text = request.form['text']
        app.logger.info('Command text: ' + text + '\n')
        user = request.form['user_id']
        if user in open_messages.keys():
            url = open_messages[user]['url'].replace('\\', '')
            data = build_response(text)
            requests.post(url, json=data)
            del open_messages[user]
            response = ('', 200)
        else:
            app.logger.info('No open messages for user ' + user + '\n')
            response = {'text': 'You do not have a message open for editing. To use the /latexedit command, you must first have pressed the "Edit" button on a message you have created with the /latex command.'}
            response = jsonify(response)
    else:
        response = ('', 403)

    return response

@app.route('/button', methods=['POST'])
def handle_button():
    data = request.form['payload']
    # convert booleans to start with capital letters so that ast.literal_eval
    # will work properly
    data = data.replace('false', 'False').replace('true', 'True')
    data = ast.literal_eval(data)

    if data['token'] == VERIFICATION_TOKEN:
        button_value = data['actions'][0]['value']
        user = data['user']['id']
        app.logger.info('Button received: ' + button_value + '\n')

        if button_value == 'edit':
            open_messages[user] = {'url': data['response_url'], 'ts': \
                    data['message_ts']}
            response = build_response(data['callback_id'])
            response['text'] = 'Paste this into your chat box and make the desired changes: /latexedit ' + data['callback_id']
            response['replace_original'] = 'true'
            response = jsonify(response)

        elif button_value == 'public':
            response = jsonify({'delete_original': 'true'})
            user_profile = sc.api_call(
                    'users.profile.get',
                    user=data['user']['id']
                    )
            # image_72 seems to be the only size that exists for the default
            # user icons
            icon_url = user_profile['profile']['image_72']
            sc.api_call(
                    'chat.postMessage',
                    channel=data['channel']['id'],
                    attachments=[ { 'fallback': 'image of latex',
                        'image_url': base_url + urllib.parse.quote(\
                                data['callback_id']) } ],
                    username=data['user']['name'],
                    icon_url=icon_url
                    )

            if user in open_messages.keys():
                if open_messages[user]['ts'] == data['message_ts']:
                    del open_messages[user]

        elif button_value == 'delete':
            response = jsonify({'delete_original': 'true'})

            if user in open_messages.keys():
                if open_messages[user]['ts'] == data['message_ts']:
                    del open_messages[user]

        else:
            response = ('', 400)

    else:
        app.logger.info('Button received: bad token\n')
        response = ('', 403)

    return response

def build_response(text):

    response =  {
                    'response_type': 'ephemeral',
                    'attachments': [ {
                        'fallback': 'image of latex',
                        'image_url': base_url + urllib.parse.quote(text),
                        'callback_id': text,
                        'actions': [
                            {
                                'name': 'message_action',
                                'text': 'Edit',
                                'type': 'button',
                                'value': 'edit'
                            },
                            {
                                'name': 'message_action',
                                'text': 'Make Public',
                                'type': 'button',
                                'value': 'public'
                            },
                            {
                                'name': 'message_action',
                                'text': 'Delete',
                                'style': 'danger',
                                'type': 'button',
                                'value': 'delete'
                            }
                        ]
                    } ]
                }

    return response

def help_text():
    response =  {
                    'response_type': 'ephemeral',
                    'text': 'LatexBot allows you to use Latex math typesetting in Slack.\n' +\
                    'Usage: \latex [Latex code]\n' +\
                    'The Latex code doesn\'t need to be surrounded by $ $ or \( \).\n' +\
                    'Example: \latex \int_a^b f(x) dx = c'
                }

    return response

