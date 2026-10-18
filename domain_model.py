from enum import Enum

class SystemState(Enum):
    SETUP="setup"
    LEVEL= "level"
    LEVEL_INTERACTION="level_interaction"
    ENTRY_OPPORTUNITY= "entry_opportunity"
    TRADE= "trade"
    TRADE_CHECKS= "trade_checks"
    NOT_TAKEN_OUTCOME= "not_taken_outcome"
    TRADE_OUTCOME="trade_outcome"

class Actions(Enum):
    #TOP LEVEL APPLICATION ACTIONS
    CREATE_SETUP="Create Setup"
    UPDATE_LIFECYCLE= "update_lifecycle"
    ANALYZE="analyze_data"
    GET_LAST_SETUP_ID= "get_last_setup_id"
    GET_ALL_SETUP_IDS= "get_all_setup_ids"
    INPUT_SETUP_ID= "input_setup_id"
    GET_SETUP_ID_BY_DATE="find_setup_id_by_date"


    # LIFECYCLE ACTION
    CONTINUE="continue"
    END="end"
    MENU="menu"
