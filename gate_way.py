import sqlite3
from tkinter.constants import INSERT

#CRATING DATABASE AND
connection=sqlite3.connect("trading_journal.db")
cur=connection.cursor()

def create_setup_table():
   # CREATING DATA TABLE
   cur.execute("CREATE TABLE IF NOT EXISTS Setup(setup_id INTEGER PRIMARY KEY,strategy TEXT, market_pair TEXT, long_htf_direction TEXT,"
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
                "timeframe TEXT,level_type TEXT, FOREIGN KEY (setup_id) REFERENCES Setup(setup_id))")

def key_level_value(level):
     cur.execute("INSERT INTO Level(setup_id,session_created,date_created,timeframe,level_type)"
                 "VALUES(?,?,?,?,?)",
                 (level.setup_id,level.session_created,level.date_created,level.timeframe,level.level_type) )

     connection.commit()
     return cur.lastrowid

#THIS TABLE AND VALUE BELONG TO LEVEL
def create_level_criteria():
    cur.execute("CREATE TABLE IF NOT EXISTS Level_criteria(criteria_id INTEGER PRIMARY KEY, level_id INTEGER NOT NULL, criteria_value TEXT)")

def level_criteria_value(level_id,criteria):
    cur.execute("INSERT INTO Level_criteria(level_id, criteria_value)VALUES(?,?)",(level_id,criteria))

    connection.commit()



def create_level_interaction():
    cur.execute("CREATE TABLE IF NOT EXISTS Level_interaction(level_interaction_id INTEGER PRIMARY KEY, level_id INTEGER NOT NULL UNIQUE,"
                "date_price_reach Text, session Text,interaction_on_level Text, FOREIGN KEY (level_id) REFERENCES Level(level_id))")

def level_interaction_value(data):
    cur.execute("INSERT INTO Level_interaction(level_id, date_price_reach, session, interaction_on_level) VALUES(?,?,?,?)",
                (data.level_id,data.date_price_reach,data.session,data.interaction_on_level))

    connection.commit()
    return cur.lastrowid

def create_entry_opportunity():
    cur.execute("CREATE TABLE IF NOT EXISTS EntryOpportunity(opportunity_id INTEGER PRIMARY KEY,level_interaction_id INTEGER NOT NULL UNIQUE,"
                " valid_entry TEXT, trade_direction TEXT, daily_bias TEXT, trade_action TEXT, not_taken_reason TEXT,"
                " FOREIGN KEY (level_interaction_id) REFERENCES Level_interaction(level_interaction_id))")

def entry_opportunity_value(data):
    cur.execute("INSERT INTO EntryOpportunity(level_interaction_id, valid_entry, trade_direction, daily_bias, trade_action,"
                " not_taken_reason)VALUES(?,?,?,?,?,?)",(data.level_interaction_id,data.valid_entry,data.trade_direction,
                 data.daily_bias,data.trade_action,  data.not_taken_reason))

    connection.commit()
    return cur.lastrowid

#THIS TABLE BELONG TO ENTRY OPPORTUNITY
def create_confirmation_pattern():
    cur.execute("CREATE TABLE IF NOT EXISTS Confirmation_pattern(confirmation_pattern_id INTEGER PRIMARY KEY,"
                " opportunity_id INTEGER NOT NULL,confirmation_pattern TEXT, FOREIGN KEY (opportunity_id) REFERENCES EntryOpportunity(opportunity_id))")

def create_confirmation_pattern_value(opportunity_id,pattern ):
    cur.execute("INSERT INTO confirmation_pattern(opportunity_id, confirmation_pattern)VALUES(?,?)", (opportunity_id,pattern))

    connection.commit()




def create_trade():
    cur.execute("CREATE TABLE IF NOT EXISTS Trade(trade_id INTEGER PRIMARY KEY, opportunity_id INTEGER NOT NULL UNIQUE,"
                "entry_date TEXT,time TEXT, entry_value REAL, tp_value REAL, sl_value REAL, FOREIGN KEY (opportunity_id) REFERENCES Entry_opportunity(opportunity_id))")

def trade_value(data):
    cur.execute("INSERT INTO Trade(opportunity_id, entry_date, time,entry_value,tp_value, sl_value) VALUES(?,?,?,?,?,?)",
                (data.opportunity_id, data.entry_date,data.time,data.entry_value, data.tp_value,data.sl_value))

    connection.commit()
    return cur.lastrowid

