#property script_show_inputs

// input bool master = false;                                                     // Master or slave
input string group = "Sync";                                                   // Group name
input string templates = "cho,demarker,stochastic,MACD,rsi,momentum,tema,atr"; // template names, separated by comma
input string template_hotkeys = "Q,W,E,R,T,Y,U,I";                             // hot keys separated by comma
input string periods = "M5,M15,M30,H1,H2,H4,H6,D";                             // periods separated by comma
input string period_hotkeys = "1,2,3,4,5,6,7,8";                               // hot keys separated by comma

int CUSTOM_EVENT_SYMBOL_CHANGE = 1;
int CUSTOM_EVENT_TEMPLATE_CHANGE = 2;

/// @brief On change symbol event
/// @param data
void OnChangeSymbolEvent(const string &data)
{
  Print("OnChangeSymbolEvent: ", data);
  string split[];
  int length = StringSplit(data, '_', split);

  if (length != 2)
  {
    Print("Invalid data: ", data);
    return;
  }

  string change_symbol = split[0];
  string change_group = split[1];

  if (group != change_group)
  {
    return;
  }

  Print("Symbol changed: ", change_symbol, " for group: ", change_group);
  ChartSetSymbolPeriod(0, change_symbol, PERIOD_CURRENT);
}

/// @brief On template change event
/// @param data
void OnTemplateChangeEvent(const string &data)
{
  Print("OnTemplateChangeEvent: ", data);
  string split[];
  int length = StringSplit(data, '_', split);

  if (length != 2)
  {
    Print("Invalid data: ", data);
    return;
  }

  string change_template = split[0];
  string change_group = split[1];

  if (group != change_group)
  {
    return;
  }

  Print("Template changed: ", change_template, " for group: ", change_group);
  ChartApplyTemplate(0, change_template);
}

/// @brief On key down event
/// @param key
void OnKeydownEvent(const long &key)
{
  Print("Key pressed: ", IntegerToString(key));

  // split templates
  string tpl_split[];
  int tpl_length = StringSplit(templates, ',', tpl_split);

  // split template_hotkeys
  string tpl_hotkey_split[];
  int tpl_hotkey_length = StringSplit(template_hotkeys, ',', tpl_hotkey_split);

  if (tpl_length != tpl_hotkey_length)
  {
    Print("Invalid template_hotkeys: ", template_hotkeys);
    return;
  }

  // split periods
  string period_split[];
  int period_length = StringSplit(periods, ',', period_split);

  // split period_hotkeys
  string period_hotkey_split[];
  int period_hotkey_length = StringSplit(period_hotkeys, ',', period_hotkey_split);

  if (period_length != period_hotkey_length)
  {
    Print("Invalid period_hotkeys: ", period_hotkeys);
    return;
  }

  // compare the key with the hotkeys
  for (int i = 0; i < tpl_length; i++)
  {
    if (key != StringGetCharacter(tpl_hotkey_split[i], 0))
      continue;

    Print("Apply template: ", tpl_split[i]);
    ChartApplyTemplate(0, tpl_split[i]);
    SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, tpl_split[i] + "_" + group);
    return;
  }

  // compare the key with the hotkeys
  for (int i = 0; i < period_length; i++)
  {
    if (key != StringGetCharacter(period_hotkey_split[i], 0))
      continue;

    Print("Apply period: ", period_split[i]);
    ChartSetSymbolPeriod(0, Symbol(), MapTimeframe(period_split[i]));
    return;
  }
}

ENUM_TIMEFRAMES MapTimeframe(const string &period)
{
  if (period == "M1")
    return PERIOD_M1;
  if (period == "M2")
    return PERIOD_M2;
  if (period == "M3")
    return PERIOD_M3;
  if (period == "M4")
    return PERIOD_M4;
  if (period == "M5")
    return PERIOD_M5;
  if (period == "M6")
    return PERIOD_M6;
  if (period == "M10")
    return PERIOD_M10;
  if (period == "M12")
    return PERIOD_M12;
  if (period == "M15")
    return PERIOD_M15;
  if (period == "M20")
    return PERIOD_M20;
  if (period == "M30")
    return PERIOD_M30;
  if (period == "H1")
    return PERIOD_H1;
  if (period == "H2")
    return PERIOD_H2;
  if (period == "H3")
    return PERIOD_H3;
  if (period == "H4")
    return PERIOD_H4;
  if (period == "H6")
    return PERIOD_H6;
  if (period == "H8")
    return PERIOD_H8;
  if (period == "H12")
    return PERIOD_H12;
  if (period == "D")
    return PERIOD_D1;
  if (period == "W")
    return PERIOD_W1;
  if (period == "MN")
    return PERIOD_MN1;

  return PERIOD_CURRENT;
}

/// @brief On chart event
/// @param id
/// @param lparam
/// @param dparam
/// @param sparam
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
  int symbol_change_event = CHARTEVENT_CUSTOM + CUSTOM_EVENT_SYMBOL_CHANGE;
  int template_change_event = CHARTEVENT_CUSTOM + CUSTOM_EVENT_TEMPLATE_CHANGE;

  if (id == symbol_change_event)
  {
    OnChangeSymbolEvent(sparam);
    return;
  }

  if (id == template_change_event)
  {
    OnTemplateChangeEvent(sparam);
    return;
  }

  // if (!master)
  // {
  //   Print("Not master, ignoring event: ", id);
  //   return;
  // }

  if (id == CHARTEVENT_KEYDOWN)
  {
    OnKeydownEvent(lparam);
    return;
  }
}

/// @brief Send custom event to all charts
/// @param event_id
/// @param event_data
void SendCustomEvent(const int event_id, const string event_data)
{

  // iterate through all charts and set custom event
  long chart_id = ChartFirst();
  while (chart_id > 0)
  {
    EventChartCustom(chart_id, event_id, 0, 0, event_data);
    chart_id = ChartNext(chart_id);
  }
}

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
  Print("Group: ", group);

  // only send out events if this is the master
  // if (master)
  SendCustomEvent(CUSTOM_EVENT_SYMBOL_CHANGE, Symbol() + "_" + group);

  return (INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
}
//+------------------------------------------------------------------+