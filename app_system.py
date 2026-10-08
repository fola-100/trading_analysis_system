import gate_way
import sys
import user_interface as ui
from datetime import date
from model import Setup,Level,LevelInteraction,EntryOpportunity,TRADE,TradeChecks,NoTradeOutcome,TradeOUTCOME
from domain_model import SystemState, Actions


def build_setup():
       setup_data=ui.get_setup_data()

       current_date=date.today().isoformat()

       setup=Setup(*setup_data,current_date)

       setup_id=gate_way.set_up(setup)

       return setup_id


def build_level(set_id):
    level_data=ui.get_level_data()

    level=Level(*level_data,set_id)

    gate_way.key_level_setup(level)


def build_level_interaction(level_id):
    level_interaction_data=ui.get_level_interaction()

    level_interaction= LevelInteraction(level_id,*level_interaction_data)

    gate_way.key_level_interaction_setup(level_interaction)

def build_entry_opportunity(level_interaction_id):
    opportunity_data= ui.get_entry_opportunity_data()

    entry_opportunity=EntryOpportunity(level_interaction_id,*opportunity_data)

    gate_way.entry_opportunity_setup(entry_opportunity)

def build_trade(opportunity_id):
    trade_data=ui.get_trade_data()

    trade=TRADE(opportunity_id,*trade_data)

    gate_way.trade_setup(trade)

def build_trade_check(trade_id):
    trade_check_data=ui.get_trade_check_data()

    trade_check=TradeChecks(trade_id,*trade_check_data)

    gate_way.trade_check_setup(trade_check)

def build_not_taken_outcome(opportunity_id):
    not_taken_outcome_data=ui.not_taken_outcome()

    not_taken_outcome=NoTradeOutcome(opportunity_id,*not_taken_outcome_data)

    gate_way.not_taken_outcome_setup(not_taken_outcome)

def build_trade_outcome(trade_id):
    trade_outcome_data=ui.get_trade_outcome_data()

    trade_outcome=TradeOUTCOME(trade_id,*trade_outcome_data)

    gate_way.build_trade_outcome(trade_outcome)



def search_setup_status(setup_id):
    setup_id_response = gate_way.has_setup(setup_id)
    level_response = gate_way.has_level(setup_id)

    if level_response:
        return SystemState.LEVEL

    if setup_id_response:
       return SystemState.SETUP

    raise ValueError(f'Setup with ID{setup_id} does not exist')

def determine_level_state(level_id):

     level_interaction_response= gate_way.has_level_interaction(level_id)
     entry_opportunity_response= gate_way.has_entry_opportunity(level_id)
     trade_response=gate_way.has_trade(level_id)
     trade_outcome_response=gate_way.has_trade_outcome(level_id)
     trade_check_response=gate_way.has_trade_check(level_id)
     not_taken_outcome_response=gate_way.has_not_taken_outcome(level_id)

     if trade_outcome_response:
         return SystemState.TRADE_OUTCOME

     if trade_check_response:
         return SystemState.TRADE_CHECKS

     if trade_response:
         return SystemState.TRADE

     if not_taken_outcome_response:
         return SystemState.NOT_TAKEN_OUTCOME

     if entry_opportunity_response:
         return SystemState.ENTRY_OPPORTUNITY

     if level_interaction_response:
         return SystemState.LEVEL_INTERACTION

     return SystemState.LEVEL

def next_setup_stage(current_stage):
    if current_stage == SystemState.SETUP:
        return SystemState.LEVEL

    if current_stage == SystemState.LEVEL:
        return SystemState.LEVEL_INTERACTION

    if current_stage == SystemState.LEVEL_INTERACTION:
        return SystemState.ENTRY_OPPORTUNITY

    if current_stage == SystemState.ENTRY_OPPORTUNITY:
        return SystemState.TRADE

    if current_stage == SystemState.TRADE:
        return SystemState.TRADE_CHECKS

    if current_stage==SystemState.TRADE_CHECKS:
        return SystemState.TRADE_OUTCOME

    if current_stage == SystemState.TRADE_OUTCOME:
        return None

    if current_stage == SystemState.NOT_TAKEN_OUTCOME:
        return None


    return None

