import json
import decimal 

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None    

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}

def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def custService(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    custNum = get_slot(intent_request, 'custNum1')
    #custNum holds the customer number intent.
    #check that it matches account
    text = "Thank you. The callback number I have is "+custNum+". A customer service specialist will be with you shortly. "
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)   

def techSupport(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    custNum = get_slot(intent_request, 'PhoneNumberCust')
    #custNum holds the customer number intent.
    #check that it matches account
    
    text = "Thank you. The callback number I have is "+custNum+". A technical support specialist will be with you shortly. "
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def billingSupport(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    custName1 = get_slot(intent_request, 'custName')
    #custName holds the customer name slot.
    #check that it matches account
    
    text = "Thank you for your payment "+custName1+"! You will receive an email conformation shortly. For additional help enter 'more options'. Otherwise, thank you and have a great day!"
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def newModemConfig(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    serialNumber = get_slot(intent_request, 'SerialNum')
    #serialNum holds the modem serial number.
    text = "Your modem with Serial Number: "+serialNumber+" is now ready for use. If you need further assistance enter 'more options'. If not, have a great day and thank you for being a Z-finity customer!"
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def upgradeServ(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    internetSpeed = get_slot(intent_request, 'speed')
    #serialNum holds the modem serial number.
    text = "Okay your service has been upgraded to "+internetSpeed+", that is fast!. You will receive an email confirmation of the changes and prorated charges. For additional help enter 'more options'. Otherwise, thank you and have a great day!"
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    fulfillment_state = "Fulfilled"    
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to your bot's intent handlers
    if intent_name == 'CustomerSupportHelper':
        return custService(intent_request)
    elif intent_name == 'TechSupportHelper':
        return techSupport(intent_request)
    elif intent_name == 'BillingHelper':
        return billingSupport(intent_request)
    elif intent_name == 'NewModemHelper':
        return newModemConfig(intent_request)
    elif intent_name == 'UpgradeServiceHelper':
        return upgradeServ(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    response = dispatch(event)
    return response