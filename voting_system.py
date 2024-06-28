import mysql.connector
from mysql.connector import Error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345',
    'database': 'election_db'
}

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'alamudev1811@gmail.com'
smtp_password = 'gytg aotd nwxy uckq'  # Use the app-specific password here

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def cast_vote(politician_name, voter_email):
    connection = create_connection()
    if connection is None:
        print("Connection to the database failed.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM politicians WHERE name = %s", (politician_name,))
        if cursor.fetchone() is None:
            print(f"Politician '{politician_name}' does not exist.")
            return

        cursor.execute("UPDATE politicians SET votes = votes + 1 WHERE name = %s", (politician_name,))
        connection.commit()
        print(f"Vote cast for {politician_name}")

        log_vote(politician_name, voter_email)
        send_thank_you_email(voter_email, politician_name)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def log_vote(politician_name, voter_email):
    vote_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Log in the first file
    print("Logging vote in vote_log.txt")
    with open('vote_log.txt', 'a') as file1:
        file1.write(f"{vote_time} - {voter_email} voted for {politician_name}\n")
        print(f"Wrote to vote_log.txt: {vote_time} - {voter_email} voted for {politician_name}")
    
    # Log in the second file
    print("Logging vote in additional_vote_log.txt")
    with open('additional_vote_log.txt', 'a') as file2:
        file2.write(f"Vote for {politician_name} recorded at {vote_time}\n")
        print(f"Wrote to additional_vote_log.txt: Vote for {politician_name} recorded at {vote_time}")

def send_thank_you_email(voter_email, politician_name):
    vote_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = "Thank you for voting!"
    body = f"Thank you for voting for {politician_name} on {vote_time}."

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = voter_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, voter_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    politician_name = input("Enter the politician's name you want to vote for: ")
    voter_email = input("Enter your email address: ")
    cast_vote(politician_name, voter_email)
    print("Vote cast successfully.")
