from device_registry import app
#import os

#import asyncio
#from kasa import Discover

app.run(host='0.0.0.0', port=3000, debug=True)

#with open("testfile2", 'w') as f:
#    output = os.system("ping -c 3 192.168.8.106")
#    f.write(str(output))

#devices = asyncio.run(Discover.discover())
#for addr, dev in devices.items():
#    asyncio.run(dev.update())
#    print(f"{addr} >> {dev}")
