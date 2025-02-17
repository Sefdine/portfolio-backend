import os
from flask_cors import CORS
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable CORS for this origin
# local_url = "http://localhost:3000"
public_url = "https://likenassuf.vercel.app"

CORS(app, resources={r"/submit-form": {"origins": public_url}})


SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')  # Set your SendGrid API key in environment variables

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not email or not subject or not message:
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Send email using SendGrid
        send_email(email, subject, message)
        return jsonify({"message": "Form submitted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_email(sender_email, subject, message_body):
    # Create a SendGrid Mail object
    subject_to_send = "Like Portfolio, new msg : "+subject
    from_email = Email("nassuf.sefdine@10000codeurs.com")  # Your SendGrid registered email
    to_email = To("nassuf.sefdine12@gmail.com")  # Destination email
    content = Content("text/plain", f"Sender Email: {sender_email}\n\nMessage:\n{message_body}")
    mail = Mail(from_email, to_email, subject_to_send, content)

    # Initialize SendGrid client and send the email
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.send(mail)

    # Log the response for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")
    print(f"Response Headers: {response.headers}")

if __name__ == '__main__':
    app.run(debug=True)
