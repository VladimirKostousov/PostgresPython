import psycopg2


with open('passwords.txt', encoding='utf-8') as file:
    password = file.readline().strip()
    file.close()


def delete_table(cur, table_name):
    """Function for delete table"""
    cur.execute(f'''
        DROP TABLE {table_name} CASCADE;
        ''')
    conn.commit()
    return print(f'{table_name} deleted')


def create_db(cur):
    """Function for creating new tables in database"""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        clients_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        surname VARCHAR(80),
        email VARCHAR(80) UNIQUE);
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS telephone_number(
        number_id SERIAL PRIMARY KEY,
        clients_id INTEGER REFERENCES Clients(Clients_id),
        number BIGINT UNIQUE);
        ''')
    conn.commit()
    return print('Database created')


def add_new_phone(cur, clients_id=int, number=int):
    """Function for adding new telephone number"""
    cur.execute('''
        INSERT INTO telephone_number(clients_id, number)
        VALUES(%s, %s);
        ''', (clients_id, number))
    conn.commit()
    return print(f'User {clients_id} added his {number}')


def add_new_client(cur, name: str, surname: str, email, number=None):
    """Function for adding new client"""
    cur.execute('''
        INSERT INTO clients(name, surname, email)
        VALUES(%s, %s, %s);
        ''', (name, surname, email))
    cur.execute('''
        SELECT clients_id FROM clients
        ORDER BY clients_id DESC
        LIMIT 1;
        ''')
    conn.commit()
    clients_id = cur.fetchone()[0]
    if number is None:
        return print('Telephone number is not a decree')
    else:
        add_new_phone(cur, clients_id, number)
        return print(f'User {clients_id} added {number}')


def delete_phone(cur, number: int):
    """Function for delete telephone number"""
    cur.execute('''
        DELETE FROM telephone_number
        WHERE number = %s;
        ''', (number, ))
    conn.commit()
    return print(f'{number} deleted')


def delete_client(cur, clients_id: int):
    """Function for delete client"""
    cur.execute(f'''
        SELECT clients_id FROM clients WHERE clients_id = {clients_id};''')
    cur.execute(f'''
        DELETE FROM telephone_number WHERE clients_id = {clients_id};''')
    cur.execute(f'''
        DELETE FROM clients WHERE clients_id = {clients_id};''')
    conn.commit()
    return print(f'{clients_id} deleted')


def update_client(cur, clients_id, name=None, surname=None, email=None, number=None):
    """Function for update information about client"""
    cur.execute('''
        UPDATE clients SET name = %s, surname = %s, email = %s
        WHERE clients_id = %s; 
        ''', (name, surname, email, clients_id))
    cur.execute('''
        SELECT * FROM clients;
        ''')
    cur.execute('''
        UPDATE telephone_number SET number = %s
        WHERE clients_id = %s;
        ''', (number, clients_id))
    cur.execute('''
        SELECT * FROM telephone_number;
        ''')
    conn.commit()
    return print(f'{clients_id} was successfully update')


def find_client(cur, name=None, surname=None, email=None, number=None):
    """Function for finding client"""
    cur.execute('''
        SELECT * FROM clients c JOIN telephone_number tp USING(clients_id)
        WHERE name = %s OR surname = %s
        OR email = %s OR tp.number = %s;
        ''', (name, surname, email, number))
    conn.commit()
    print(cur.fetchall())


conn = psycopg2.connect(database='netologyDB', user='postgres', password=password)
with conn.cursor() as cur:
    delete_table(cur, 'clients')
    delete_table(cur, 'telephone_number')
    create_db(cur)
    add_new_client(cur, 'Ivan', 'Ivanov', 'ivanov@yandex.ru')
    add_new_client(cur, 'Alex', 'Alexandrov', 'alexandrov25@yandex.ru', '98989898')
    add_new_client(cur, 'Sidor', 'Sidorov', 'sidorov@yandex.ru', '123456789')
    add_new_phone(cur, 2, 2222222)
    add_new_phone(cur, 1 , 1111111)
    update_client(cur, clients_id=3, surname='Snow')
    delete_phone(cur, number=1111111)
    add_new_phone(cur, 1, 4444444)
    delete_client(cur, clients_id=3)
    find_client(cur, number=2222222)
    find_client(cur, name='Ivan', surname='Ivanov')
conn.close()