import os
from bot import app


app.run(port=int(os.getenv('PORT', 4390)))
