# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### 1. Create Conda Environment
```bash
conda env create -f environment.yml
conda activate plivo-ivr
```

### 2. Create .env File
Copy the credentials and create `.env`:
```bash
cat > .env << 'EOF'
PLIVO_AUTH_ID=MANZJJOGRLNZK0ZMZIMM
PLIVO_AUTH_TOKEN=NmU2ZmRhMjYtOTE1OS00YWRiLWJlNmEtNTIxYzUy
PLIVO_PHONE_NUMBER=+YOUR_PLIVO_NUMBER
FORWARD_TO_NUMBER=+1234567890
AUDIO_URL=https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav
BASE_URL=http://localhost:5000
EOF
```

### 3. Start ngrok (in a separate terminal)
```bash
ngrok http 5000
```
Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 4. Update BASE_URL in .env
Edit `.env` and set `BASE_URL` to your ngrok URL:
```
BASE_URL=https://abc123.ngrok.io
```

### 5. Run the Application
```bash
python app.py
```

### 6. Test
- Open browser: `http://localhost:5000`
- Enter a phone number
- Click "Make Outbound Call"
- Answer the call and test the IVR!

## 📞 Testing the IVR Flow

1. **Call is answered** → You'll hear: "Welcome to InspireWorks. Press 1 for English. Press 2 for Spanish."
2. **Press 1** → "You selected English..."
3. **Level 2 Menu** → "Press 1 to play a short audio message. Press 2 to connect to a live associate."
4. **Press 1** → Audio plays, then call ends
5. **Press 2** → Call forwards to the number in `FORWARD_TO_NUMBER`

## ⚠️ Important Notes

- Make sure `BASE_URL` in `.env` matches your ngrok URL
- Keep ngrok running while testing
- Your Plivo account needs a phone number and sufficient credits
- Phone numbers must include country code (e.g., `+1` for US)

