from flask import Flask, request, render_template, render_template_string, redirect
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ========================================================
# ⚙️ यहाँ अपनी डिटेल्स भरें
# ========================================================
MY_EMAIL = "yr3574524@gmail.com"
MY_PASSWORD = "hyqprqhqjijriexr" # बिना स्पेस के पेस्ट करें

# यहाँ अपने ज़ार्विस का गूगल ड्राइव या डाउनलोड लिंक डाल दें
SOURCE_CODE_LINK = "https://drive.google.com/drive/folders/1eAtrnK9QToNPT8zn5AWbpZ8cCS4LZl2K?usp=sharing" 
# ========================================================

# पेंडिंग पेमेंट्स को याद रखने के लिए लिस्ट
pending_payments = []

# 🔥 यह नया रूट है जो तुम्हारी index.html फाइल को लोड करेगा!
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    name = request.form.get('name')
    email = request.form.get('email')
    utr = request.form.get('utr')
    
    # डेटा को लिस्ट में सेव करें
    user_data = {"name": name, "email": email, "utr": utr}
    pending_payments.append(user_data)
    
    # आपको (एडमिन को) अलर्ट ईमेल भेजना
    try:
        msg = MIMEText(f"Hi Yash,\n\nNew Payment Request Received!\n\nName: {name}\nEmail: {email}\nUTR/Transaction ID: {utr}\n\nTo approve this payment, go to: https://jarvis-ai-store.onrender.com/admin")
        msg['Subject'] = '🚨 New Jarvis AI Purchase Request'
        msg['From'] = MY_EMAIL
        msg['To'] = MY_EMAIL
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending admin notification:", e)

    return "<h1>Details Submitted Successfully!</h1><p>Our team is verifying your UTR number. The source code will be emailed to you within 10-30 minutes. Thank you!</p>"

@app.route('/admin')
def admin_panel():
    # एडमिन पैनल का सिंपल डिज़ाइन
    html_content = '''
    <html>
    <head>
        <title>Jarvis Shop - Admin Panel</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e293b; }
            th, td { padding: 12px; border: 1px solid #334155; text-align: left; }
            th { background: #334155; color: #38bdf8; }
            .btn { color: #4ade80; text-decoration: none; font-weight: bold; }
            .btn:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h2>🤖 Jarvis Shop - Pending Payment Approvals</h2>
        <table>
            <tr><th>Name</th><th>Email</th><th>UTR / Transaction ID</th><th>Action</th></tr>
            {% for user in payments %}
            <tr>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.utr }}</td>
                <td><a class="btn" href="/approve/{{ loop.index0 }}">Approve & Send Code</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_content, payments=pending_payments)

@app.route('/approve/<int:index>')
def approve_user(index):
    if 0 <= index < len(pending_payments):
        user = pending_payments.pop(index)
        
        # यूजर को ऑटोमैटिकली सोर्स कोड का ईमेल भेजना
        try:
            msg = MIMEText(f"Hello {user['name']},\n\nYour payment has been successfully verified! 🎉\n\nYou can download the complete Jarvis AI Source Code and Setup Guide from the link below:\n\n🔗 {SOURCE_CODE_LINK}\n\nIf you face any issues during setup, feel free to reply to this email.\n\nBest Regards,\nYash (Creator of Jarvis AI)")
            msg['Subject'] = '🔥 Your Jarvis AI Source Code is Here!'
            msg['From'] = MY_EMAIL
            msg['To'] = user['email']
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, user['email'], msg.as_string())
            server.quit()
            print(f"Success: Code sent to {user['name']}")
        except Exception as e:
            print("Error sending code to user:", e)
            
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
