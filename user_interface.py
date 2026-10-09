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

# DATA COLLECTION
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
   while True:
      market_pair= input("\nEnter market pair:").lower()
      if market_pair:
          break
      print("Enter market pair been traded")

   while True:
       long_htf_direction= input("\nEnter long term HTF direction(long/short):").lower().strip()
       short_htf_direction=input("\nEnter short term HTF direction(long/short):").lower().strip()
       if long_htf_direction not in ["long","short"] or short_htf_direction not in ["long","short"]:
         print("HTF entry should  long or short ")
       else:
           break

   while True:
       mkt_condition= input("\nEnter market condition(ranging/trending/transitioning):").strip().lower()
       if mkt_condition not in ["ranging","trending","transitioning"]:
         print("\nmarket condition must be ranging, trending, or transitioning")
       else:
           break

   while True:
      candle_bias=input("\nEnter speculated next three candle (bullish/bearish/unsure):").lower().strip()
      if candle_bias not in ["bullish","bearish","unsure"]:
        print("Candle bias must be bullish, bearish or unsure")
      else:
          break

   return strategy,market_pair,long_htf_direction,short_htf_direction,mkt_condition,candle_bias

def get_date():
    while True:
        date_input = input("Enter data(YYYY-MM-DD):").strip()

        try:
            date_object = datetime.strptime(date_input, "%Y-%m-%d")

            formatted_date = date_object.strftime("%Y-%m-%d")

            return formatted_date
        except ValueError:
            print("invalid date. Pls enter date in this formate(YYYY-MM-DD")


def get_level_data():
    #Get session
    while True:
        print("\n Which session was the level found in ?:")
        print("1. Asian session")
        print("2. London session")
        print("3.New York session")
        print("4.Sydney session")

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
            timeframe="30MIN"
            break
        elif timeframe_choice=="4":
            timeframe="4hr"
            break
        elif timeframe_choice== "5":
             timeframe="Daily"
             break
        else:
            print("Invalid choice. Please enter from 1,2,3,or 5")

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

        criteria_input = input("\nEnter criteria: ").lower()

        criteria_list = re.split(r",\s*", criteria_input)

        if not criteria_input.strip() or any(not item for item in criteria_list):
            print("\n Invalid input. Please enter criteria separated by commas.")
            continue

        if len(criteria_list) != len(set(criteria_list)):
            print("\n Duplicate criteria detected.")
            print("Please enter each criteria only once")
            continue


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

    date=get_date()


    return session,timeframe, criteria_list, level_type,date

def get_level_interaction():

    date=get_date()

    print("\nSelect session when price came to level in the available options")
    sessions= ["Asian", "London","New York","Sydney"]

    for number,sessions in enumerate(sessions, start=1):
        print(f'{number},{sessions}')

    while True:
        responses=input('Enter session number:').strip()
        try:
          if responses.isdigit():
            choice=int(responses)

            if 1<=choice <= len(sessions):
                session_selected=sessions[choice -1]
                break
          print("invalid choice. please select a valid session")

        except ValueError:
            print("invalid input")

    print("\nSelect price action movement when approaching  level")
    price_movements=["enter level","touch","break","did not reach"]

    for number, movement in enumerate(price_movements, start=1):
        print(f'{number}, {movement}')

    while True:
        responses=input("Enter your choice:").strip()
        try:
          if responses.isdigit():
            choice=int(responses)

            if 1 <= choice <= len(price_movements):
                price_interaction= price_movements[choice -1]
                break

            print("invalid choice. enter valid option.")

        except ValueError:
            print("invalid input number most be a whole number")

    return date,session_selected,price_interaction

def get_entry_opportunity_data():
    # Trade direction
    while True:
        print("\nWhat was the trade direction?:")
        print("1. Long")
        print("2. Short")

        response=input("Select an option:").strip()

        if response == "1":
            trade_direction= "LONG"
            break
        elif response== "2":
            trade_direction = "SHORT"
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

    while True:
        print("\n What was the daily bias?")
        print("1. Bullish ")
        print("2. Bearish")
        print("3. Unclear")

        response=input("Select an option:").strip()

        if response== "1":
            daily_bias= "BULLISH"
            break
        elif  response== "2":
            daily_bias= "BEARISH"
            break
        elif  response== "3":
            daily_bias= "UNCLEAR"
            break
        else:
            print("invalid choice. Please select 1,2, or 3")

