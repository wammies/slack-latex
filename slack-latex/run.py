import os
from bot import app


app.run(host='0.0.0.0', port=int(os.getenv('PORT', 4390)))
