# -*- coding: utf-8 -*-
from hashlib import sha1
import base64
import hmac
from datetime import *
import string, random
import urllib
from urllib import parse
import requests

import urllib.request
import http.client

def id_generator(size=6, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def percentEncode(string):
    return urllib.parse.quote(string, safe='-_.~')

def getReqString(key, value):
    return key + "=" +value


# SETTING AREA

# SET YOUR ACCESS KEY ID and ACCESS KEY SECRET
AccessKeyID = "YourAccessKeyID"
AccessKeySecret = "YourAccessKeySecret"


# SET Your SMS signature, must be audited
SignName = "YOURSignature"

# SET Your Template Code, must be audited
TemplateCode = "SMS_21310051"


RecNum = input('Target Phone number:')
smsparam = input('SMS Param String with {}:')

# sms param example:
# {"name": "value", "name2", "value2"}


# Random string
SignatureNonce = id_generator(16)

# Timestamp GMT
timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

Params = (("AccessKeyId",AccessKeyID), ("Action","SingleSendSms"), ("Format","XML"), ("ParamString", smsparam), ("RecNum", RecNum), ("RegionId","cn-hangzhou"), ("SignName", SignName), ("SignatureMethod", "HMAC-SHA1"), ("SignatureNonce", SignatureNonce), ("SignatureVersion","1.0"), ("TemplateCode", TemplateCode), ("Timestamp", timestamp), ("Version","2016-09-27"))

paramstr = ""
reqstr=""

# Change param key and value, generate request/Paramstring
for item in Params:
    paramstr = paramstr+getReqString(percentEncode(item[0]), percentEncode(item[1]))
    paramstr += "&"
    reqstr = reqstr+getReqString(item[0], item[1])
    reqstr += "&"

paramstr = paramstr[0:len(paramstr)-1]
reqstr = reqstr[0:len(reqstr)-1]

StringToSign = "POST"+"&"+percentEncode('/')+"&"+percentEncode(paramstr)

# Calculate Signature, HMAC-SHA1
secretKey = AccessKeySecret+"&"
hmac_obj = hmac.new(secretKey.encode('utf-8'), StringToSign.encode('utf-8'), sha1)
signature = percentEncode(base64.b64encode(hmac_obj.digest()).decode('utf-8'))


print("\n********RESULT********")
reqbody = "Signature="+signature+"&"+reqstr
print("Request Body:")
print(reqbody)

print("*****SENDING REQUEST*****")
print("Method:","POST")
headerdata = {
"Content-Type": "application/x-www-form-urlencoded",
"charset": "utf-8"
}
conn = http.client.HTTPSConnection('sms.aliyuncs.com')
reqbody = "Signature="+signature+"&"+reqstr
conn.request(method='POST', url='https://sms.aliyuncs.com/', body=reqbody.encode('utf-8'), headers=headerdata)
response=conn.getresponse()
res=response.read()
print(res)
