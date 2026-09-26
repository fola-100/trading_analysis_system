import gate_way
import sys
import user_interface as ui
from datetime import date
from model import Setup,Level,LevelInteraction,EntryOpportunity
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

    gate_way.key_level_interaction(level_interaction)

def build_entry_opportunity(level_interaction_id):
    opportunity_data= ui.get_entry_opportunity_data()

    entry_opportunity=EntryOpportunity(level_interaction_id,*opportunity_data)

    gate_way.entry_opportunity_value(entry_opportunity)





def search_setup_status(setup_id):
    setup_id_response = gate_way.has_setup(setup_id)
    level_response = gate_way.has_level(setup_id)

    if level_response:
        return SystemState.LEVEL

    if setup_id_response:
       return SystemState.SETUP

    raise ValueError(f'Setup with ID{setup_id} does not exist')

def continue_setup_status_search(level_id):

     level_interaction_response= gate_way.has_level_interaction(level_id)
     entry_opportunity_response= gate_way.has_entry_opportunity(level_id)
     trade_response=gate_way.has_trade(level_id)
     trade_outcome_response=gate_way.has_trade_outcome(level_id)

     if trade_outcome_response:
         return SystemState.TRADE_OUTCOME

     if trade_response:
         return SystemState.TRADE

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
        return SystemState.TRADE_OUTCOME

    if current_stage == SystemState.TRADE_OUTCOME:
        return None

    return None

def determine_current_and_next_state(setup_id):
    response = search_setup_status(setup_id)
    if response == SystemState.LEVEL:
        levels = get_levels_created(setup_id)
        levels_id = ui.get_user_level_choice(levels)

        current_state = continue_setup_status_search(levels_id)

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
    levels = get_levels_created(setup_id)

    if not levels:
        return build_level(setup_id)

    user_response = ui.get_level_creation_choice(levels)

    if user_response:
       return build_level(setup_id)

    return None

def test():



def continue_lifecycle(setup_id, level_id, next_stage):
    if next_stage == SystemState.LEVEL:
        create_new_level(setup_id)

    if next_stage == SystemState.LEVEL_INTERACTION:
        build_level_interaction(level_id)

    if next_stage == SystemState.ENTRY_OPPORTUNITY:
        level_interaction_id=gate_way.get_level_interact_id(level_id)
        build_entry_opportunity(level_interaction_id)

    #if next_stage== SystemState.TRADE:



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
              current_state, next_state,level_id = determine_current_and_next_state(setup_id)

              if current_state == SystemState.LEVEL:
                  create_new_level(setup_id)

              user_next_action = ui.get_lifecycle_action(setup_id,current_state,next_state)

              if user_next_action == Actions.END:
                  sys.exit()

              elif user_next_action == Actions.MENU:
                  break

              elif user_next_action == Actions.CONTINUE:
                  continue_lifecycle(setup_id,level_id,next_state)
















#if __name__== "__main__":
 # start_application()















