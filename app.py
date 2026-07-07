import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, render_template_string, redirect

app = Flask(__name__)

# ========================================================
# ⚙️ BREVO SMTP CONFIGURATION (100% AUTOMATIC)
# ========================================================
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "yr3574524@gmail.com"
SMTP_PASSWORD = "Xsmtpsib-aa563da47eb35f6ff019a653aac87a307042dcb5500bd0b8a3fc4d4fd51b7581-LRwsUDzkxkWRnxXe"

SOURCE_CODE_LINK = "https://drive.google.com/drive/folders/1eAtrnK9QToNPT8zn5AWbpZ8cCS4LZl2K?usp=sharing"
# ========================================================

# प्रत्येक रिक्वेस्ट को एक यूनिक आईडी देने के लिए काउंटर
request_counter = 0
pending_payments = {}

def send_source_code_email(user_email, user_name):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = user_email
        msg['Subject'] = "Your Jarvis AI Assistant Source Code is Here!"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; line-height: 1.6;">
            <h2 style="color: #0284c7;">Hello {user_name}! 👋</h2>
            <p>Your payment has been successfully verified by Yash. Here is the download link for your Jarvis AI Assistant Source Code:</p>
            <p style="margin: 20px 0;">
                <a href="{SOURCE_CODE_LINK}" style="background: #22c55e; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">Download Source Code</a>
            </p>
            <p><strong>Note:</strong> Make sure you have Python and VS Code installed on your HP laptop to run this Jarvis program smoothly.</p>
            <p>Thank you for your purchase!</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, user_email, msg.as_string())
        server.quit()
        print(f"✅ SUCCESS: Email sent to {user_email}")
        return True
    except Exception as e:
        print(f"❌ SMTP ERROR: {str(e)}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    global request_counter
    name = request.form.get('name')
    email = request.form.get('email')
    utr = request.form.get('utr')
    
    # प्रत्येक रिक्वेस्ट को एक पक्की ID देकर डिक्शनरी में सेव करें
    request_counter += 1
    pending_payments[str(request_counter)] = {"name": name, "email": email, "utr": utr}
    
    print(f"🚨 New Request Saved [ID: {request_counter}]: {name} ({email})")
    return "<h1>Details Submitted Successfully!</h1><p>Our team is verifying your UTR number. Code will be sent shortly.</p>"

@app.route('/admin')
def admin_panel():
    html_content = '''
    <html>
    <head>
        <title>Jarvis Shop - Admin Panel</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e293b; }
            th, td { padding: 12px; border: 1px solid #334155; text-align: left; }
            th { background: #334155; color: #38bdf8; }
            .btn { background: #16a34a; color: white; padding: 8px 16px; text-decoration: none; font-weight: bold; border-radius: 4px; display: inline-block; }
            .btn:hover { background: #15803d; }
        </style>
    </head>
    <body>
        <h2>🤖 Jarvis Shop - Admin Control Panel</h2>
        <p>Review requests and click 'Approve & Send Code' below:</p>
        <table>
            <tr><th>Name</th><th>Email</th><th>UTR / Transaction ID</th><th>Action</th></tr>
            {% if payments %}
                {% for req_id, user in payments.items() %}
                <tr>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.utr }}</td>
                    <td><a class="btn" href="/approve/{{ req_id }}">Approve & Send Code</a></td>
                </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan="4" style="text-align:center; padding:20px; color:#94a3b8;">No pending requests. 🎉</td></tr>
            {% endif %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_content, payments=pending_payments)

@app.route('/approve/<string:req_id>')
def approve_user(req_id):
    print(f"🖱️ Click Detected: Action for Request ID {req_id}")
    if req_id in pending_payments:
        # डेटा निकालें ताकि दोबारा न भेजा जा सके
        user = pending_payments.pop(req_id)
        # ईमेल भेजने की प्रक्रिया शुरू करें
        send_source_code_email(user['email'], user['name'])
    else:
        print(f"⚠️ Warning: Request ID {req_id} not found in pending list.")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
