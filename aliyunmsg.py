from hashlib import sha1
import base64
import hmac
from datetime import *
import string, random
import urllib
from urllib import parse

def id_generator(size=6, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def percentEncode(string):
    return urllib.parse.quote(string, safe='-_.~')

# AccessKeyID = input('Your Access Key ID:')
# AccessKeySecret = input('Your Access Key Secret:')
# SignName = "AU/思存"
# TemplateCode = "SMS_18700766"
# RecNum = input('Target Phone number:')
# smsparam = input('SMS Param String with {}:')
AccessKeySecret = "testsecret"
smsparam = "{\"name\":\"d\",\"name1\":\"d\"}"
# "Format": "","Version": "2016-09-27",

timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

SignatureNonce = id_generator(16)

# Params = {"AccessKeyID":AccessKeyID, "Action":"SingleSendSms", "Format":"XML", "ParamString": smsparam, "RecNum": RecNum, "SignName": SignName, "SignatureMethod": "HMAC-SHA1", "SignatureNonce": SignatureNonce, "SignatureVersion":"1.0", "TemplateCode": TemplateCode, "Timestamp": timestamp, "Version":"2016-09-27"}
# Params = (("AccessKeyID",AccessKeyID), ("Action","SingleSendSms"), ("Format","XML"), ("ParamString", smsparam), ("RecNum", RecNum), ("SignName", SignName), ("SignatureMethod", "HMAC-SHA1"), ("SignatureNonce", SignatureNonce), ("SignatureVersion","1.0"), ("TemplateCode", TemplateCode), ("Timestamp", timestamp), ("Version","2016-09-27"))
Params = (("AccessKeyId","testid"), ("Action","SingleSendSms"), ("Format","XML"), ("ParamString", smsparam), ("RecNum", "13098765432"), ("RegionId","cn-hangzhou"), ("SignName", "标签测试"), ("SignatureMethod", "HMAC-SHA1"), ("SignatureNonce", "9e030f6b-03a2-40f0-a6ba-157d44532fd0"), ("SignatureVersion","1.0"), ("TemplateCode", "SMS_1650053"), ("Timestamp", "2016-10-20T05:37:52Z"), ("Version","2016-09-27"))

paramstr = ""
# Change param key and value
for item in Params:
    paramstr += percentEncode(item[0])
    paramstr += "="
    paramstr += percentEncode(item[1])
    paramstr += "&"

paramstr = paramstr[0:len(paramstr)-1]

StringToSign = "POST"+"&"+percentEncode('/')+"&"+percentEncode(paramstr)

# Calc Hmac sha1
secretKey = AccessKeySecret+"&"
hmac_obj = hmac.new(secretKey.encode('utf-8'), StringToSign.encode('utf-8'), sha1)
signature = percentEncode(base64.b64encode(hmac_obj.digest()).decode('utf-8'))


# Add Request Method
print("********PARAMS********")
print("SMS Param:", smsparam)
print("timestamp:", timestamp)
print("SignatureNonce:", SignatureNonce)
print("Params:", Params)
print("\nParam string:", paramstr)
print("\nString to sign:", StringToSign)
print("********RESULT********")
print("Signature:",signature)
# print(urllib.parse.urlencode(Params))
# param_name =
# param_meeting_name =
# param_meeting_time =
# param_meeting_place =
# param_meeting_req =
