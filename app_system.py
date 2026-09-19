import gate_way
import sys
import user_interface as ui
from datetime import date
from model import Setup,Level
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

    level_id=gate_way.key_level_setup(level)

    return level_id



def determine_current_stage(setup_id):
     level_response=gate_way.has_level(setup_id)
     level_interaction_response= gate_way.has_level_interaction(setup_id)
     entry_opportunity_response= gate_way.has_entry_opportunity(setup_id)
     trade_response=gate_way.has_trade(setup_id)
     trade_outcome_response=gate_way.has_trade_outcome(setup_id)
     setup_id_response=gate_way.has_setup(setup_id)

     if trade_outcome_response:
         return SystemState.TRADE_OUTCOME

     if trade_response:
         return SystemState.TRADE

     if entry_opportunity_response:
         return SystemState.ENTRY_OPPORTUNITY

     if level_interaction_response:
         return SystemState.LEVEL_INTERACTION

     if level_response:
         return SystemState.LEVEL

     if setup_id_response:
         return SystemState.SETUP

     raise ValueError(f'Setup with ID{setup_id} does not exist')


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

def continue_lifecycle(setup_id, next_stage:SystemState):
    if next_stage== SystemState.LEVEL:
        level_id=build_level(setup_id)



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
              current_state = determine_current_stage(setup_id)
              next_state = next_setup_stage(current_state)

              user_next_action = ui.get_lifecycle_action(setup_id,current_state,next_state)

              if user_next_action==Actions.END:
                sys.exit()

              elif user_next_action==Actions.MENU:
                break

              elif user_next_action==Actions.CONTINUE:
                  continue_lifecycle(setup_id, next_state)











#if __name__== "__main__":
 # start_application()















