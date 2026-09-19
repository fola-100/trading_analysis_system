import sqlite3

#CRATING DATABASE AND
connection=sqlite3.connect("trading_journal.db")
cur=connection.cursor()

def create_setup_table():
   # CREATING DATA TABLE
   cur.execute("CREATE TABLE IF NOT EXISTS Setup(set_id INTEGER PRIMARY KEY,strategy TEXT, market_pair TEXT, long_htf_direction TEXT,"
               "short_htf_direction TEXT,mkt_condition TEXT, candle_bias TEXT,date_created TEXT)")

def set_value(setup):
   #ADDING VALUE INTO DATA TABLE
   cur.execute("INSERT INTO Setup(strategy,market_pair,long_htf_direction,short_htf_direction,mkt_condition,candle_bias,date_created)"
               "VALUES(?,?,?,?,?,?,?)",
               (setup.trade_strategy, setup.market_pair,
                setup.long_htf_direction,setup.short_htf_direction, setup.market_condition, setup.htf_next_three_candle, setup.date_created))

   connection.commit()


def create_key_level():
    cur.execute("CREATE TABLE IF NOT EXISTS Level(level_id INTEGER PRIMARY KEY,setup_id INTEGER NOT NULL,session_created TEXT,date_created TEXT,"
                "timeframe TEXT,criteria TEXT,level_type TEXT, FOREIGN KEY (setup_id) REFERENCES Setup(set_id))")

def key_level_value(level):
     cur.execute("INSERT INTO Level(setup_id,session_created,date_created,timeframe,criteria,level_type)"
                 "VALUES(?,?,?,?,?,?)",
                 (level.setup_id,level.session_created,level.date_created,level.timeframe,level.criteria,level.level_type) )

     connection.commit()



def get_set_id():
    record_id=cur.lastrowid
    return record_id


def get_key_zone_id():
    record_id=cur.lastrowid
    return record_id


def has_level(setup_id):
    cur.execute("SELECT 1 FROM LEVEL WHERE setup_id=? LIMIT 1", (setup_id,))
    result=cur.fetchone()
    return result is not None

def has_level_interaction(setup_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_entry_opportunity(setup_id):
    cur.execute("SELECT 1 FROM ENTRY_OPPORTUNITY WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_trade(setup_id):
    cur.execute("SELECT 1 FROM TRADE WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_trade_outcome(setup_id):
    cur.execute("SELECT 1 FROM TRADE_OUTCOME WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_setup(setup_id):
    cur.execute("SELECT 1 FROM SETUP WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None


def set_up(setup):
    create_setup_table()
    set_value(setup)
    setup_id=get_set_id()
    return setup_id

def key_level_setup (level):
    create_key_level()
    key_level_value(level)
    level_id=get_key_zone_id()
    return level_id



if __name__== "__main__":

    res = cur.execute("SELECT * FROM Setup")
    for row in res:
        print(row)
   #res = cur.execute("SELECT name FROM sqlite_master")
   #print(res.fetchone())



