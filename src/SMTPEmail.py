import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendEmail:
    def __init__(self, filename, email):
        """
        Initialise SendEmail class.

        :param filename: Filename created by EC2Prediction
        :param email: User email.
        """
        self.filename = filename
        email = email.replace("-fullstop-", ".")
        self.useremail = email.replace("-atsymbol-", "@")
        self.senderemail = "wekohealth@gmail.com"
        self.password = "LcVS8f55e#JT"

    def write_email(self):
        """
        Writes and sends email to user.
        """
        message = MIMEMultipart("alternative")
        username = self.useremail.split("@", 1)[0]
        message["Subject"] = f"WeKo Walking Analysis Results for {username}"
        message["From"] = self.senderemail
        message["To"] = self.useremail
        print(f"Preparing to send email to {self.useremail}\n\n\n\n\n\n")

        # Text if email doesnt support HTML
        text = f"""\
        Your video with keypoints overlayed can be found at https://gait-analysis.s3-ap-southeast-2.amazonaws.com/output_videos/{self.filename}.
        Thank you for uploading your walking video, we appreciate really appreciate it!
        If you want to try your luck at getting the celebrity you want, simply record yourself walking again on our website (weko.health)
        """

        # HTML if email does support HTML
        html = f"""\
        <html>
            <body>
                <p>
                    Your video with keypoints overlayed can be found <a href="https://gait-analysis.s3-ap-southeast-2.amazonaws.com/output_videos/{self.filename}">Here</a>.
                    <br><br>Thank you for uploading your walking video, we appreciate really appreciate it!

                    <br><br>If you want to try your luck at getting the celebrity you want, simply record yourself walking again 
                    on our website, <a href="weko.health">WeKo Health</a> 
                </p> 
            </body> 
        </html> 
        """

        # Creates two parts to allow all email clients to receive email
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        text = message.as_string()

        # Initialise SSL
        context = ssl.create_default_context()

        # Send email via gmail smtp server.
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.senderemail, self.password)
            server.sendmail(self.senderemail, self.useremail, text)
