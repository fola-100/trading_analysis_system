import re
from domain_model import Actions
from datetime import datetime

def get_user_action():
    while True:
        print("\n What would you like to do?")
        print("1) Create Setup")
        print("2) Update Setup")
        print("3) Analyze data")

        choice=input("Enter choice:").strip()

        if choice== "1":
            return Actions.CREATE_SETUP

        elif choice== "2":
            return Actions.UPDATE_SETUP

        elif choice=="3":
            return Actions.ANALYZE

        else:
            print("invalid choice")


def get_setup_data():
   while True:
       print("\n CHOOSE STRATEGY BEEN USED ")
       print('1) Supply and demand')
       print('2)Return-to-origin reversal')

       strategy_choice= input(">:")

       if strategy_choice=="1":
         strategy= "supply and demand"
         break
       elif strategy_choice=="2":
         strategy= "return-to-origin-reversal"
         break
       else:
         print("invalid choice. Please enter 1 or 2.")

   market_pair= input("Enter market pair:")

   while True:
       long_htf_direction= input("Enter long term HTF direction(long/short):")
       short_htf_direction=input("Enter short term HTF direction(long/short):")
       if long_htf_direction not in ["long","short"] or short_htf_direction not in ["long","short"]:
         print("HTF entry should  up or down ")
       else:
           break

   while True:
       mkt_condition= input("Enter market condition(ranging/trending/transitioning):")
       if mkt_condition not in ["ranging","trending","transitioning"]:
         print("market condition must be ranging, trending, or transitioning")
       else:
           break

   while True:
      candle_bias=input("Enter speculated next three candle (bullish/bearish/unsure):")
      if candle_bias not in ["bullish","bearish","unsure"]:
        print("Candle bias must be bullish, bearish or unsure")
      else:
          break

   return strategy,market_pair,long_htf_direction,short_htf_direction,mkt_condition,candle_bias


def get_level_data():
    #Get session
    while True:
        print("\n Which session was the level found in ?:")
        print("1. Asian session")
        print("2. London session")
        print("3.New York session")
        print("Sydney session")

        session_choice=input("Enter choice:").strip()

        if session_choice== "1":
            session= "Asia"
            break

        elif session_choice=="2":
            session= "London"
            break

        elif session_choice=="3":
            session= "New_York"
            break
        elif session_choice=="4":
            session= "Sydney"
            break
        else:
            print("Invalid choice. Please enter 1,2,3 4 or 5")

  #Get timeframe
    while True:
        print("\nWhat timeframe was the level created in?")
        print("1) 15M")
        print("2)30M")
        print("3) 1H")
        print("4) 4H")
        print("5) Daily")

        timeframe_choice=input("Enter choice:").strip()

        if timeframe_choice== "1":
            timeframe= "15M"
            break
        elif timeframe_choice=="2":
            timeframe= "1H"
            break
        elif timeframe_choice=="3":
            timeframe="3"
            break
        elif timeframe_choice=="4":
            timeframe="Daily"
            break
        else:
            print("Invalid choice. PLS enter 1,2,3,or 4")

   #GET LEVEL CRITERIA
    valid_criteria = {
        "displacement",
        "last pull back before displacement",
        "imbalance",
        "price created new high/low",
        "last pull back before imbalance",
        "no new high/low"
    }

    while True:
        print("\nWhat determined the area chosen as the level?")
        print("You can select more than one. Separate each option with a comma.")
        print("\nAvailable criteria:")
        print("- Displacement")
        print("- Last pull back before displacement")
        print("- Imbalance")
        print("- Price created new high/low")
        print("- Last pull back before imbalance")
        print("- No new high/low")
        print("- Other")

        criteria_input = input("\nEnter criteria: ").strip().lower()

        criteria_list = re.split(r",\s*", criteria_input)

        invalid_criteria = []

        for criterion in criteria_list:
            if criterion == "other":
                continue

            if criterion not in valid_criteria:
                invalid_criteria.append(criterion)

        if invalid_criteria:
            print("\nInvalid criteria:")
            for criterion in invalid_criteria:
                print(f"- {criterion}")

            print("\nPlease enter only criteria from the available options.")
            continue

        if "other" in criteria_list:
            while True:
                other_criteria = input(
                    "\nPlease describe the other factor that determined the level: "
                ).strip()

                if other_criteria:
                    criteria_list.remove("other")
                    criteria_list.append(f"other: {other_criteria}")
                    break

                print("Please provide a description.")

        break

    while True:
        print("\n What type of level is this?")
        print("1) Support")
        print("2) Resistance")

        level_type_choice = input("Enter choice: ").strip()

        if level_type_choice == "1":
            level_type = "support"
            break
        elif level_type_choice == "2":
            level_type = "resistance"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    while True:
        date_input= input("Enter data(YYYY-MM-DD):").strip()

        try:
            date_object=datetime.strptime(date_input,"%Y-%m-%d")

            formatted_date=date_object.strftime("%Y-%m-%d")

            break
        except ValueError:
            print("invalid date. Pls enter date in this formate(YYYY-MM-DD")


    return session,timeframe, criteria_list, level_type,formatted_date


def get_lifecycle_action(setup_id, current_stage, next_stage):
    print(f'Setup_id: {setup_id}')
    print(f'Current stage:{current_stage}')

    if next_stage is None:
        print("Next stage: Lifecycle completed")
        print("Would you like to end the program?")
        print("1)End program")

        while True:
            choice= input("Enter choice:").strip()

            if choice=="1":
                return Actions.END

            print("invalid input")


    print(f'Next stages: {next_stage}')
    print(f'What would you like to do?')
    print('1. Move to next the stage')
    print("2. End program")

    while True:
        choice= input("Enter choice:").strip()

        if choice== "1":
            return Actions.CONTINUE

        elif choice== "2":
            return Actions.END

        else:
            print("invalid choice. Enter 1 or 2.")

def display_error(error):
    print(f'Error:{error}')


