#property script_show_inputs

input string input_group = "Sync";   // Group name
input string template1 = "";         // Template name
input string template2 = "";         // Template name
input string template3 = "";         // Template name
input string template4 = "";         // Template name
input string template5 = "";         // Template name
input string template1_hotkey = "q"; // Template hotkey
input string template2_hotkey = "w"; // Template hotkey
input string template3_hotkey = "e"; // Template hotkey
input string template4_hotkey = "r"; // Template hotkey
input string template5_hotkey = "t"; // Template hotkey
input ENUM_TIMEFRAMES period1 = PERIOD_M5;
input ENUM_TIMEFRAMES period2 = PERIOD_M15;
input ENUM_TIMEFRAMES period3 = PERIOD_M30;
input ENUM_TIMEFRAMES period4 = PERIOD_H1;
input ENUM_TIMEFRAMES period5 = PERIOD_H2;
input ENUM_TIMEFRAMES period6 = PERIOD_H4;
input ENUM_TIMEFRAMES period7 = PERIOD_H6;
input ENUM_TIMEFRAMES period8 = PERIOD_D1;

int CUSTOM_EVENT_SYMBOL_CHANGE = 1;
int CUSTOM_EVENT_TEMPLATE_CHANGE = 2;

void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
  int symbol_change_event = CHARTEVENT_CUSTOM + CUSTOM_EVENT_SYMBOL_CHANGE;
  int template_change_event = CHARTEVENT_CUSTOM + CUSTOM_EVENT_TEMPLATE_CHANGE;

  if (id == symbol_change_event)
  {
    // use split to get symbol and group
    string split[2];
    StringSplit(sparam, '_', split);
    string symbol = split[0];
    string group = split[1];

    if (group != input_group)
    {
      return;
    }

    Print("Symbol changed: ", symbol, " for group: ", group);
    ChartSetSymbolPeriod(0, symbol, PERIOD_CURRENT);
    return;
  }

  if (id == template_change_event)
  {
    // use split to get symbol and group
    string split[2];
    StringSplit(sparam, '_', split);
    string tpl = split[0];
    string group = split[1];

    if (group != input_group)
    {
      return;
    }

    Print("Template changed: ", tpl, " for group: ", group);
    ChartApplyTemplate(0, tpl);
    return;
  }

  if (id == CHARTEVENT_KEYDOWN)
  {
    long key = lparam;
    Print("Key pressed: ", key);

    if (key == 81)
    {
      ChartApplyTemplate(0, template1);
      SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, template1 + "_" + input_group);
      return;
    }
    else if (key == 87)
    {
      ChartApplyTemplate(0, template2);
      SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, template2 + "_" + input_group);
      return;
    }
    else if (key == 69)
    {
      ChartApplyTemplate(0, template3);
      SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, template3 + "_" + input_group);
      return;
    }
    else if (key == 82)
    {
      ChartApplyTemplate(0, template4);
      SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, template4 + "_" + input_group);
      return;
    }
    else if (key == 84)
    {
      ChartApplyTemplate(0, template5);
      SendCustomEvent(CUSTOM_EVENT_TEMPLATE_CHANGE, template5 + "_" + input_group);
      return;
    }
    else if (key == 49)
    {
      ChartSetSymbolPeriod(0, Symbol(), period1);
      return;
    }
    else if (key == 50)
    {
      ChartSetSymbolPeriod(0, Symbol(), period2);
      return;
    }
    else if (key == 51)
    {
      ChartSetSymbolPeriod(0, Symbol(), period3);
      return;
    }
    else if (key == 52)
    {
      ChartSetSymbolPeriod(0, Symbol(), period4);
      return;
    }
    else if (key == 53)
    {
      ChartSetSymbolPeriod(0, Symbol(), period5);
      return;
    }
    else if (key == 54)
    {
      ChartSetSymbolPeriod(0, Symbol(), period6);
      return;
    }
    else if (key == 55)
    {
      ChartSetSymbolPeriod(0, Symbol(), period7);
      return;
    }
    else if (key == 56)
    {
      ChartSetSymbolPeriod(0, Symbol(), period8);
      return;
    }
    return;
  }  
}

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
  Print("Group: ", input_group);
  Print("Custom event: ", CUSTOM_EVENT_SYMBOL_CHANGE);
  Print("Custom: ", CHARTEVENT_CUSTOM);

  SendCustomEvent(CUSTOM_EVENT_SYMBOL_CHANGE, Symbol() + "_" + input_group);

  return (INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
}
//+------------------------------------------------------------------+