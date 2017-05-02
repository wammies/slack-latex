import os
from bot import app


app.run(port=os.environ['PORT'])
