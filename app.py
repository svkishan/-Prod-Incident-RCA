from flask import Flask
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route("/")
def home():
    logging.info("Request received")
    try:
        # The business logic is now protected
        return "Application is running fine!"
    except Exception as e:
        logging.error(f"Incident detected: {str(e)}")
        return "Temporary issue, please retry", 500

if __name__ == "__main__":
    # Running on port 80 requires sudo/root privileges
    app.run(host="0.0.0.0", port=80)
