import os
from app import create_app

# --------------- Create App
app = create_app(os.environ.get("PRODUCTION_CONFIG"))

if __name__ == "__main__":
    app.run()
