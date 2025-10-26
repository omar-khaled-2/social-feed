from app import create_app
from app.db import db
from app.config import Config
from app.db import Base


app = create_app()

with app.app_context():
    Base.metadata.create_all(db.engine,tables=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=Config.PORT,debug=Config.DEPUG)




