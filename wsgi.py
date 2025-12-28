import os
from app import create_app, db

# --------------- Create App
app = create_app(os.environ.get("PRODUCTION_CONFIG"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
