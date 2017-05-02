import os
from bot import app


app.run(port=os.environ.get('PORT', 4390))
