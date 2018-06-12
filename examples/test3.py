import time
i = 0
while True:
    print("TEST 3 | {}".format(i))
    i += 1
    time.sleep(1)

'''
[Unit]
Description=Sonarr Daemon
After=network.target

[Service]
User=nzbdrone
Group=nzbdrone

Type=simple
ExecStart=/usr/bin/mono /opt/NzbDrone/NzbDrone.exe -nobrowser
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
'''
