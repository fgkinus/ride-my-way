from db.utils import Database
import run

# initialise the database object
app = run.app
Database = Database(username=app.config['DATABASE_USER'], password=app.config['DATABASE_PASSWORD'],
                    db_name=app.config['DATABASE_NAME']).init_db()
