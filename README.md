# -Prod-Incident-RCA

Simulated Production Incident & RCA 
 PART 1: Create EC2 Ubuntu Instance
Step 1: Launch EC2

AWS Console → EC2

Launch Instance

Name: incident-lab

AMI: Ubuntu Server 22.04 LTS

Instance type: t2.micro (free tier)

Key pair → Create or select

Security Group:

Allow SSH (22) from your IP

Allow HTTP (80) from Anywhere

Launch instance

Step 2: Connect to EC2

From your local terminal:

ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

 PART 2: Prepare the Server
Update system
sudo apt update && sudo apt upgrade -y

Install Python & tools
sudo apt install python3 python3-pip -y

 PART 3: Deploy a Buggy App (Simulated Incident)

We’ll create a Python web app that:

Sometimes works

Sometimes crashes randomly 

Step 1: Create app directory
mkdir buggy-app
cd buggy-app

Step 2: Create the buggy app
nano app.py


from flask import Flask
import random
import time
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route("/")
def home():
    logging.info("Request received")

    # Random failure (production incident simulation)
    if random.choice([True, False]):
        logging.error("Random failure occurred!")
        raise Exception("App crashed due to random error")

    return "Application is running fine!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


Save → CTRL+O, Enter → CTRL+X

Step 3: Install Flask
pip3 install flask

Step 4: Run the app
sudo python3 app.py

 PART 4: Reproduce the Incident
Open browser:
http://<EC2_PUBLIC_IP>

What you’ll see:

Sometimes:
 Application is running fine!

Sometimes:
 Internal Server Error

  You have reproduced a production issue.

 PART 5: Capture Logs (Very Important)

Open a new SSH session or stop app with CTRL+C

View logs
cat app.log


You’ll see entries like:

INFO Request received
ERROR Random failure occurred!

 PART 6: Debug & Explain the Issue
What is happening?

App randomly crashes

Users see intermittent failures

Logs show Random failure occurred

Why is this dangerous?

Unpredictable outages

Poor user experience

Hard to detect without logs

 PART 7: Root Cause Analysis (RCA)

Below is simple RCA documentation you can submit or explain in interviews.

📄 ROOT CAUSE ANALYSIS (RCA)
Incident Title:

Random Application Crash in Production

Incident Summary:

The application intermittently returned 500 Internal Server Error to users.

Impact:

Users experienced random downtime

Service reliability reduced

No consistent reproduction without logs

Timeline:
Time	Event
App deployed	App started successfully
User traffic	Random failures observed
Logs checked	Error logs detected
Root cause found	Random crash logic
Root Cause:

The application contained intentional random failure logic:

if random.choice([True, False]):
    raise Exception("App crashed")


This caused the app to crash unpredictably during requests.

Detection:

Application logs (app.log)

HTTP 500 errors observed by users

Resolution (Proposed Fix):

Remove random failure logic

Add proper error handling

Implement monitoring and alerts

Preventive Measures:

Code review before deployment

Add health checks

Add monitoring (Prometheus / CloudWatch)

Enable structured logging

 PART 8: Proposed Fix (Beginner Level)
Fixed code snippet:
try:
    # business logic
    return "Application is running fine!"
except Exception as e:
    logging.error(str(e))
    return "Temporary issue, please retry", 500