#THIS TABLE AND VALUE BELONG TO TRADE
def create_trade_confirmation_timeframe():
   cur.execute("CREATE TABLE IF NOT EXISTS Trade_confirmation_timeframe(confirmation_id INTEGER PRIMARY KEY, "
               "trade_id INTEGER NOT NULL, timeframe TEXT)")

   connection.commit()

def trade_confirmation_value(trade_id, timeframe):
    cur.execute("INSERT INTO Trade_confirmation_timeframe(trade_id, timeframe)"
                "VALUES(?,?)",(trade_id,timeframe))

    connection.commit()

def create_trade_ratio_factor():
    cur.execute("CREATE TABLE IF NOT EXISTS Trade_ratio_factor(factor_id INTEGER PRIMARY KEY,"
                "trade_id INTEGER NOT NULL, factor TEXT )")

    connection.commit()

def trade_ratio_value(trade_id, factor):
    cur.execute("INSERT INTO Trade_ratio_factor(trade_id, factor)VALUES(?,?)",(trade_id,factor))

    connection.commit()

#THIS TABLE IS FOR TRADE CHECKS
def create_trade_checks():
    cur.execute("CREATE TABLE IF NOT EXISTS Trade_check(trade_check_id INTEGER PRIMARY KEY,trade_id INTEGER NOT NULL UNIQUE,"
                "followed_rules TEXT ,setup_skepticism TEXT,entry_timing TEXT)")


def trade_check_value(data):
    cur.execute("INSERT INTO Trade_check(trade_id,followed_rules,setup_skepticism,entry_timing)VALUES(?,?,?,?)",
                (data.trade_id,data.followed_rules,data.setup_skepticism,data.entry_timing))


    connection.commit()

    return cur.lastrowid
#THIS TABLE BELONG TO NOT TAKEN TRADE OUTCOME
def create_not_taken_outcome():
    cur.execute("CREATE TABLE IF NOT EXISTS Not_taken_outcome(not_taken_outcome_id INTEGER PRIMARY KEY,"
                "opportunity_id INTEGER NOT NULL UNIQUE, hypothetical_trade_ratio TEXT, outcome TEXT) ")

def not_taken_outcome_value(data):
    cur.execute("INSERT INTO Not_taken_outcome(opportunity_id, hypothetical_trade_ratio, outcome) VALUES(?,?,?)",
                (data.opportunity_id, data.hypothetical_trade_ratio,data.outcome))

    connection.commit()
    return cur.lastrowid

#THIS TABLE BELONG TO TRADE-OUTCOME
def create_trade_outcome():
    cur.execute("CREATE TABLE IF NOT EXISTS Trade_outcome(trade_outcome_id INTEGER PRIMARY KEY,trade_id INTEGER NOT NULL UNIQUE,"
                "outcome TEXT,manual_close_pattern TEXT,maximum_favorable_movement REAL,maximum_adverse_movement REAL,daliy_candle_result TEXT)")

def trade_outcome_value(data):
    cur.execute("INSERT INTO Trade_outcome(trade_id, outcome, manual_close_pattern,maximum_favorable_movement,maximum_adverse_movement,daliy_candle_result)"
                "VALUES(?,?,?,?,?,?)",(data.trade_id,data.outcome,data.manual_close_pattern,data.maximum_favorable_movement,
                data.maximum_adverse_movement,data.daily_candle_result))

    connection.commit()
    return cur.lastrowid

def get_levels(setup_id):
    cur.execute("SELECT level_id, setup_id, session_created, date_created, timeframe,level_type"
                " FROM LEVEL WHERE setup_id=?", (setup_id,))
    result=cur.fetchall()
    return result

