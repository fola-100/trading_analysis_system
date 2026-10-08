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

class LevelInteraction:
    def __init__(self,level_id,date,session,price_movement):
        self.level_id=level_id
        self.date_price_reach=date
        self.session=session
        self.interaction_on_level=price_movement

class EntryOpportunity:
    def __init__(self,level_interaction_id, valid_entry,trade_direction,daily_bias,
                 trade_action, confirmation_pattern, not_taken_reason):

        self.level_interaction_id=level_interaction_id
        self.valid_entry= valid_entry
        self.trade_direction=trade_direction
        self.daily_bias= daily_bias
        self.trade_action=trade_action
        self.confirmation_patterns=confirmation_pattern
        self.not_taken_reason=not_taken_reason

class  TRADE:
    def __init__(self,opportunity_id,date,time,time_frame,trade_ratio,entry_value,tp_value,sl_value):
        self.opportunity_id=opportunity_id
        self.entry_date=date
        self.time=time
        self.confirmation_timeframe=time_frame
        self.trade_ratio=trade_ratio
        self.entry_value=entry_value
        self.tp_value=tp_value
        self.sl_value=sl_value


class TradeChecks:
    def __init__(self,trade_id,followed_rules,setup_skepticism,entry_timing):
        self.trade_id=trade_id
        self.followed_rules=followed_rules
        self.setup_skepticism=setup_skepticism
        self.entry_timing = entry_timing

class TradeOUTCOME:
    def __init__(self,trade_id,outcome,manual_close_pattern,mfm,mam,daily_candle_result):
        self.trade_id=trade_id
        self.outcome=outcome
        self.manual_close_pattern=manual_close_pattern
        self.maximum_favorable_movement=mfm
        self.maximum_adverse_movement=mam
        self.daily_candle_result=daily_candle_result

class NoTradeOutcome:
    def __init__(self,opportunity_id,outcome,trade_ratio):
        self.opportunity_id=opportunity_id
        self.hypothetical_trade_ratio=trade_ratio
        self.outcome=outcome







