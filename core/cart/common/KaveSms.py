from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, tokens: dict, template):
    """
        sending sms that needs template
    """
    try:
        api = KavenegarAPI(
            '43502F55745965686564474946647937784646345379377763726B2F535035694751356944707A6E7166593D'
        )
        params = {
            'receptor': receptor,
            'template': template,
        }
        for key, value in tokens.items():
            params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI(
            '43502F55745965686564474946647937784646345379377763726B2F535035694751356944707A6E7166593D')
        params_buyer = {
            'receptor': receptor,
            'message': message,
            'sender': '10005000505077'
        }
        response = api.sms_send(params_buyer)
        print(response)
    except APIException as e:
        print(e)
    except HTTPError as e:
        print(e)
