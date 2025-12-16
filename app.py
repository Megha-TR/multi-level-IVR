"""
Plivo IVR System - Multi-level Interactive Voice Response
Uses Plivo XML for call flow control
"""

from flask import Flask, request, render_template, jsonify
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Plivo credentials
PLIVO_AUTH_ID = os.getenv('PLIVO_AUTH_ID', '')  # Set in .env file
PLIVO_AUTH_TOKEN = os.getenv('PLIVO_AUTH_TOKEN', '')  # Set in .env file
PLIVO_PHONE_NUMBER = os.getenv('PLIVO_PHONE_NUMBER', '')  # Your Plivo number
FORWARD_TO_NUMBER = os.getenv('FORWARD_TO_NUMBER', '+1234567890')  # Placeholder for live associate

# Public audio file URL (using Plivo's default audio or a public MP3)
AUDIO_URL = os.getenv('AUDIO_URL', 'https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav')

# Base URL for your application (update this with your ngrok/public URL)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

# XML files directory
XML_DIR = os.path.join(os.path.dirname(__file__), 'xml')


def load_xml_template(filename, **kwargs):
    """Load XML file and replace template variables"""
    filepath = os.path.join(XML_DIR, filename)
    with open(filepath, 'r') as f:
        xml_content = f.read()
    
    # Replace template variables
    for key, value in kwargs.items():
        xml_content = xml_content.replace(f'{{{{{key}}}}}', str(value))
    
    return xml_content


@app.route('/')
def index():
    """Simple frontend to trigger outbound calls"""
    return render_template('index.html')


@app.route('/make-call', methods=['POST'])
def make_call():
    """Endpoint to initiate an outbound call"""
    try:
        data = request.json
        to_number = data.get('to_number')
        
        if not to_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        if not PLIVO_PHONE_NUMBER:
            return jsonify({'error': 'PLIVO_PHONE_NUMBER not configured in .env file'}), 400
        
        # Construct answer URL for Level 1 IVR
        answer_url = f"{BASE_URL}/ivr/level1"
        
        # Make outbound call using Plivo REST API directly
        url = f"https://api.plivo.com/v1/Account/{PLIVO_AUTH_ID}/Call/"
        
        # Basic auth for Plivo API
        auth_string = f"{PLIVO_AUTH_ID}:{PLIVO_AUTH_TOKEN}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        payload = {
            'from': PLIVO_PHONE_NUMBER,
            'to': to_number,
            'answer_url': answer_url,
            'answer_method': 'GET'
        }
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json'
        }
        
        # Make API call
        api_response = requests.post(url, json=payload, headers=headers)
        
        if api_response.status_code == 201:
            response_data = api_response.json()
            return jsonify({
                'success': True,
                'call_uuid': response_data.get('request_uuid', ''),
                'message': f'Call initiated to {to_number}'
            })
        else:
            error_msg = api_response.json().get('error', api_response.text)
            return jsonify({'error': f'Plivo API error: {error_msg}'}), api_response.status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ivr/level1', methods=['GET', 'POST'])
def ivr_level1():
    """
    Level 1 IVR: Language Selection
    Returns Plivo XML to prompt for language choice
    """
    xml_content = load_xml_template('level1.xml', BASE_URL=BASE_URL)
    return xml_content, 200, {'Content-Type': 'text/xml'}


@app.route('/ivr/level1-action', methods=['GET', 'POST'])
def ivr_level1_action():
    """
    Processes Level 1 input and routes to Level 2 based on language selection
    """
    digits = request.args.get('Digits', '')
    
    if digits == '1':
        # English selected - route to Level 2 English
        xml_content = load_xml_template('level1-action-en.xml', BASE_URL=BASE_URL)
    elif digits == '2':
        # Spanish selected - route to Level 2 Spanish
        xml_content = load_xml_template('level1-action-es.xml', BASE_URL=BASE_URL)
    else:
        # Invalid input - repeat Level 1 menu
        xml_content = load_xml_template('level1-action-invalid.xml', BASE_URL=BASE_URL)
    
    return xml_content, 200, {'Content-Type': 'text/xml'}


@app.route('/ivr/level2', methods=['GET', 'POST'])
def ivr_level2():
    """
    Level 2 IVR: Action Selection (Play audio or connect to associate)
    Language-specific prompts based on lang parameter
    """
    lang = request.args.get('lang', 'en')
    
    if lang == 'es':
        xml_content = load_xml_template('level2-es.xml', BASE_URL=BASE_URL)
    else:
        xml_content = load_xml_template('level2-en.xml', BASE_URL=BASE_URL)
    
    return xml_content, 200, {'Content-Type': 'text/xml'}


@app.route('/ivr/level2-action', methods=['GET', 'POST'])
def ivr_level2_action():
    """
    Processes Level 2 input: Play audio or connect to associate
    """
    digits = request.args.get('Digits', '')
    lang = request.args.get('lang', 'en')
    
    if digits == '1':
        # Play audio file
        if lang == 'es':
            xml_content = load_xml_template('level2-action-audio-es.xml', AUDIO_URL=AUDIO_URL)
        else:
            xml_content = load_xml_template('level2-action-audio-en.xml', AUDIO_URL=AUDIO_URL)
    
    elif digits == '2':
        # Connect to live associate
        if lang == 'es':
            xml_content = load_xml_template('level2-action-dial-es.xml', 
                                          PLIVO_PHONE_NUMBER=PLIVO_PHONE_NUMBER,
                                          FORWARD_TO_NUMBER=FORWARD_TO_NUMBER)
        else:
            xml_content = load_xml_template('level2-action-dial-en.xml',
                                          PLIVO_PHONE_NUMBER=PLIVO_PHONE_NUMBER,
                                          FORWARD_TO_NUMBER=FORWARD_TO_NUMBER)
    
    else:
        # Invalid input - repeat Level 2 menu
        if lang == 'es':
            xml_content = load_xml_template('level2-action-invalid-es.xml', BASE_URL=BASE_URL)
        else:
            xml_content = load_xml_template('level2-action-invalid-en.xml', BASE_URL=BASE_URL)
    
    return xml_content, 200, {'Content-Type': 'text/xml'}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Plivo IVR System'}), 200


if __name__ == '__main__':
    print(f"Starting Plivo IVR System...")
    print(f"Auth ID: {PLIVO_AUTH_ID}")
    print(f"Base URL: {BASE_URL}")
    print(f"\nMake sure to update BASE_URL in .env with your public URL (ngrok) for Plivo to reach your endpoints!")
    app.run(host='0.0.0.0', port=5000, debug=True)

