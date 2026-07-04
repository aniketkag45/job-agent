
from app.services.database import engine
from sqlalchemy import text

conn = engine.connect()

# Add columns (IF NOT EXISTS pattern not supported in PG 10+, use try/except)
for col, col_type in [('scraped_at', 'VARCHAR(50)'), ('applied_at', 'VARCHAR(50)')]:
    try:
        conn.execute(text(f'ALTER TABLE jobs ADD COLUMN {col} {col_type}'))
        print(f'Added column: {col}')
    except Exception as e:
        if 'already exists' in str(e):
            print(f'Column {col} already exists — skipping')
        else:
            print(f'Error adding {col}: {e}')

conn.commit()
conn.close()
print('Done. Columns added to jobs table.')