def determine_current_and_next_state(setup_id,levels_id=None):
    response = search_setup_status(setup_id)
    if response == SystemState.LEVEL:
        if levels_id is None:
          levels = get_levels_created(setup_id)
          levels_id = ui.get_user_level_choice(levels)

        current_state = determine_level_state(levels_id)

        if current_state==SystemState.ENTRY_OPPORTUNITY:
            trade_action=gate_way.get_trade_action(levels_id)

            if trade_action == "NOT_TAKEN":
                next_state = SystemState.NOT_TAKEN_OUTCOME

            else:
                next_state= next_setup_stage(current_state)

        else:
            next_state = next_setup_stage(current_state)

        return current_state, next_state, levels_id


    elif response== SystemState.SETUP:
        current_state=SystemState.SETUP
        next_state= next_setup_stage(current_state)

        return current_state, next_state, None

    return None



def get_levels_created(setup_id):
    return gate_way.get_levels(setup_id)

def create_new_level(setup_id):
    build_level(setup_id)
    return None

#HELP FUNCTIONS
def get_level_interaction_or_stop(level_id):
    level_interaction_id=gate_way.get_level_interact_id(level_id)

    if level_interaction_id is None:
        ui.display_error(f'Level_interaction as not been created yet.')
        return None
    return level_interaction_id

def get_opportunity_or_stop(level_interaction_id):
    opportunity_id = gate_way.get_entry_opportunity(level_interaction_id)
    if opportunity_id is None:
        ui.display_error(f'Entry_opportunity as not been created yet')
        return None
    return opportunity_id

def get_trade_or_stop(opportunity_id):
    trade_id=gate_way.get_trade(opportunity_id)
    if trade_id is None:
        ui.display_error(f'Trade as not been created yet.')
    return trade_id


def continue_lifecycle(setup_id, level_id, next_stage):
    if next_stage == SystemState.LEVEL:
        create_new_level(setup_id)

    elif next_stage == SystemState.LEVEL_INTERACTION:
        build_level_interaction(level_id)

    elif next_stage == SystemState.ENTRY_OPPORTUNITY:
       level_interaction_id=get_level_interaction_or_stop(level_id)
       build_entry_opportunity(level_interaction_id)

    elif next_stage== SystemState.TRADE:
        level_interaction_id = get_level_interaction_or_stop(level_id)
        opportunity_id=get_opportunity_or_stop(level_interaction_id)
        build_trade(opportunity_id)

    elif next_stage== SystemState.TRADE_CHECKS:
        level_interaction_id = get_level_interaction_or_stop(level_id)
        opportunity_id = get_opportunity_or_stop(level_interaction_id)
        trade_id=get_trade_or_stop(opportunity_id)
        if trade_id is None:
            return None
        build_trade_check(trade_id)

    elif next_stage== SystemState.NOT_TAKEN_OUTCOME :
        level_interaction_id = get_level_interaction_or_stop(level_id)
        opportunity_id = get_opportunity_or_stop(level_interaction_id)
        build_not_taken_outcome(opportunity_id)

    elif next_stage == SystemState.TRADE_OUTCOME :
        level_interaction_id = get_level_interaction_or_stop(level_id)
        opportunity_id = get_opportunity_or_stop(level_interaction_id)
        trade_id = get_trade_or_stop(opportunity_id)
        if trade_id is None:
            return None
        build_trade_outcome(trade_id)




def action_lifecycle(action):
    try:
       if action == Actions.CREATE_SETUP:
            setup_id = build_setup()

            return  setup_id

    except ValueError as error:
        ui.display_error(str(error))

    return None


def start_application():

    while True:
      action = ui.get_user_action()
      if action==Actions.END:
        sys.exit()

      if action== Actions.CREATE_SETUP:
          result=action_lifecycle(action)

          if result is None:
              continue

          setup_id = result


          while True:
              response=search_setup_status(setup_id)
              if response == SystemState.LEVEL:
                  levels = get_levels_created(setup_id)
                  user_response = ui.get_level_creation_choice(levels)

                  if user_response:
                      create_new_level(setup_id)
                      continue
                  else:
                      break
              else:
                  break

          levels_id=None

          while True:
              current_state, next_state,level_id = determine_current_and_next_state(setup_id,levels_id)

              levels_id=level_id

              user_next_action = ui.get_lifecycle_action(setup_id,current_state,next_state)

              if user_next_action == Actions.END:
                  sys.exit()

              elif user_next_action == Actions.MENU:
                  break

              elif user_next_action == Actions.CONTINUE:
                  continue_lifecycle(setup_id,level_id,next_state)
















