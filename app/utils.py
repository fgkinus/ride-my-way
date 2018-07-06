# initialise the database object
import run
from db.utils import Database

app = run.app
Database = Database(username=app.config['DATABASE_USER'], password=app.config['DATABASE_PASSWORD'],
                    db_name=app.config['DATABASE_NAME'], url=app.config['DATABASE_URL']).init_db()
