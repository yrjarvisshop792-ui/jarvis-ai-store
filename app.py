from flask import Flask, request, render_template, render_template_string, redirect
import urllib.parse

app = Flask(__name__)

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
    phone = request.form.get('phone', '') # अगर फॉर्म में फोन नंबर का फील्ड है

    request_counter += 1
    pending_payments[str(request_counter)] = {
        "name": name, 
        "email": email, 
        "utr": utr,
        "phone": phone
    }
    
    print(f"🚨 New Request Saved [ID: {request_counter}]: {name}")
    return "<h1>Details Submitted Successfully!</h1><p>Our team is verifying your UTR number. The source code link will be sent to you shortly after verification. Thank you!</p>"

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
            .btn { background: #0284c7; color: white; padding: 8px 16px; text-decoration: none; font-weight: bold; border-radius: 4px; display: inline-block; }
            .btn:hover { background: #0369a1; }
        </style>
    </head>
    <body>
        <h2>🤖 Jarvis Shop - Admin Control Panel</h2>
        <p>Review requests and click 'Approve & Send via WhatsApp' to open WhatsApp with a pre-filled message.</p>
        <table>
            <tr><th>Name</th><th>Email / Phone</th><th>UTR ID</th><th>Action</th></tr>
            {% if payments %}
                {% for req_id, user in payments.items() %}
                <tr>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }} {% if user.phone %}({{ user.phone }}){% endif %}</td>
                    <td>{{ user.utr }}</td>
                    <td><a class="btn" href="/approve/{{ req_id }}" target="_blank">Approve & Send Code</a></td>
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
    if req_id in pending_payments:
        user = pending_payments.pop(req_id)
        
        # व्हाट्सएप के लिए एक बढ़िया सा मैसेज तैयार करना
        message = f"Hello {user['name']}! 👋\n\nYour payment (UTR: {user['utr']}) has been verified successfully by Yash. ✅\n\nHere is the download link for your Jarvis AI Assistant Source Code Configuration Files:\n📥 {SOURCE_CODE_LINK}\n\nThank you for your purchase! 🤖"
        
        # मैसेज को URL फ्रेंडली बनाना
        encoded_message = urllib.parse.quote(message)
        
        # व्हाट्सएप वेब/एप का डायरेक्ट लिंक (अगर यूजर का फोन नंबर नहीं है, तो यह सीधा व्हाट्सएप खोलेगा जहाँ आप किसी भी चैट में पेस्ट कर सकते हैं)
        whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_message}"
        
        return redirect(whatsapp_url)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
