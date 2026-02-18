class Config:
    SECRET_KEY = "supersecretkey"
    # SQLite database file in your project folder
    SQLALCHEMY_DATABASE_URI = "sqlite:///shopping.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False