from enum import Enum

class SystemState(Enum):
    SETUP="setup"
    LEVEL= "level"
    LEVEL_INTERACTION="level_interaction"
    ENTRY_OPPORTUNITY= "entry_opportunity"
    TRADE= "trade"
    TRADE_OUTCOME="trade_outcome"

class Actions(Enum):
    #TOP LEVEL APPLICATION ACTIONS
    CREATE_SETUP="Create Setup"
    UPDATE_SETUP="update_setup"
    ANALYZE="analyze_data"

    # LIFECYCLE ACTION
    CONTINUE="continue"
    END="end"
    MENU="menu"
