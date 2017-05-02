import os
from bot import app


app.run(port=os.getenv('PORT', 4390))
