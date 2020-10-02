import re

st = "ANIRUDH GOUTHAM +91 8000848783  382424"

def mobile_no(original):
    pattern = r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[\ -]?){10}\d$'
    numbers = re.findall(pattern,original)
    updatedOG = re.sub(pattern,'',original)
    return numbers,updatedOG,original

contacts,newOG,_ = mobile_no(st)
print(contacts,newOG)
def pincode(original):
    pattern = r'([0-9]{6}|[0-9]{3}\s[0-9]{3})'
    pincodes = re.findall(pattern,original)
    updatedOG = re.sub(pattern,'',original)
    return pincodes,updatedOG,original    

pincode,newOG,_ = pincode(newOG)
print(pincode,newOG)

def email(original):
    pattern = r''
    emails = re.findall(pattern,original)
    updatedOG = re.sub(pattern,'',original)
    return emails,updatedOG,original    

def city(original):
    pass