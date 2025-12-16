#!/bin/bash
# Helper script to get tunnel URL

echo "Checking for running tunnels..."
echo ""

# Check ngrok
if pgrep -f "ngrok http" > /dev/null; then
    echo "✓ Ngrok is running"
    URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); tunnels = [t for t in data.get('tunnels', []) if 'https' in t.get('public_url', '')]; print(tunnels[0]['public_url'] if tunnels else '')" 2>/dev/null)
    if [ ! -z "$URL" ]; then
        echo "Ngrok URL: $URL"
        exit 0
    fi
fi

# Check localtunnel
if pgrep -f "localtunnel" > /dev/null; then
    echo "✓ Localtunnel is running"
    echo "Check the terminal where localtunnel started for the URL"
    echo "It should look like: https://random-name.loca.lt"
fi

echo ""
echo "To set up ngrok:"
echo "1. Sign up at https://dashboard.ngrok.com/signup"
echo "2. Get authtoken from https://dashboard.ngrok.com/get-started/your-authtoken"
echo "3. Run: ./ngrok config add-authtoken YOUR_TOKEN"
echo "4. Run: ./ngrok http 5000"