#  was the trade taken ?
    while True:
        print("\n Was the trade taken")
        print("1. Taken")
        print("2. Not taken")

        response=input("Select an option:").strip()

        if response== "1":
            trade_action= "TAKEN"
            break
        elif response== "2":
            trade_action = "NOT_TAKEN"
            break
        else:
            print("invalid choice. Please select 1 or 2.")

    confirmation_patterns= None
    not_taken_reason= None

    if trade_action == "TAKEN":
        patterns=[ "BOS", "Strong bullish candle",
                   "Liquidity sweep", "Order block",
                   "CHoCH", "Rejection", "Depletion",
                   "No confirmation use", "Failed BOS" ]

        print("\nWhat pattern was the trading/entry decision based on?")

        # Display the available patterns
        for number, pattern in enumerate(patterns, start=1):
            print(f"{number}. {pattern}")

        while True:
            user_response = input("Select pattern(s). Separate multiple choices with commas: ")

            # Check that at least one choice was entered
            if not user_response.strip():
                print("Invalid choice. Please select at least one choice.")
                continue

            try:
                selected_choices=[ int(choice.strip()) for choice in user_response.split(",") ]

                if len(selected_choices)!= len(set(selected_choices)):
                    print("\n Duplicate criteria detected.")
                    print("Please enter each pattern number only once")
                    continue

                # Check that every number is a valid option
                if not all( 1 <= choice <= len(patterns) for choice in selected_choices ):
                    print("Input entered is not among the options.")
                    continue


                confirmation_patterns = [patterns[choice - 1] for choice in selected_choices]

                break

            except ValueError:
                print("Selected input must be a number seprated by comma.")

    else:
        reasons_list=["No confirmation","Missed entry", "Hesitation", "Fear","Didn't see  it",
                 "Rule violation prevented entry","confirmation unclear", "Other"]

        print("\n Why was the trade not taken?:")

        for number, reasons in enumerate(reasons_list, start=1):
            print(f'{number},{reasons}')

        while True:
            response = input("Select a reason: ").strip()

            if not response.strip():
                print("Invalid choice. Please select at least one choice.")
                continue

            if len(response) != len(set(response)):
                print("\n Duplicate criteria detected.")
                print("Please enter each pattern number only once")
                continue

            try:
                choice = int(response)

                if 1 <= choice <= len(reasons_list):
                    not_taken_reason = reasons_list[choice - 1]
                    print(reasons_list[choice-1])
                    break

                print("Invalid choice. Please select a valid option.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        #Valid decision
    while True:
        print("\n Do you believe this was a valid decision")
        print("1.Yes")
        print("2.No")

        response = input("Select an option:")

        if response == "1":
            valid_entry = "VALID"
            break
        elif response == "2":
            valid_entry = "INVALID"
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

    return valid_entry, trade_direction, daily_bias, trade_action, confirmation_patterns, not_taken_reason


def get_trade_data():
    #Entry date
    entry_data=get_date()

    #Entry time
    while True:
        time_input=input("\nEnter entry time (HH:MM):").strip()

        try:
            time_object=datetime.strptime(time_input, "%H:%M")
            entry_time=time_object.strftime("%H:%M")
            break
        except ValueError:
            print("Invalid time. please enter time is the correct format")

    # Confirmation timeframes
    while True:
        timeframe_input=input("Enter confirmation timeframe(s), separated by commas:")

        if timeframe_input.strip():
            confirmation_timeframe=[timeframe.strip() for timeframe in timeframe_input.split(",")
                                    if timeframe.strip()]

            if confirmation_timeframe:
               break

        print("Please enter at least one timeframe.")

      # What determined the trade ratio
    ratio_options=["1:5","1:6","2:1","Break of new structure","Target the middle of the level",
                   "Target the whole level", "Last pull back for SL","Below level for SL"]

    print("\nWhat determined the trading ratio?:")

    for number, option in enumerate(ratio_options, start=1):
        print(f'{number}, {option}')

    trade_ratio=None

    while True:
        response = input("\nSelect all applicable option numbers, separated by commas: ").strip()
        try:
           choices = [int(choice.strip()) for choice in response.split(",")]

           if not choices:
               print("Please select at least one option.")
               continue

           if len(choices) != len(set(choices)):
               print("\n Duplicate criteria detected.")
               print("Please enter each pattern number only once")
               continue

           if all(1 <= choice <= len(ratio_options) for choice in choices):
              trade_ratio = [ratio_options[choice - 1] for choice in choices]
              break
               
           print("One or more choices are invalid. Please select valid options.")

        except ValueError:
            print("invalid input Please enter numbers separated by commas.")

    #Price information
    entry_price = None
    tp_price = None
    sl_price = None
    while True:
        response=input("\nDO you want to enter the entry, TP and SL price? (yes/no):").strip().lower()

        if response in ("yes","no"):
            break
        print("Please enter yes or no.")

    if response== "yes":
      while True:
            try:
                entry_price = float(input("Enter entry price:"))
                tp_price = float(input('Enter TP price:'))
                sl_price = float(input('Enter Sl price:'))

                break

            except ValueError:
                    print("Please enter valid numbers.")


    return entry_data,entry_time, confirmation_timeframe, trade_ratio,entry_price,tp_price,sl_price


def get_trade_check_data():
    #FOLLOW MY RULES
    while True:
        followed_rules=input("Did you follow your trading rules?(yes/no):").strip().lower()

        if followed_rules in ("yes","no"):
            followed_rules=followed_rules.upper()
            break

        print("invalid input. Please enter yes or no")

    # SETUP SKEPTICISM
    while True:
        response=str(input("Were you skeptical about the trade setup? (yes/no):").strip().lower())

        if response=="no":
            setup_skepticism=None
            break

        if response=="yes":
            while True:
                reason=input("Why were you skeptical about the setup?:").strip().capitalize()

                if reason:
                   setup_skepticism=reason
                   break

                print("Please enter a reason ")

            break

        print("Invalid input. Please enter yes or no")

    while True:
        entry_timings=["ON_TIME","EALY","LATE","FOMO"]

        print("\n How did you think you enter the trade?")
        for number, timing in enumerate(entry_timings,start=1):
            print(f'{number},{timing}')

        try:
            choice=int(input("Enter choice:").strip())

            if 1<=choice<=len(entry_timings):
                entry_timing=entry_timings[choice-1]
                break
            print("invalid number.")

        except ValueError:
            print("enter in a number")

    return followed_rules, setup_skepticism, entry_timing

def not_taken_outcome():
    #Hypothetical trade ratio
    while True:
        hypothetical_trade_ratio=input("Enter the hypothetical trade ratio(e.g 1:5):").strip()

        if hypothetical_trade_ratio:
            break

        print("Please enter a hypothetical trade ratio.")

    #Hypothetical outcome
    outcomes=["TP","SL"]

    while True:
        print("\nWhat would have happened to the hypothetical trade?:")

        for number, outcome in enumerate(outcomes, start=1):
            print(f'{number}, {outcome}')

        try:
            choice=int(input("Enter choice:").strip())

            if 1<=choice<=len(outcomes):
                outcome=outcomes[choice-1]
                break
            print("invalid option.")

        except ValueError:
            print("Invalid input. Please enter a number")

    return hypothetical_trade_ratio,outcome



def get_trade_outcome_data():
    while True:
       print("\nSelect speculated daily candle result")
       print("1)bullish")
       print("2)bearish")
       try:
         speculated_daily_candle_result=input("Enter choice:").strip()

         if speculated_daily_candle_result=="1":
             speculated_daily_candle_result="bullish"
             break
         elif speculated_daily_candle_result=="2":
             speculated_daily_candle_result= "bearish"
             break
         else:
             print("Invalid choice. enter 1 or 2")

       except ValueError:
           print("You can only enter in a number")


    #OUTCOME
    outcomes=["TP","SL", "MANUAL_CLOSE"]

    while True:
        print("\nWhat was the trade outcome?")

        for number,outcomes in enumerate(outcomes, start=1):
            print(f'{number},{outcomes}')

        try:
            choice=int(input("Enter choice:").strip())

            if 1<=choice<=len(outcomes):
                outcome=outcomes[choice-1]
                break

            print("Invalid option. Select options available.")

        except ValueError:
              print("Invalid input. Please enter a number")

    #Manual close patterns
    if outcome== "manual_close":
        while True:
            pattern_input = input("\n Enter the manual close pattern(s), separated by commas:").strip()

            manual_close_pattern = [each_pattern.strip() for each_pattern in pattern_input.split(",") if each_pattern.strip()]

            if manual_close_pattern:
                break
            print("Please enter at least one pattern")
    else:
        manual_close_pattern=None

    #Maximum favorable movement
    while True:
        try:
          mfm=float(input("\nEnter maximum favorable movement value:"))

          if mfm:
            break
          print("Please enter in a value")
        except ValueError:
            print("Value most be a number")

    #Maximum adverse movement
    while True:
        try:
          mam=float(input("Enter maximum favorable movement value:").strip())

          if mam:
            break
          print("Please enter in a value")
        except ValueError:
            print("Please enter a number")

    return outcome,manual_close_pattern,mfm,mam,speculated_daily_candle_result

# LIFECYCLE CONTROL CHOICES

def get_lifecycle_action(setup_id, current_stage, next_stage):
    print(f'\nSetup_id: {setup_id}')
    print(f'Current stage:{current_stage.value}')

    if next_stage is None:
        print("Next stage: Lifecycle completed")
        print("Would you like to end the program?")
        print("1)End program")

        while True:
            choice= input("Enter choice:").strip()

            if choice=="1":
                return Actions.END

            print("invalid input")


    print(f'Next stages: {next_stage.value}')
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

def get_level_creation_choice(levels):
    if levels:
        print("\nHere are the levels already created:")
        for level in levels:
            print(level)

    print("\nDo you want to enter a new level?")
    user_response=input(">:")

    while user_response not in ["yes","no"]:
        print("response can only be yes or no")
        user_response = input(">:")

    if user_response == "yes":
         return True
    else:
        return False

def get_user_level_choice(key_zones):
    print("\nLevels created for this setup")

    for level in key_zones:
        print(f'level ID:{level[0]} |'
              f'Date:{level[3]} |'
              f'Timeframe:{level[4]} |'
              f'Type:{level[5]} |'
              f'Session {level[2]}'
              )

    while True:
        user_choice=input("\nEnter the level ID you want to continue with: ").strip()

        try:
            level_id= int(user_choice)
        except ValueError:
            print("Invalid Level ID")
            continue

        for level in key_zones:
            if level[0] == level_id:
                return level_id

        print("Level ID entered does not belong to this setup")

    return None


def display_error(error):
    print(f'Error:{error}')


if __name__ == "__main__":
    print(get_trade_data())
