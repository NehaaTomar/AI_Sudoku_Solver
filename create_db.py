# backend/create_db.py

from app import db
from app import Score  # Make sure Score model is imported or already in app.py

db.create_all()
print("✅ Database created with updated schema!")
