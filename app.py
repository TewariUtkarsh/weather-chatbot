import json
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
# Package to fetching data from open weather api
import os
import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

app = Flask(__name__)
CORS(app)

api_key = '89021cdbaab75b66c97cbdd395a9d1be'
owm = pyowm.OWM(api_key)
mgr = owm.weather_manager()


# Getting and sending response to dialogFlow
@app.route('/webhook', methods='POST')
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    print(f"Request: {json.dumps(req)}")

    res = processRequest(req)

    res = json.dumps(res)
    print(f"{res}")

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r



def processRequest(req):
    result = req.get('queryResult')
    print(result)

    params = result.get('parameters')

    city = params.get('city')

    observation = mgr.weather_at_place(str(city))
    print(observation)

    w = observation.weather

    wind_res = w.wind()
    wind_speed = str(wind_res['speed'])

    humid = str(w.humidity)

    celsius_res = w.temperature('celsius')
    temp_min_cel = str(celsius_res['temp_min'])
    temp_cel = str(celsius_res['temp'])
    temp_max_cel = str(celsius_res['temp_max'])

    fahrenheit_res = w.temperature('fahrenheit')
    temp_min_fahrenheit = str(fahrenheit_res['temp_min'])
    temp_far = str(fahrenheit_res['temp'])
    temp_max_fahrenheit = str(fahrenheit_res['temp_max'])

    # lat_lon_res = observation.get_location()
    # lat = str(lat_lon_res.get_lat())
    # lon = str(lat_lon_res.get_lon())

    deg = u"\N{DEGREE SIGN}"

    speech = f"Today the weather is {str(city)}\nHumidity: {str(humid)}\nWind Speed: {str(wind_speed)}\n" \
             f"Temperature: \nTemp: {temp_cel}{deg}C / {temp_far}{deg}F\nMin. Temp: {temp_min_cel}{deg}C / {temp_min_fahrenheit}{deg}F\nMax. Temp: {temp_max_cel}{deg}C / {temp_max_fahrenheit}{deg}F"


    return {
        "fulfillmentText": speech,
        "displayText": speech
    }


if __name__ == '__main__':
    app.run(debug=True)



'''
# ---------- FREE API KEY examples ---------------------

mgr = owm.weather_manager()

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
answer = forecast.will_be_clear_at(timestamps.tomorrow())
'''

'''
{
  "responseId": "6d8a2c40-5dad-442b-b7f3-3811f66bd662-5a74d3f9",
  "queryResult": {
    "queryText": "Hey there",
    "action": "input.welcome",
    "parameters": {},
    "allRequiredParamsPresent": true,
    "fulfillmentText": "Hi! How are you doing?",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Hi! How are you doing?"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/first-dl-agent-tdgw/locations/global/agent/intents/d89cf32a-6ec8-4297-960c-c6621ccab7a4",
      "displayName": "Default Welcome Intent"
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en",
    "sentimentAnalysisResult": {
      "queryTextSentiment": {
        "score": 0.2,
        "magnitude": 0.2
      }
    }
  },
  "alternativeQueryResults": [
    {
      "queryText": "Hey there",
      "languageCode": "en",
      "sentimentAnalysisResult": {
        "queryTextSentiment": {
          "score": 0.2,
          "magnitude": 0.2
        }
      }
    }
  ],
  "agentId": "e42512f7-51bb-42c1-a551-a59695f57079",
  "agentSettings": {
    "enableAgentWideKnowledgeConnector": true
  }
}
'''
