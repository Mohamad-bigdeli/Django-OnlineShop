from kavenegar import *

def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI('ApiKey')
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
