# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['AC6919b825005c39b1c46d590aeef7b510']
# auth_token = os.environ['9db5cf5f51f00df00a58e534109c6da1']
client = Client('AC6919b825005c39b1c46d590aeef7b510', '9db5cf5f51f00df00a58e534109c6da1')

message = client.messages.create(
                              body='Hi there, Fiverr here!',
                              from_='+18055153327',
                              to='+8801770001211'
                          )

print(message.sid)