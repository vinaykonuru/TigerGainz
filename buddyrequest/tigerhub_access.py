import hashlib
import random
from base64 import b64encode
from datetime import datetime

def getStudentInfo(id):
    url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates/' + id
    created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
    username = 'vkonuru'
    password = 'e98c0aa0a289b517f8073984777d94e5'

    generated_digest = b64encode(hashlib.sha256((nonce + created + password).encode('utf-8')).digest()).decode('utf-8')

    r = requests.get(url, headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (username, generated_digest, b64encode(nonce.encode()).decode('utf-8'), created)
    })
    return r.json()
