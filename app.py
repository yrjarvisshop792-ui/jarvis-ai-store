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
SMTP_USERNAME = "yr3574524@gmail.com"  # तुम्हारी ब्रेवो वाली ईमेल आईडी
SMTP_PASSWORD = "Xsmtpsib-aa563da47eb35f6ff019a653aac87a307042dcb5500bd0b8a3fc4d4fd51b7581-LRwsUDzkxkWRnxXe"

# ज़ार्विस का गूगल ड्राइव या डाउनलोड लिंक
SOURCE_CODE_LINK = "https://drive.google.com/drive/folders/1eAtrnK9QToNPT8zn5AWbpZ8cCS4LZl2K?usp=sharing"
# ========================================================

# पेंडिंग पेमेंट्स को याद रखने के लिए लिस्ट
pending_payments = []

def send_source_code_email(user_email, user_name):
    """यह फ़ंक्शन ब्रेवो के ज़रिए यूजर को ऑटोमैटिक ईमेल भेजेगा"""
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Jarvis Store <{SMTP_USERNAME}>"
        msg['To'] = user_email
        msg['Subject'] = "🔥 Your Jarvis AI Assistant Source Code is Here! 🤖"

        # ईमेल का प्रोफेशनल मैसेज डिज़ाइन
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
                <h2 style="color: #0284c7; text-align: center;">Hello {user_name}! 👋</h2>
                <p>Thank you for purchasing the <strong>Jarvis AI Assistant Personal Personal Project</strong>.</p>
                <p>Your UTR payment has been successfully verified by Yash. As promised, your complete source code configuration files are ready for download.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{SOURCE_CODE_LINK}" target="_blank" style="background-color: #22c55e; color: white; padding: 12px 25px; text-decoration: none; font-size: 16px; font-weight: bold; border-radius: 5px;">📥 Download Source Code</a>
                </div>
                
                <p><strong>Note:</strong> Make sure you have Python and VS Code installed on your HP laptop to run this Jarvis program smoothly.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #777; text-align: center;">Jarvis AI Store • Automated Delivery System powered by Brevo</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # SMTP सर्वर से कनेक्ट करके ईमेल भेजना
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # सिक्योर कनेक्शन चालू करें
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, user_email, msg.as_string())
        server.quit()
        print(f"✅ Success: Email sent to {user_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    name = request.form.get('name')
    email = request.form.get('email')
    utr = request.form.get('utr')
    
    # डेटा को पेंडिंग लिस्ट में सेव करें
    user_data = {"name": name, "email": email, "utr": utr}
    pending_payments.append(user_data)
    
    print(f"🚨 New Request Received: {name} ({email})")
    return "<h1>Details Submitted Successfully!</h1><p>Our team is verifying your UTR number. The source code will be emailed to you within 10-30 minutes after verification. Thank you!</p>"

@app.route('/admin')
def admin_panel():
    # एडमिन पैनल का सिंपल और धांसू डिज़ाइन
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
            .btn:hover { background: #15803d; }
            .no-data { text-align: center; padding: 20px; color: #94a3b8; }
        </style>
    </head>
    <body>
        <h2>🤖 Jarvis Shop - Admin Control Panel</h2>
        <p>Review requests and click 'Approve & Send Code' to instantly email the link via Brevo Server.</p>
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
                <tr><td colspan="4" class="no-data">No pending requests available. 🎉</td></tr>
            {% endif %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_content, payments=pending_payments)

@app.route('/approve/<int:index>')
def approve_user(index):
    if 0 <= index < len(pending_payments):
        # लिस्ट से यूजर का डेटा निकालें
        user = pending_payments.pop(index)
        # ब्रेवो के जरिए ईमेल भेजें
        send_source_code_email(user['email'], user['name'])
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
