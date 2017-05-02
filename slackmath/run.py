import os
from bot import app


port = int(os.getenv('PORT', 4390))
print(port)
app.run(port=port)
