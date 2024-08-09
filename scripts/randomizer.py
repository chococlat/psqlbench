from collections.abc import Iterable
import nltk
import random,os,glob,time,threading
from nltk.corpus import words
from datetime import datetime, timedelta
from faker import Faker
import psycopg2

#nltk.download('words')
fake = Faker()
word_list = words.words()

queue = []

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)
cur = conn.cursor()
def pg_exec(query:str):
    global cur,conn
    cur.execute(query)
    conn.commit()

def gen_timestamp():
    """Generate a random timestamp between start_date and end_date."""
    time_delta = datetime(2089, 11, 3) - datetime(1999, 11, 3)
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    random_timestamp = datetime(1999, 11, 3) + timedelta(seconds=random_seconds)
    return random_timestamp

def gen_token():
    max = 4
    connections = ("of","to","from","in","with","on","for","between")
    string = random.choice(word_list)
    if max>1:        
        for i in range(max-1):
            string += f" {random.choice(connections)} {random.choice(word_list)}"
    return string

def gen_filename():
    max = 2
    connections = ("of","to","from","in","with","on","for","between")
    string = f"{random.choice(word_list)}_{random.choice(connections)}_{random.choice(word_list)}"
    return string + random.choice([".txt",".py",".cpp",".xls",".csv",".js",".exe",".bat",".doc",".png",".jpeg"])

def gen_number_15M():
    return random.randrange(1,15000000)
def gen_number_50M():
    return random.randrange(1,50000000)
def gen_number_500k():
    return random.randrange(1,500000)
def gen_number_100k():
    return random.randrange(1,100000)
def gen_number_50():
    return random.randrange(1,50)

def generate(amount:int,table:str,columns:Iterable,values:Iterable[callable]):
    global queue
    sections_amount = 1
    or_amount = amount
    if amount>500000:
        sections_amount = int(amount/500000)
        amount = amount%500000
    for section in range(sections_amount):
        strlist = []
        query = f"INSERT INTO {table} "
        query += "("
        for column in columns:
            query += f"{column},"
        query = f"{query[:-1]}) VALUES\n"
        strlist.append(query) 
        query=""
        for i in range(amount+1):
            query += "("
            for gen in values:
                query += f"\'{gen()}\',"
            query = f"{query[:-1]})"
            query += ",\n" if i < amount else ";\n"
            
            strlist.append(query)
            query=""
            
            if i%100000 == 0:
                print(f"{table} : section({section+1}/{sections_amount}) - {i}/{amount}")
        amount = 500000
        with open(f"{table}_{section}.sql","w") as oq:
            oq.write(''.join(strlist))
        with open("../INSERT_ALL.sql","a") as q:
            q.write(f"\\i insert/{table}_{section}.sql\n")
    print(f"{table} : {or_amount}/{or_amount}\n")
    
def generate2(amount:int,table:str,columns:Iterable,values:Iterable[callable]):
    global queue
    sections_amount = 1
    or_amount = amount
    if amount>500000:
        sections_amount = int(amount/500000)
        amount = amount%500000
    for section in range(sections_amount):
        strlist = []
        query = f"INSERT INTO {table} "
        query += "("
        for column in columns:
            query += f"{column},"
        query = f"{query[:-1]}) VALUES\n"
        strlist.append(query) 
        query=""
        for i in range(amount+1):
            query += "("
            for gen in values:
                query += f"\'{gen()}\',"
            query = f"{query[:-1]})"
            query += ",\n" if i < amount else ";\n"
            
            strlist.append(query)
            query=""
            
            if i%100000 == 0:
                print(f"{table} : section({section+1}/{sections_amount}) - {i}/{amount}")
        amount = 500000
        queue.insert(0,''.join(strlist))
    print(f"{table} : {or_amount}/{or_amount}\n")
    
def generatelbl(amount:int,table:str,columns:Iterable,values:Iterable[callable]):
    sections_amount = 1
    or_amount = amount
    if amount>500000:
        sections_amount = int(amount/500000)
        amount = amount%500000
    for section in range(sections_amount):
        strlist = []
        for i in range(amount+1):
            query = f"INSERT INTO {table} ("
            for column in columns:
                query += f"{column},"
            query = f"{query[:-1]}) VALUES ("
            for gen in values:
                query += f"\'{gen()}\',"
            query = f"{query[:-1]})"
            query += ";\n"
            
            strlist.append(query)
            query=""
            
            if i%100000 == 0:
                print(f"{table} : section({section+1}/{sections_amount}) - {i}/{amount}")
        amount = 500000
        with open(f"{table}_{section}.sql","w") as oq:
            oq.write(''.join(strlist))
        with open("../INSERT_ALL.sql","a") as q:
            q.write(f"\\i insert/{table}_{section}.sql\n")
    print(f"{table} : {or_amount}/{or_amount}\n")

def consume():
    global queue
    try:
        query = queue.pop()
        pg_exec(query)
        print('Sent')
        print('Queue length: ',len(queue))
    except IndexError:
        pass
    
def consumeloop():
    while True:
        time.sleep(0.3)
        threading.Thread(target=consume).start()


counter = 0
def benchmark_tokens():
    global counter
    while True:
        query = f'INSERT INTO timescale.tokens (token,user_id,created) VALUES (\'{gen_token()}\',\'{gen_number_500k()}\',\'{gen_timestamp()}\')'
        pg_exec(query)
        counter+=1
        
        
        

        
        
    
if __name__ == "__main__":
    
    #r = threading.Thread(target=generate2,args=((2000000000,"timescale.tokens",("token","user_id","created"),(gen_token,gen_number_500k,gen_timestamp))))
    #r.daemon = True
    #r.start()
    #
    #q = threading.Thread(target=consumeloop)
    #q.daemon = True
    #q.start()
    b1 = threading.Thread(target=benchmark_tokens)
    b1.daemon = True
    b1.start()
    
    b2 = threading.Thread(target=benchmark_tokens)
    b2.daemon = True
    b2.start()
    
    b3 = threading.Thread(target=benchmark_tokens)
    b3.daemon = True
    b3.start()

    while True:
        input()
        print(counter)


    #generate(500000,"relational.users",
    #                ("firstname","lastname","phone","address","iban","company_id"),
    #                (fake.first_name,fake.last_name,fake.basic_phone_number,fake.street_address,fake.bban,gen_number_50))
        
    #generate(50000000,"relational.files",
    #                ("filename","created"),
    #                (gen_filename,gen_timestamp))

    #generatelbl(2000000,"relational.file_access",
    #                ("user_id","file_id"),
    #                (gen_number_500k,gen_number_15M))
