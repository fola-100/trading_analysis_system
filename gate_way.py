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
   return cur.lastrowid


def create_key_level():
    cur.execute("CREATE TABLE IF NOT EXISTS Level(level_id INTEGER PRIMARY KEY,setup_id INTEGER NOT NULL,session_created TEXT,date_created TEXT,"
                "timeframe TEXT,criteria TEXT,level_type TEXT, FOREIGN KEY (setup_id) REFERENCES Setup(set_id))")

def key_level_value(level):
     cur.execute("INSERT INTO Level(setup_id,session_created,date_created,timeframe,criteria,level_type)"
                 "VALUES(?,?,?,?,?,?)",
                 (level.setup_id,level.session_created,level.date_created,level.timeframe,level.criteria,level.level_type) )

     connection.commit()
     return cur.lastrowid

def create_level_interaction():
    cur.execute("CREATE TABLE IF NOT EXISTS Level_interaction(level_interaction_id INTEGER PRIMARY KEY, level_id INTEGER NOT NULL UNIQUE,"
                "date_price_reach Text, session Text,interaction_on_level Text, FOREIGN KEY (level_id) REFERENCES (Level_interaction))")

def level_interaction_value(data):
    cur.execute("INSERT INTO Level_interaction(level_id, date_price_reach, session, interaction_on_level) VALUES(?,?,?,?)",
                (data.level_id,data.data_price_reach,data.session,data.interaction_on_level))

    connection.commit()
    return cur.lastrowid

def create_entry_opportunity():
    cur.execute("CREATE TABLE IF NOT EXISTS EntryOpportunity(opportunity_id INTEGER PRIMARY KEY,level_interaction_id INTEGER NOT NULL UNIQUE,"
                "valid_entry TEXT, trade_direction TEXT, daily_bias TEXT, trade_action TEXT, confirmation_pattern TEXT, not_taken_reason TEXT,"
                "FOREIGN KEY (level_interaction_id) REFERENCE Level_interaction(level_interaction_id)")

def entry_opportunity_value(data):
    cur.execute("INSERT INTO EntryOpportunity(level_interaction_id, valid_entry, trade_direction, daily_bias, trade_action,"
                "confirmation_pattern, not_taken_reason),VALUES(?,?,?,?,?,?,?)",(data.valid_entry,data.trade_direction,
                 data.daily_bias,data.trade_action, data.confirmation_pattern, data.not_taken_reason))

    connection.commit()
    return cur.lastrowid

def create_trade():
    cur.execute("CREATE TABLE IF NOT EXIST Trade(Trade_id INTEGER PRIMARY KEY, opportunity_id INTEGER NOT NULL UNIQUE,"
                "entry_date,time,time_frame,trade_ratio REFERENCE entry_opportunity(opportunity_id))")

def trade_value(data):
    cur.execute("INSERT INTO Trade(opportunity_id, entry_date, time, time_frame,trade_ratio),VALUES(?,?,?,?,?)",
                (data.entry_date,data.time, data.confirmation_timeframe,data.trade_ratio))

    connection.commit()
    return cur.lastrowid





def get_levels(setup_id):
    cur.execute("level_id, setup_id, session, date_created, timeframe, criteria,level_type"
                " FROM LEVEL WHERE setup_id=?", (setup_id,))
    result=cur.fetchone()
    return result

def has_setup(setup_id):
    cur.execute("SELECT 1 FROM SETUP WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_level(setup_id):
    cur.execute("SELECT 1 FROM LEVEL WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result

def has_level_interaction(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION WHERE level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def has_entry_opportunity(level_id):
    cur.execute("SELECT 1 FROM ENTRY_OPPORTUNITY WHERE level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def has_trade(level_id):
    cur.execute("SELECT 1 FROM TRADE WHERE level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def has_trade_outcome(level_id):
    cur.execute("SELECT 1 FROM TRADE_OUTCOME WHERE level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def get_level_interact_id(level_id):
    cur.execute("SELECT level_interaction_id FROM level_interaction WHERE level_id=?",(level_id,))
    result=cur.fetchone()

    if result is None:
        return None

    return result[0]

def set_up(setup):
    create_setup_table()
    setup_id=set_value(setup)
    return setup_id

def key_level_setup (level_id):
    create_key_level()
    key_zone_id=key_level_value(level_id)
    return key_zone_id

def key_level_interaction(interaction_data):
    create_level_interaction()
    level_interact_id=level_interaction_value(interaction_data)
    return level_interact_id

def trade(trade_data):
    create_trade()
    trade_id=trade_value(trade_data)



if __name__== "__main__":

    res = cur.execute("SELECT * FROM Setup")
    for row in res:
        print(row)
   #res = cur.execute("SELECT name FROM sqlite_master")
   #print(res.fetchone())



