import os
from slack_latex import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 4390)))

