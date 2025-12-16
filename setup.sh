#!/bin/bash

# Setup script for Plivo IVR System

echo "🚀 Setting up Plivo IVR System..."
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install conda first."
    exit 1
fi

echo "✅ Conda found"
echo ""

# Create conda environment
echo "📦 Creating conda environment..."
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo "✅ Conda environment created successfully"
else
    echo "❌ Failed to create conda environment"
    exit 1
fi

echo ""
echo "🔧 Setting up environment variables..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOF
# Plivo Credentials
PLIVO_AUTH_ID=YOUR_PLIVO_AUTH_ID
PLIVO_AUTH_TOKEN=YOUR_PLIVO_AUTH_TOKEN

# Your Plivo Phone Number (update this with your actual Plivo number)
PLIVO_PHONE_NUMBER=

# Number to forward calls to (for live associate option)
FORWARD_TO_NUMBER=+1234567890

# Public audio file URL for Level 2 option 1
AUDIO_URL=https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav

# Base URL for your application
# IMPORTANT: Update this with your public URL (ngrok URL) so Plivo can reach your endpoints
BASE_URL=http://localhost:5000
EOF
    echo "✅ Created .env file"
else
    echo "⚠️  .env file already exists, skipping..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the conda environment: conda activate plivo-ivr"
echo "2. Edit .env file and update:"
echo "   - PLIVO_PHONE_NUMBER (your Plivo number)"
echo "   - BASE_URL (your ngrok/public URL)"
echo "3. Run the application: python app.py"
echo "4. In another terminal, start ngrok: ngrok http 5000"
echo "5. Update BASE_URL in .env with your ngrok URL"
echo "6. Restart the application"
echo ""

