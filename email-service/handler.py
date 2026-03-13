import json
import resend

resend.api_key = "re_D4RQMrgF_ABo2PfXpU8eMYQwPMJXNF5MU"


def send_email(event, context):

    try:
        body = json.loads(event["body"])

        action = body["action"]
        email = body["email"]

        if action == "SIGNUP_WELCOME":
            subject = "Welcome to HMS"
            message = "Thank you for signing up!"

        elif action == "BOOKING_CONFIRMATION":
            doctor = body["doctor"]
            date = body["date"]
            time = body["time"]

            subject = "Appointment Confirmation"
            message = f"Your appointment with Dr {doctor} is confirmed on {date} at {time}"

        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["blackdevil0123456@gmail.com"],
            "subject": subject,
            "text": message
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"})
        }

    except Exception as e:

        print("Email error:", e)

        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }