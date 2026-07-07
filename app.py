from flask import Flask, request, render_template, render_template_string, redirect, session
import urllib.parse

app = Flask(__name__)

# 🔑 सुरक्षा के लिए सीक्रेट की और एडमिन पासवर्ड
app.secret_key = "super_secret_jarvis_key_yash" # यह सेशन को सुरक्षित रखता है
ADMIN_PASSWORD = "YASH_JARVIS_STORE_@_SECURE" # 🎯 अपना एडमिन पासवर्ड यहाँ बदलो!

# ========================================================
# ⚙️ CONFIGURATION
# ========================================================
SOURCE_CODE_LINK = "https://drive.google.com/drive/folders/1eAtrnK9QToNPT8zn5AWbpZ8cCS4LZl2K?usp=sharing"
# ========================================================

request_counter = 0
pending_payments = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    global request_counter
    name = request.form.get('name')
    email = request.form.get('email')
    utr = request.form.get('utr')
    phone = request.form.get('phone')

    if phone:
        phone = phone.strip().replace(" ", "").replace("-", "")
        if not phone.startswith('+') and len(phone) == 10:
            phone = "91" + phone
        elif phone.startswith('+'):
            phone = phone.replace("+", "")

    request_counter += 1
    pending_payments[str(request_counter)] = {
        "name": name, 
        "email": email, 
        "utr": utr,
        "phone": phone
    }
    
    return "<h1>Details Submitted Successfully!</h1><p>Our team is verifying your UTR number. The source code link will be sent directly to your WhatsApp shortly after verification. Thank you!</p>"

# 🔒 एडमिन लॉगिन पेज (Password Prompt)
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        if entered_password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return '''
            <div style="text-align:center; margin-top:50px; font-family:Arial;">
                <h3 style="color:red;">❌ Incorrect Password! Access Denied.</h3>
                <a href="/admin">Try Again</a>
            </div>
            '''

    # अगर यूजर पहले से लॉगिन नहीं है, तो उसे पासवर्ड का डिब्बा दिखाओ
    if not session.get('logged_in'):
        return '''
        <html>
        <head>
            <title>Admin Login</title>
            <style>
                body { font-family: Arial, sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .login-box { background: #1e293b; padding: 40px; border-radius: 12px; border: 1px solid #334155; text-align: center; width: 300px; }
                input { width: 100%; padding: 12px; margin: 15px 0; background: #05070a; border: 1px solid #475569; color: white; border-radius: 6px; text-align: center; }
                button { width: 100%; padding: 12px; background: #00f3ff; color: black; border: none; font-weight: bold; border-radius: 6px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h2>🤖 Admin Access</h2>
                <form method="POST">
                    <input type="password" name="password" placeholder="Enter Admin Password" required>
                    <button type="submit">ACCESS PANEL</button>
                </form>
            </div>
        </body>
        </html>
        '''

    # अगर लॉगिन सक्सेसफुल है, तो असली एडमिन पैनल दिखाओ
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
            .logout { float: right; background: #ef4444; color: white; padding: 8px 16px; text-decoration: none; font-weight: bold; border-radius: 4px; }
        </style>
    </head>
    <body>
        <a class="logout" href="/admin/logout">Secure Logout</a>
        <h2>🤖 Jarvis Shop - Admin Control Panel</h2>
        <table>
            <tr><th>Name</th><th>Email</th><th>WhatsApp Number</th><th>UTR ID</th><th>Action</th></tr>
            {% if payments %}
                {% for req_id, user in payments.items() %}
                <tr>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>+{{ user.phone }}</td>
                    <td>{{ user.utr }}</td>
                    <td><a class="btn" href="/approve/{{ req_id }}" target="_blank">Approve & Send Code</a></td>
                </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan="5" style="text-align:center; padding:20px; color:#94a3b8;">No pending requests. 🎉</td></tr>
            {% endif %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_content, payments=pending_payments)

# 🚪 लॉगआउट रूट
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect('/admin')

@app.route('/approve/<string:req_id>')
def approve_user(req_id):
    if not session.get('logged_in'):
        return "Unauthorized", 401
        
    if req_id in pending_payments:
        user = pending_payments.pop(req_id)
        customer_phone = user['phone']
        
        message = (
            f"⚡ *OFFICIAL JARVIS AI ASSISTANT STORE* ⚡\n\n"
            f"Hello *{user['name']}*! 👋\n\n"
            f"Your payment has been verified successfully by Yash! ✅\n"
            f"🧾 *Transaction UTR:* {user['utr']}\n\n"
            f"As promised, your advanced *Jarvis AI Personal Assistant Source Code* configuration files are ready for deployment! 🚀\n\n"
            f"📥 *DOWNLOAD LINK:* {SOURCE_CODE_LINK}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 *CORE FACILITIES & FEATURES INCLUDED:*\n"
            f"• 🎙️ *Advanced Voice Recognition:* Natural voice command processing (Wake word detection like 'Hey Jarvis').\n"
            f"• 🧠 *AI-Powered Brain:* Smart responses powered by advanced LLM Integration.\n"
            f"• 💻 *System Automation:* Control your desktop applications, search Google/YouTube, and check system status via voice.\n"
            f"• 📧 *Automated Utilities:* Features to send emails, manage notes, and set smart reminders.\n"
            f"• 🛠️ *Fully Customizable:* Open-source code tailored for custom feature development.\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⚙️ *PREREQUISITES FOR RUNNING THE CODE:*\n"
            f"1. Make sure you have *Python* installed on your system.\n"
            f"2. Use *Visual Studio Code (VS Code)* as your main editor.\n"
            f"3. Run `pip install -r requirements.txt` in your terminal to install all modules.\n\n"
            f"Thank you for your purchase and being a part of this amazing AI project! If you face any issues during setup, feel free to drop a message here. 🤝\n\n"
            f"Best Regards,\n"
            f"*Yash — Jarvis Project Developer*"
        )
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={customer_phone}&text={encoded_message}"
        return redirect(whatsapp_url)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
