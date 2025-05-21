# Quash the Quish: A Mobile App for Detecting Suspicious QR Codes

## User Manual

This is a mobile app developed using **Expo** (frontend) and **Flask** (backend) for detecting suspicious QR codes.

## What must be installed in order to run this project

- Node.js and npm https://nodejs.org
- Python 3.x installed https://www.python.org/downloads/
- Expo CLI installed globally:

```bash
npm install -g expo-cli
```

## 1. Getting Started (Backend)

1. Create a virtual environment in project root directory:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install necessary modules:

   ```bash
   pip install flask
   pip install flask_cors
   pip install pandas
   pip install rapidfuzz
   pip install mysql-connector-python
   pip install requests
   ```

4. Go to backend and run the app.py
   ```bash
   cd backend
   python3 app.py
   ```

## 2. Getting Started (Frontend)

1. Install dependencies

   ```bash
   npm install
   ```

2. Create config.js file in frontend containing the following:

   ```bash
   export const DEVICE_ADDRESS = `YOUR DEVICE'S IP ADDRESS`;
   ```

   - To find your device's IP address, in Terminal write:

   # For Windows

   ```bash
   ipconfig
   ```

   # For macOS/Linux

   ```bash
   ifconfig
   ```

3. Start the app

   ```bash
    npx expo start
   ```
