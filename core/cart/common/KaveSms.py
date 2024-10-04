from kavenegar import *

def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI('43502F55745965686564474946647937784646345379377763726B2F535035694751356944707A6E7166593D')
        params = {
            'sender': '',#optional
            'receptor': receptor,#multiple mobile number, split by comma
            'message': message,
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)