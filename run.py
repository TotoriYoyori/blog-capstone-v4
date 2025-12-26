import os
from app import create_app

# --------------- Create App
app = create_app(os.environ.get("DEV_CONFIG") or 'default')

if __name__ == "__main__":
    app.run()
