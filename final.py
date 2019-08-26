from flask import Flask
from flask import request
from flask import make_response
from datetime import date
import json
import requests

app = Flask(__name__)
date=date.today().strftime('%Y%m%d')
@app.route('/webhook', methods=["GET","POST"])

def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    if(intent_name == 'Train_Information'):
        return Train_Information(req)
    if(intent_name == 'Cancelled_Trains'):
        return Cancelled_Trains(req)
    if(intent_name=='Live_Status'):
        return Live_Status(req)
    if (intent_name == 'PNR_Status'):
        return PNR_Status(req)
    if(intent_name=='Rescheduled_Trains'):
        return Rescheduled_Trains(req)
    return {}
def Live_Status(data):
    action = data['queryResult']['action']
    Date=data["queryResult"]["parameters"]['number']
    Train_Number=data["queryResult"]["parameters"]['TrainNumber']
    base_url = "http://indianrailapi.com/api/v2/livetrainstatus/apikey/b5ca80f0b179b6a6114d0ecfb8e9e90f/trainnumber/" + Train_Number + "/date/" + date + "/"
    api = requests.get(base_url).json()
    for i in api['TrainRoute']:
        StationName = i['StationName']
        ScheduledArrival = i['ScheduleArrival']
        ScheduleDeparture = i['ScheduleDeparture']
        str=" "
        str = str + "\n\nStation name :" + StationName + " \nScheduled arrival : " + ScheduledArrival + "\nScheduled departure: " + ScheduleDeparture
    if (action == "Text"):
        return Live_Text(str)
    return{}

def Live_Text(string):
    return{
        "fulfillmentText":"The train live schedule is" + string
        }

def Train_Information(data):

    action = data['queryResult']['action']
    Train_Number=data["queryResult"]["parameters"]["TrainNumber"]
    base_url = "http://indianrailapi.com/api/v2/TrainInformation/apikey/b5ca80f0b179b6a6114d0ecfb8e9e90f/TrainNumber/" + Train_Number + "/"
    api = requests.get(base_url).json()
    TrainName=api['TrainName']
    Source=api['Source']['Code']
    Destination=api['Destination']['Code']
    if (action == "Train_Information_Text"):
        return TextResponse(TrainName,Train_Number,Source,Destination)
    return {}

def TextResponse(Tr_Name,Tr_Num,Src,Dst):
    return{
        "fulfillmentText": "The train" + Tr_Num + " is " + Tr_Name + " from " + Src + " to " + Dst + "."
    }

def Cancelled_Trains(data):
    action = data["queryResult"]["action"]
    base_url = "https://indianrailapi.com/api/v2/CancelledTrains/apikey/b5ca80f0b179b6a6114d0ecfb8e9e90f/Date/" + date + "/"
    api = requests.get(base_url).json()
    TotalTrain=api['TotalTrain']
    LastUpdate=api['LastUpdate']
    if (action == "Text"):
        return Cancelled_Trains_Response(TotalTrain,LastUpdate)
    return {}

def Cancelled_Trains_Response(Tot_Tr,Lst_up):
    return {
        "fulfillmentText": "A Total of " + Tot_Tr + " is cancelled today and it was last updated at " + Lst_up
    }

def PNR_Status(data):
    action = data["queryResult"]["action"]
    PNR_Number=data["queryResult"]["parameters"]["pnr_number"]
    base_url="http://indianrailapi.com/api/v2/PNRCheck/apikey/b5ca80f0b179b6a6114d0ecfb8e9e90f/PNRNumber/" + PNR_Number + "/Route/1/"
    api = requests.get(base_url).json()
    TrainNumber=api['TrainNumber']
    TrainName=api['TrainName']
    JourneyClass=api['JourneyClass']
    JourneyDate=api['JourneyDate']
    if (action == "Text"):
        return PNR_Text(PNR_Number,TrainNumber,TrainName,JourneyClass,JourneyDate)
    return {}

def PNR_Text(PNR_num,Tr_Num,Tr_Name,J_Class,J_Date):
    return {
        "fulfillmentText": "The PNR Status for " + PNR_num + " for the train " + Tr_Name +" [ " + Tr_Num + " ] on " +J_Date + " . The Journey Class is " + J_Class
    }

def Rescheduled_Trains(data):
    action = data["queryResult"]["action"]
    base_url="https://indianrailapi.com/api/v2/RescheduledTrains/apikey/b5ca80f0b179b6a6114d0ecfb8e9e90f/Date/" + date + "/"
    api = requests.get(base_url).json()
    TotalTrain = api['TotalTrain']
    LastUpdate = api['LastUpdate']
    if (action == "Text"):
        return Rescheduled_text(TotalTrain, LastUpdate)
    return {}

def Rescheduled_text(Tot_Tr,Lst_Up):
    return {
        "fulfillmentText": "A Total of " + Tot_Tr + " is Rescheduled and it was last updated at " + Lst_Up
    }


if __name__ == '__main__':
    app.run(port=3000, debug=True)
