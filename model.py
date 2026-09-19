class Setup:
    def __init__(self, strategy, market_pair, long_htf_direction, short_htf_direction, market_condition, candle_bias, date):
        #CHECKING DATA ENTER
        if strategy not in ["supply and demand","return-to-origin-reversal"]:
            raise ValueError("Value enter is not part of strategy available")
        if long_htf_direction not in ["short", "long"] or short_htf_direction not in ["short", "long"]:
            raise ValueError("HTF direction can only  bullish or bearish")
        if candle_bias not in ["bullish", "bearish","unsure"]:
            raise ValueError("HTF direction can only be up or down")
        if market_condition not in ["trending", "ranging", "transitioning"]:
            raise ValueError("market condition must be trending,ranging or transitioning")


        self.trade_strategy=strategy
        self. market_pair= market_pair
        self.long_htf_direction=long_htf_direction
        self.short_htf_direction=short_htf_direction
        self.htf_next_three_candle=candle_bias
        self.market_condition=market_condition
        self.date_created=date


class Level:
    def __init__(self,session,time_frame,level_criteria,level_type,date,setup_id):
        self.setup_id=setup_id
        self.session_created=session
        self.date_created=date
        self.timeframe=time_frame
        self.criteria=level_criteria
        self.level_type=level_type

#class LevelINTERACTION:
#    def __init__(self,):




