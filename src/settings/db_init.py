import sqlite3
import datetime

def monthly_init_db():
    conn = sqlite3.connect(f'db/year-{datetime.datetime.now().year}.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS month{datetime.datetime.now().month}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post TEXT NOT NULL,
            name TEXT NOT NULL,
            begining TEXT NOT NULL,
            finish TEXT,
            zakr TEXT NOT NULL
            )
    """)
    conn.commit()
    # conn.close()


async def add_to_monthly_db(post:str, name:str, zakr:str, finish:str = None, begining:str = None):
    conn = sqlite3.connect(f'db/year-{datetime.datetime.now().year}.db')
    monthly_init_db()
    cursor = conn.cursor()
    if begining != None and finish == None:
        cursor.execute(f'SELECT * FROM month{datetime.datetime.now().month}')
        itog = cursor.fetchall()
        for i in itog:
            if i[5] == "False" and i[2] == f'{name}':
                return "У вас уже есть открытая смена"  
        cursor.execute(f'INSERT INTO month{datetime.datetime.now().month} (post, name, begining, finish, zakr) VALUES (?,?,?,?,?)', (post, name, begining, finish, zakr))
        conn.commit()
        conn.close()
        return "Смена успешно открыта"
    elif finish != None and begining == None:
        cursor.execute(f'SELECT * FROM month{datetime.datetime.now().month}')
        itog = cursor.fetchall()
        print(itog)
        for t in itog:
            if t[5] == "False" and t[2] == f'{name}':
                cursor.execute(f'UPDATE month{datetime.datetime.now().month} SET finish = ? WHERE id = ? ', (finish, t[0]) )
                cursor.execute(f'UPDATE month{datetime.datetime.now().month} SET zakr = ? WHERE id = ? ', (zakr, t[0]) )
                conn.commit()
                conn.close()
                return "Смена успешно закрыта"
        else:
            return "У вас нет открытой смены"
            
def beg_and_fin():
    conn = sqlite3.connect(f'db/year-{datetime.datetime.now().year}.db')
    monthly_init_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM month{datetime.datetime.now().month - 1}')
    prev_month = cursor.fetchall()
    print(prev_month)
    to_new_month = []
    for i in prev_month:
        if i[5] == "False":
            to_new_month.append(i)
            cursor.execute(f'UPDATE month{datetime.datetime.now().month-1} SET zakr = ? WHERE id = ? ', ("TRUE", i[0]) )
            cursor.execute(f'UPDATE month{datetime.datetime.now().month-1} SET finish = ? WHERE id = ? ', (datetime.datetime.now(), i[0]) )
            conn.commit()
        else:
            continue
    print(to_new_month)
    for i in to_new_month:
        cursor.execute(f'INSERT INTO month{datetime.datetime.now().month} (post, name, begining, finish, zakr) VALUES (?,?,?,?,?)', (i[1],i[2],i[3],i[4],i[5]) )
        conn.commit()
    conn.close()




