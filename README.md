# Plivo IVR System - Multi-level Interactive Voice Response

A complete implementation of a multi-level IVR (Interactive Voice Response) system using Plivo's Voice API with XML call flow control. This system demonstrates outbound calling, language selection, and branching logic.

## 📋 Overview

This application implements a 2-level IVR system:
- **Level 1**: Language selection (English/Spanish)
- **Level 2**: Action selection (Play audio message / Connect to live associate)

All call flow logic is handled using **Plivo XML** (not JSON API), as required.

## 🏗️ Architecture

- **Backend**: Flask (Python) web application
- **Call Flow**: Plivo XML responses
- **Frontend**: Simple HTML/JavaScript interface to trigger calls
- **Environment**: Conda environment for dependency management

## 📦 Prerequisites

1. **Conda** installed on your system
2. **Plivo Account** with:
   - Auth ID (get from Plivo dashboard)
   - Auth Token (get from Plivo dashboard)
   - A Plivo phone number (for making outbound calls)
3. **ngrok** or similar tool (for exposing local server to Plivo)

## 🚀 Setup Instructions

### Step 1: Create Conda Environment

```bash
cd /home/megha-tr/Desktop/plivo
conda env create -f environment.yml
```

### Step 2: Activate Conda Environment

```bash
conda activate plivo-ivr
```

### Step 3: Install Additional Dependencies (if needed)

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and update the following:

```env
# Your Plivo Phone Number (get this from Plivo dashboard)
PLIVO_PHONE_NUMBER=+1234567890

# Number to forward calls to (for live associate option)
FORWARD_TO_NUMBER=+1234567890

# Base URL - IMPORTANT: Update this with your ngrok/public URL
BASE_URL=https://your-ngrok-url.ngrok.io
```

**Important**: The `BASE_URL` must be publicly accessible so Plivo can reach your IVR endpoints. Use ngrok or similar service:

```bash
# Install ngrok: https://ngrok.com/download
# Then run:
ngrok http 5000
# Copy the HTTPS URL (e.g., https://abc123.ngrok.io) and set it as BASE_URL
```

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🧪 Testing

### Option 1: Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a phone number (with country code, e.g., `+1234567890`)
3. Click "Make Outbound Call"
4. Answer the call and follow the IVR prompts:
   - **Level 1**: Press 1 for English, Press 2 for Spanish
   - **Level 2**: Press 1 to play audio, Press 2 to connect to associate

### Option 2: Using cURL

```bash
curl -X POST http://localhost:5000/make-call \
  -H "Content-Type: application/json" \
  -d '{"to_number": "+1234567890"}'
```

### Expected Call Flow

1. **Call is answered** → Plivo requests `/ivr/level1`
2. **Level 1 Menu** → "Press 1 for English, Press 2 for Spanish"
3. **User presses 1 or 2** → Plivo requests `/ivr/level1-action`
4. **Language confirmation** → Redirects to `/ivr/level2?lang=en` or `lang=es`
5. **Level 2 Menu** → "Press 1 to play audio, Press 2 for associate"
6. **User presses 1** → Plays audio file and hangs up
7. **User presses 2** → Dials the forward number

## 📁 Project Structure

```
plivo/
├── app.py                 # Main Flask application with IVR endpoints
├── templates/
│   └── index.html        # Frontend UI for triggering calls
├── environment.yml       # Conda environment configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🔧 API Endpoints

### `GET /`
- Serves the frontend HTML interface

### `POST /make-call`
- Initiates an outbound call
- **Request Body**: `{"to_number": "+1234567890"}`
- **Response**: `{"success": true, "call_uuid": "...", "message": "..."}`

### `GET /ivr/level1`
- Returns Plivo XML for Level 1 language selection menu
- Called by Plivo when call is answered

### `GET /ivr/level1-action`
- Processes Level 1 DTMF input
- Routes to Level 2 based on language selection

### `GET /ivr/level2?lang=en|es`
- Returns Plivo XML for Level 2 action selection menu
- Language-specific prompts based on `lang` parameter

### `GET /ivr/level2-action?lang=en|es&Digits=1|2`
- Processes Level 2 DTMF input
- Plays audio (Digits=1) or connects to associate (Digits=2)

### `GET /health`
- Health check endpoint

## 🔑 Plivo Credentials

You need to configure your Plivo credentials in the `.env` file:
- **Auth ID**: Get from your Plivo dashboard
- **Auth Token**: Get from your Plivo dashboard

Copy `.env.example` to `.env` and add your credentials there.

## 📝 Plivo XML Elements Used

- `<Response>`: Root element for all Plivo XML responses
- `<GetDigits>`: Captures DTMF input from caller
- `<Speak>`: Text-to-speech prompts
- `<Play>`: Plays audio files
- `<Dial>`: Forwards call to another number
- `<Redirect>`: Redirects call flow to another endpoint
- `<Hangup>`: Ends the call

## 🐛 Troubleshooting

### Issue: Plivo can't reach my endpoints
**Solution**: Make sure `BASE_URL` in `.env` is set to your public ngrok URL, not `localhost:5000`

### Issue: Call fails immediately
**Solution**: 
- Verify your Plivo phone number is correct in `.env`
- Check that your Plivo account has sufficient credits
- Ensure the destination number format is correct (include country code)

### Issue: IVR menu doesn't play
**Solution**:
- Check Flask logs for errors
- Verify ngrok is running and `BASE_URL` is correct
- Test endpoints manually: `curl http://localhost:5000/ivr/level1`

### Issue: Audio doesn't play
**Solution**: The default audio URL should work, but you can replace `AUDIO_URL` in `.env` with your own publicly accessible MP3 file

## 📚 Additional Resources

- [Plivo XML Reference](https://www.plivo.com/docs/voice/xml/)
- [Plivo Python SDK](https://www.plivo.com/docs/sdk/python/)
- [Plivo Voice API](https://www.plivo.com/docs/voice/api/)

## ✅ Deliverables Checklist

- ✅ Working application with outbound call capability
- ✅ Multi-level IVR (Level 1: Language, Level 2: Actions)
- ✅ Plivo XML implementation (not JSON API)
- ✅ DTMF input handling with branching logic
- ✅ Invalid input handling
- ✅ Code repository with README
- ✅ Setup instructions
- ✅ Plivo credentials documented

## 📄 License

This project is created for the Plivo Forward Deployed Engineer technical assignment.

