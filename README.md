# Session-Recording-RDP
A python script based on the Xrdp, ffmpeg to give live stream of the user session unattended in the background and also saves it in the media server.  

Note: Run media server locally or get enterprise edition of the ant media server for the rtmp link
Edit rtmp server link in the python script

### Installation & Setup

Step 1: Git clone the repo in the system

```git clone https://git.com/naman1102/Session-Recording-RDP.git```

```cd Session-Recording-RDP```

Step 2: Change the rtmp server link

```vi rdp-monitor.py```

```# /rtmp # in the vi editor search```

``` change the link with rtmp server ```

Step 3: Copy the rdp-monitor.py to the /usr/local/bin

```cp rdp_monitor.py /usr/local/bin/rdp_monitor.py```

Step 4: Copy the rdp-monitor.service to the /etc/systemd/system/

```cp rdp-monitor.service /etc/systemd/system/rdp-monitor.service```

Step 5: System Daemon Reload and start rdp-monitor service.

```systemctl daemon-reload```

```systemctl enable rdp-monitor.service```

```systemctl start rdp-monitor.service```

Step 6: Check the RDP monitor working

```systemctl status rdp-monitor.service```

### Support and Contribute

Feel free to fork and contribute. Let me know if there is any issue. Drop PR for the merge. Do follow and star the project if you like it.
