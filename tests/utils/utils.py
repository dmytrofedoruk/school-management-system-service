from app.config import db


def truncate_table(db, table_name):
    with db.transaction() as transaction:
        result = db.execute(
            query=f'''TRUNCATE TABLE {table_name} RESTART IDENTITY CASCASE''')