def has_setup(setup_id):
    cur.execute("SELECT 1 FROM SETUP WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_level(setup_id):
    cur.execute("SELECT 1 FROM LEVEL WHERE setup_id=? LIMIT 1",(setup_id,))
    result=cur.fetchone()
    return result is not None

def has_level_interaction(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION WHERE level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def has_entry_opportunity(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION li JOIN EntryOpportunity eo"
                " ON eo.level_interaction_id= li.level_interaction_id WHERE level_id=? LIMIT 1",(level_id,))

    result=cur.fetchone()
    return result is not None

def has_trade(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION li JOIN EntryOpportunity eo"
                " ON eo.level_interaction_id=li.level_interaction_id JOIN TRADE t "
                "ON t.opportunity_id = eo.opportunity_id WHERE level_id=? LIMIT 1",(level_id,))

    result=cur.fetchone()
    return result is not None

def has_trade_check(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION li JOIN ENTRYOPPORTUNITY eo "
                "ON eo.level_interaction_id=li.level_interaction_id JOIN TRADE t "
                "ON t.opportunity_id=eo.opportunity_id JOIN TRADE_CHECK tc "
                "ON tc.trade_id= t.trade_id WHERE li.level_id=? LIMIT 1",(level_id,))

    result=cur.fetchone()
    return result is not None

def has_trade_outcome(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION li JOIN EntryOpportunity eo"
                " ON eo.level_interaction_id=li.level_interaction_id JOIN TRADE t ON t.opportunity_id=eo.opportunity_id"
                " JOIN TRADE_OUTCOME ot ON t.trade_id = ot.trade_id WHERE li.level_id=? LIMIT 1",(level_id,))
    result=cur.fetchone()
    return result is not None

def has_not_taken_outcome(level_id):
    cur.execute("SELECT 1 FROM LEVEL_INTERACTION li JOIN EntryOpportunity eo"
                " ON eo.level_interaction_id=li.level_interaction_id JOIN Not_taken_outcome nto "
                " ON nto.opportunity_id=eo.opportunity_id WHERE li.level_id=? LIMIT 1",(level_id,))

    result=cur.fetchone()
    return result is not None

def get_level_interact_id(level_id):
    cur.execute("SELECT level_interaction_id FROM level_interaction WHERE level_id=?",(level_id,))
    result=cur.fetchone()

    if result is None:
        return None

    return result[0]

def get_entry_opportunity(level_interact_id):
    cur.execute("SELECT opportunity_id FROM EntryOpportunity WHERE level_interaction_id=?",(level_interact_id,))
    result=cur.fetchone()

    if result is None:
        return None

    return result[0]

def get_trade(opportunity_id):
    cur.execute("SELECT trade_id FROM trade WHERE opportunity_id=?",(opportunity_id,))

    result = cur.fetchone()

    if result is None:
        return None

    return result[0]

def get_trade_action(level_id):
    cur.execute("SELECT trade_action FROM LEVEL_INTERACTION li JOIN ENTRYOPPORTUNITY eo "
                " ON eo.level_interaction_id = li.level_interaction_id WHERE li.level_id=? ",(level_id,))
    result=cur.fetchone()

    if result is None:
        return None

    return result[0]


def set_up(setup):
    setup_id=set_value(setup)
    return setup_id

def key_level_setup (level_data):
    key_zone_id=key_level_value(level_data)

    for criteria in level_data.criteria:
      level_criteria_value(key_zone_id,criteria)


def key_level_interaction_setup(interaction_data):
    level_interact_id=level_interaction_value(interaction_data)
    return level_interact_id

def trade_setup(trade_data):

    trade_id=trade_value(trade_data)

    for timeframe in trade_data.confirmation_timeframe:
        trade_confirmation_value(trade_id, timeframe)

    for factor in trade_data.trade_ratio:
        trade_ratio_value(trade_id, factor)

    return trade_id

def trade_check_setup(trade_check_data):
    trade_check_id=trade_check_value(trade_check_data)
    return trade_check_id

def entry_opportunity_setup(entry_opportunity_data):
    entry_opportunity_id=entry_opportunity_value(entry_opportunity_data)

    if entry_opportunity_data.confirmation_patterns is not None:
      for pattern in entry_opportunity_data.confirmation_patterns:
        create_confirmation_pattern_value(entry_opportunity_id, pattern)


def not_taken_outcome_setup(data):

    not_taken_outcome_id=not_taken_outcome_value(data)
    return not_taken_outcome_id

def build_trade_outcome(trade_outcome_data):

    trade_outcome_id=trade_outcome_value(trade_outcome_data)
    return trade_outcome_id

def initialize_database():
    create_setup_table()
    create_key_level()
    create_level_criteria()
    create_level_interaction()
    create_entry_opportunity()
    create_confirmation_pattern()
    create_trade()
    create_trade_confirmation_timeframe()
    create_trade_ratio_factor()
    create_trade_checks()
    create_not_taken_outcome()
    create_trade_outcome()




