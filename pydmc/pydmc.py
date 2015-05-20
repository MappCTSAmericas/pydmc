"""
PyDMC API Client
"""
import requests

class DMC:
    def __init__(self,user,pwrd,host,v=5,content='json',accept='json'):
        self.user = user
        self.pwrd = pwrd
        self.host = "%s/api/rest/v%d" % (host,v)
        self.content = content
        self.accept = accept
        self.headers = {
            'content-type': 'application/%s' % content,
            'accept':       'application/%s' % accept
        }

    def get(self,domain,function,query=None):
        return requests.get(
            self._build_url(domain,function),
            auth=(self.user, self.pwrd),
            headers=self.headers,
            params=query
        )

        # if str(call.status_code)[0] == '2':
        #     return call
        # else:
        #     raise HttpError(call.status_code,call.reason)

    def post(self,domain,function,query=None,entity=None):
        return requests.post(
            self._build_url(domain,function),
            auth=(self.user, self.pwrd),
            headers=self.headers,
            params=query,
            data=entity
        )

        # if str(call.status_code)[0] == '2':
        #     return call
        # else:
        #     raise HttpError(call.status_code,call.reason)

    def _build_url(self,domain,function):
        return '%s/%s/%s' % (self.host,domain,function)


    def getAttributes(self):
        return self.get('meta','getAttributeDefinitions')


    def createAttributes(self,defs):
        return self.post('meta','createAttributeDefinitions',None,defs)


    def getUsedPersonalizations(self,messageId):
        query = {"messageId": messageId}
        call = self.get('message','getUsedPersonalizations', query)
        try:
            return call.json()
        except:
            print('Something has gone horribly wrong and you need to write an exception for it.')
            print(call)
            print(call.url)
            print(call.status_code)
            quit()
        finally:
            pass

    def getUserByEmail(self,email):
        query = {"email": email}
        # user = self.get('user','getByEmail',query).json()
        call = self.get('user','getByEmail',query)

        user = call.json()

        try:
            return User(user['id'],user['email'],user['mobileNumber'],user['identifier'])
        except:
            # TODO: add exception objects
            if user['errorCode'] == 'INVALID_PARAMETER':
                print("'%s' is an invalid value for '%s'. Please try again.") % (
                    user['value'],user['parameterName']
                )
            else:
                print('There was an error that you need an exception for.')
                quit()
        finally:
            pass


    def getUser(self,user_id):
        query = {"userId": user_id}
        # user = self.get('user','getByEmail',query).json()
        call = self.get('user','get',query)

        user = call.json()

        try:
            return User(user['id'],user['email'],user['mobileNumber'],user['identifier'])
        except:
            # TODO: add exception objects
            if user['errorCode'] == 'INVALID_PARAMETER':
                print("'%s' is an invalid value for '%s'. Please try again.") % (
                    user['value'],user['parameterName']
                )
                quit()
            else:
                print('There was an error that you need an exception for.')
                quit()
        finally:
            pass

    def updateProfileByEmail(self,email,attributes=None):
        query = {"email": email}
        if attributes:
            entity = "[%s]" % ",".join([ "%s" % a.json() for a in attributes ])
        else:
            entity = "null"

        return self.post('user','updateProfileByEmail',query,entity)


    def updateProfile(self,userId,attributes=None):
        query = {"userId": userId}
        if attributes:
            entity = "[%s]" % ",".join([ "%s" % a.json() for a in attributes ])
        else:
            entity = "null"

        call = self.post('user','updateProfile',query,entity)

        if call.status_code == 204:
            return True
        else:
            for a in attributes:
                print(a.json())

            print(call.headers)
            print(userId)
            print(attributes)
            print(call.url)
            print('There was an error that you need an exception for.')
            quit()


    def getPreparedMessages(self,groupId):
        query = {"groupId": groupId}

        return self.get('group','getPreparedMessages', query)


    def sendSingleMessage(self,recipientId,messageId,additionalContent='null'):
        query = {"recipientId": recipientId,"messageId": messageId}
        entity = additionalContent

        return self.post('message','sendSingle',query,entity)


class Attribute:
    def __init__(self,name,value):
        from dateutil import parser
        self.name = name
        if "date" in self.name.lower():
            d = parser.parse(value, fuzzy=True)
            value = d.isoformat()

        self.value = value

    def json(self):
        return '{"name":"%s","value":"%s"}' % (self.name,self.value)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.value)

    def __str__(self):
        return '%s: %s' % (self.name, self.value)


class Attachment:
    def __init__(self,name,contentType,content):
        import base64
        self.name = name
        self.contentType = contentType

        with open(content,'rb') as f:
            self.content = base64.b64encode(f.read())

    def json(self):
        return '{"name":"%s","contentType":"%s","content":"%s"}' % (self.name,self.contentType,self.content)


class MessageContent:
    def __init__(self,parameters=None,attachments=None):
        self.parameters = parameters
        self.attachments = attachments


class User:
    def __init__(self,id,email,mobileNumber,identifier):
        self.id = id
        self.email = email
        self.mobileNumber = mobileNumber
        self.identifier = identifier

    def json(self):
        return '{"name":"%s","value":"%s"}' % (self.name,self.value)

    def __unicode__(self):
        return 'DMC User: %d (%s)' % (self.id, self.email)

    def __str__(self):
        return unicode(self).encode('utf-8')


class DMCError(Exception):
    def __init__(self,errorActor,errorCode,message):
        self.errorActor = errorActor
        self.errorCode = errorCode
        self.message = message

    def __unicode__(self):
        return "[DMC Error] %s\n" % str(self.message)
    def __str__(self):
        return unicode(self).encode('utf-8')


class InvalidParameterError(DMCError):
    def __init__(self,errorActor,errorCode,message,parameterName,propertyName,value):
        self.parameterName = parameterName
        self.propertyName = propertyName
        self.value = value

    def __unicode__(self):
        print "%s %s %s %s %s %s\n" % (self.errorCode,self.errorActor,self.message,self.parameterName,self.propertyName,self.value)
        quit()

    def __str__(self):
        print "%s %s %s %s %s %s\n" % (self.errorCode,self.errorActor,self.message,self.parameterName,self.propertyName,self.value)
        quit()

