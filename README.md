# slack_latex
A Latex-rendering app for Slack.

![screenshot of slack_latex in Slack](https://raw.githubusercontent.com/wammies/slack_latex/master/screenshot.png)

## Features

- Send Slack messages with rendered latex code using a slash command
- Preview your messages before making them public
- Edit your messages

## Installation

slack_latex is a Slack app, and needs a server to run on. It can be run easily on your machine using a tool like [ngrok](https://www.ngrok.com), or on a PaaS such as [Heroku](https://www.heroku.com).

### Running locally with ngrok

1. Download the source, navigate into the parent `slack_latex` directory and run
```bash
pip install .
```
2. Download and install [ngrok](https://ngrok.com/download) and run
```bash
ngrok http 4390
```
3. Make note of the forwarding url ngrok gives you - you will need it when you're adding the app to Slack.
4. Complete the steps in the section below to add the app to Slack.
5. Once you have added the app to Slack, export the token and verification token you received from Slack as environment variables:
```bash
export $SLACK_TOKEN=[token]
export $VERIFICATION_TOKEN=[verification token]
```
6. Run the app with
```bash
python slack_latex/run.py
```
Note: the files `Procfile` and `runtime.txt` are only needed for running on Heroku. If you are not using Heroku, you do not need these files.

### Running on Heroku

1. Set up a (free) Heroku account, and [install the Heroku cli](https://devcenter.heroku.com/articles/heroku-cli). Follow the instructions to login to your Heroku account from the cli.
2. Navigate into the parent `slack_latex` directory, and run
```bash
heroku create
git push heroku master
```
3. Make a note of the url Heroku gives you - you will need it when you're adding the app to Slack. You can find the url by running
```bash
heroku open
```
4. Complete the steps in the section below to add the app to Slack.
5. Once you have added the app to Slack, you'll need to configure Heroku with the token and verification token you received from Slack:
```bash
heroku config:set SLACK_TOKEN=[token]
heroku config:set VERIFICATION_TOKEN=[verification token]
```
### Adding to Slack

1. From your Slack team, navigate to the Apps and Integrations page -> Build -> Your Apps.
2. Create a new app, and fill out the relevant information. Under Basic Information, you will find the verification token for your app. This is the token you should use for the `$VERIFICATION_TOKEN` variable.
3. Visit the Interactive Messages section, and under Request URL enter `[your url]/button`, where `[your url]` is the url you were given by ngrok or Heroku.
4. Visit the Slash Commands section, and add two new commands. Name the first `/latex`, and under Request URL enter `[your url]/latex`. Name the other `/latexedit`, and under Request URL enter `[your url]/latexedit`.
5. Visit the [Slack legacy token](https://api.slack.com/custom-integrations/legacy-tokens) page, and obtain a token. This is the token you should use for the `$SLACK_TOKEN` variable.

## Usage

To post a Latex message, use the command `/latex [latex code]`. The Latex code need not contain `$ ... $` or `\( ... \)`. You will then be shown a preview of your message; from there you can either make the message public or edit the message. To edit the message, press the edit button and then use the command `/latexedit [latex code]`.
