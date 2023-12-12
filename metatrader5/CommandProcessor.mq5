//+------------------------------------------------------------------+
//|                                                   CommandProcessor.mq5 |
//|                                  Copyright 2023, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, MetaQuotes Ltd."
#property link "https://www.mql5.com"
#property version "1.00"
#include <Socket.mqh>
#include <JSON.mqh>
#include <Trade\Trade.mqh>

input string hostname = "trading.local.com";
input int port = 9355;

CTrade trade;

ClientSocket *connection = NULL;

struct SymbolStruct
{
   long tick_time;
   string name;
};

SymbolStruct SubscribedSymbols[];

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   //---
   bool result = ConnectSocket();
   if (!result)
   {
      Print("Failed to connect to socket");
      return (INIT_FAILED);
   }

   Print("Connected to socket");

   if (!EventSetMillisecondTimer(200))
   {
      Print("Failed to set timer");
      return (INIT_FAILED);
   }

   // Testing subscribe functions
   // SymbolStruct symbol;
   // symbol.name = "EURUSD";
   // symbol.tick_time = GetLastTick(symbol.name).time_msc;
   // ArrayResize(SubscribedSymbols, 1);
   // SubscribedSymbols[0] = symbol;

   //---
   return (INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("Deinit: " + reason);
   //---
   delete connection;
   connection = NULL;

   //--- destroy timer
   EventKillTimer();
}
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   //---
}

void OnTimer()
{
   if (!connection)
      ConnectSocket();
   if (!connection.IsSocketConnected())
   {
      Print("Socket disconnected");
      ConnectSocket();
   }
   else
   {
      ReceiveMessage();
   }
}
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
   //---
}
//+------------------------------------------------------------------+

bool ConnectSocket()
{
   if (connection) // Socket already exists
   {
      delete connection;
      connection = NULL;
   }

   // Create a socket if none already exists
   connection = new ClientSocket(hostname, port);

   if (connection.IsSocketConnected())
   {
      // Socket is okay. Do some action such as sending or receiving
      return true;
   }

   return false;
}

void ReceiveMessage()
{
   string data = connection.Receive("\x03");
   if (data != "")
   {
      Print("Received data: " + data);

      CJAVal json(NULL, jtUNDEF);
      bool success = json.Deserialize(data);

      // Failed parsing data.
      if (!success)
      {
         Print("Failed to parse JSON", data);
         return;
      }
      else
      {
         string msgType = json["type"].ToStr();
         CJAVal *payload = json["payload"];

         if (msgType == "MESSAGE")
            HandleMessage(payload);
         else if (msgType == "REQUEST")
            HandleRequest(json["id"].ToStr(), payload);
         else
            Print("Unknown message type: " + msgType);
      }
   }
}

void HandleMessage(CJAVal *payload)
{
   string msg = payload.ToStr();
   Print("Message: " + msg);
}

void HandleRequest(string id, CJAVal *payload)
{
   string payloadType = payload["type"].ToStr();
   Print("Request: " + payloadType);

   if (payloadType == "AUTHORIZE")
   {
      Print("Authorize request");
      CJAVal payload(NULL, jtOBJ);
      payload["success"] = true;
      payload["command"] = true;
      SendResponse(id, &payload);
   }
   else if (payloadType == "LAST_CANDLES")
   {
      string symbolName = payload["symbol"].ToStr();
      int n_candles = payload["n_candles"].ToInt();
      string timeframe = payload["timeframe"].ToStr();

      MqlRates rates[];
      int n_rates = GetLastCandles(symbolName, timeframe, n_candles, rates);
      SendResponse(id, &RatesToJSON(rates));
   }
   else
   {
      Print("Unknown request type: " + payloadType);
      CJAVal responsePayload(NULL, jtOBJ);
      responsePayload["error"] = "Unknown request type: " + payloadType;
      SendResponse(id, &responsePayload);
   }
}

void SendResponse(string id, CJAVal *payload)
{
   CJAVal response;
   response["id"] = id;
   response["type"] = "RESPONSE";
   response["payload"].Set(payload);
   connection.Send(response.Serialize() + "\x03");
}

ENUM_TIMEFRAMES TimeframeToPeriod(string timeframe)
{
   if (timeframe == "5Min")
      return PERIOD_M5;
   else if (timeframe == "15Min")
      return PERIOD_M15;
   else if (timeframe == "30Min")
      return PERIOD_M30;
   else if (timeframe == "1H")
      return PERIOD_H1;
   else if (timeframe == "2H")
      return PERIOD_H2;
   else if (timeframe == "4H")
      return PERIOD_H4;
   else if (timeframe == "6H")
      return PERIOD_H6;
   else
      return PERIOD_CURRENT;
}

int GetLastCandles(string symbol, string timeframe, int n_candles, MqlRates &rates[])
{
   int n_rates = CopyRates(symbol, TimeframeToPeriod(timeframe), 0, n_candles, rates);
   return n_rates;
}

CJAVal RatesToJSON(MqlRates &rates[])
{
   CJAVal json(NULL, jtARRAY);
   for (int i = 0; i < ArraySize(rates); i++)
   {
      CJAVal candle(NULL, jtOBJ);
      candle["open"] = rates[i].open;
      candle["high"] = rates[i].high;
      candle["low"] = rates[i].low;
      candle["close"] = rates[i].close;
      candle["time"] = (string)rates[i].time;
      json.Add(candle);
   }
   return json;
}