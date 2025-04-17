from app import app, db

# only run ONCE when creating the tables for the first time
with app.app_context():
    # db.drop_all()
    db.create_all()
    print("Database created !")