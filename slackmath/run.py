import os
from bot import app


if __name__ == '__main__':
    port = int(os.getenv('PORT', 4390))
    print(port)
    app.run(host='0.0.0.0', port=port)
