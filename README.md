# guilded-user
A Api wrapper for guilded user api 
Example
```python
import guilded_user as guilded
from time import sleep


client = guilded.client.Client()

client.login("email@gmail.com", "mysupersecurepassword")

channel = "channel_id"
    
msg = client.send_message(channel,"Test message")

sleep(1)

msg.edit("Editing a message!")

sleep(1)

msg.delete()
```
