from app.services.database import engine
from sqlalchemy import text
conn=engine.connect()
conn.execute(text('DROP TABLE IF EXISTS user_profiles CASCADE'))
conn.commit()
conn.close()
from app.services.database import init_db
init_db()
print('Done')