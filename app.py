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

pending_payments = []

def send_source_code_email(user_email, user_name):
    try:
        msg = MIMEMultipart()
        # From फील्ड को एकदम सिंपल रखा है ताकि ब्रेवो रिजेक्ट न करे
        msg['From'] = SMTP_USERNAME
        msg['To'] = user_email
        msg['Subject'] = "Your Jarvis AI Assistant Source Code is Here!"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Hello {user_name}! 👋</h2>
            <p>Your payment has been verified. Here is the download link for your Jarvis AI Assistant Source Code:</p>
            <p><a href="{SOURCE_CODE_LINK}" style="background: #22c55e; color: white; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">Download Source Code</a></p>
            <p>Thank you for your purchase!</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # कनेक्शन टाइमआउट जोड़ दिया है ताकि कोड अटके नहीं
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, user_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"❌ SMTP Error: {str(e)}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    name = request.form.get('name')
    email = request.form.get('email')
    utr = request.form.get('utr')
    
    user_data = {"name": name, "email": email, "utr": utr}
    pending_payments.append(user_data)
    
    print(f"🚨 New Request: {name} ({email})")
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
            .btn { background: #16a34a; color: white; padding: 6px 12px; text-decoration: none; font-weight: bold; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h2>🤖 Jarvis Shop - Admin Control Panel</h2>
        <table>
            <tr><th>Name</th><th>Email</th><th>UTR / Transaction ID</th><th>Action</th></tr>
            {% if payments %}
                {% for user in payments %}
                <tr>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.utr }}</td>
                    <td><a class="btn" href="/approve/{{ loop.index0 }}">Approve & Send Code</a></td>
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

@app.route('/approve/<int:index>')
def approve_user(index):
    if 0 <= index < len(pending_payments):
        user = pending_payments.pop(index)
        # ईमेल भेजने की कोशिश करें, अगर फेल भी हो तो वेबसाइट क्रैश नहीं होगी
        email_status = send_source_code_email(user['email'], user['name'])
        if not email_status:
            print("⚠️ Email failed but request removed from queue to prevent loop.")
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
