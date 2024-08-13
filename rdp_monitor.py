import subprocess
import time
import re
import os
import threading

def sanitized_user(username):
    return re.sub(r'[.]','_', username)

# Function to monitor user sessions
def monitor_user(user):
    while True:
        # Run xrdp-sesadmin -c=list and check for the session
        session_output = subprocess.getoutput(f"su - {user} -c 'xrdp-sesadmin -c=list'")
        
        if not re.search(r'Display: :[0-9]+', session_output):
            print(f"No active session for {user}. Stopping monitoring.")
            del user_sessions[user]
            break

        display = re.search(r'Display: :[0-9]+', session_output).group().split(":")[-1]
        video_size = re.search(r'[0-9]+x[0-9]+', session_output).group()
        
        # Check if ffmpeg process is running for the user
        if not user_sessions[user]["ffmpeg_process"] or user_sessions[user]["ffmpeg_process"].poll() is not None:
            # Start ffmpeg process as the user
            filename = user_sessions[user]['filename']
            ffmpeg_command = f"ffmpeg -f x11grab -i :{display} -framerate 25 -video_size {video_size} -c:v h264 -crf 20 -preset ultrafast -f flv rtmp://<change with the rtmp server and application>/{filename}_{display} -y"
            print(f"Starting ffmpeg for user {user}: {ffmpeg_command}")
            user_sessions[user]["ffmpeg_process"] = subprocess.Popen(f"su - {user} -c \"{ffmpeg_command}\"", shell=True)

        # Check every 10 seconds
        time.sleep(10)

# Function to check for new Xvnc sessions
def monitor_sessions():
    while True:
        xvnc_output = subprocess.getoutput("ps aux | grep -i Xvnc")
        users = re.findall(r'/home/(.*?)/.vnc', xvnc_output)
        for user in users: 
            sanitized_users = sanitized_user(user)
            if user not in user_sessions:
                print(f"Detected new session for user {user}. Starting monitoring.")
                filename = f"{sanitized_users}_{time.strftime('%Y%m%d_%H%M%S')}"
                user_sessions[user] = {"filename": filename, "ffmpeg_process": None}
                threading.Thread(target=monitor_user, args=(user,)).start()
        
        time.sleep(10)

# Dictionary to store user sessions
user_sessions = {}

# Start monitoring for sessions
if __name__ == "__main__":
    monitor_sessions()
