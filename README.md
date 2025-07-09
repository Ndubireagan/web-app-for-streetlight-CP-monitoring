# 📡 GSM Sensor SMS Monitor

A lightweight Python-based system that reads sensor data from a GSM module via SMS, stores it in a local SQLite database, and displays it through a user-friendly web dashboard powered by Flask.

This is ideal for remote IoT or industrial applications where internet connectivity is limited but GSM (SMS) coverage is available.

---

## 📋 Features

- 📨 Read unread SMS messages from a GSM modem (via serial port)
- 📊 Parse sensor data like **Voltage**, **Current**, and **Power** from SMS
- 🧠 Store parsed and raw messages in a **local SQLite database**
- 🌐 View data in a **responsive Flask web app** with TailwindCSS styling
- 🚨 Highlight alerts such as **overvoltage** or **undervoltage**
- 💻 Fully offline — runs on local computers without cloud dependencies

---

## 🛠 Technologies Used

- Python 3
  - `pyserial` for GSM modem communication
  - `re` for SMS parsing
  - `sqlite3` for persistent local storage
  - `Flask` for the web interface
- HTML + TailwindCSS for responsive UI

---

## 🗂 Project Structure

📁 project-root/
├── sm_reader.py # GSM modem reader and database updater
├── app.py # Flask web server for displaying readings
├── sensor_readings.db # SQLite database (auto-created on first run)
├── templates/
│ └── index.html # Web dashboard template (Tailwind CSS)


---

## 🔍 SMS Format

Your GSM device should send messages in the following format:

V:220.5 I:1.25 P:275.6

Optional alerts like:

!!OVERVOLTAGE DETECTED!!

These messages are fully logged and visualized.

---

## ⚙️ How to Run

1. **Connect your GSM modem** to the machine (e.g., `COM3` on Windows or `/dev/ttyUSB0` on Linux)
2. **Install dependencies**:
   ```bash
   pip install pyserial flask
   
Start SMS Reader (run this to collect new SMS and save to DB):

python sm_reader.py

Launch the Web App:
python app.py

View Dashboard
Open your browser at:
http://localhost:5000

📌 Use Cases
Remote power system monitoring (solar, industrial)

Agriculture sensors with GSM capabilities

Offline IoT control panels

Emergency alert logging via SMS

🧱 Future Improvements
Automatic deletion of processed SMS

Configurable threshold alerts

REST API for external integrations

Dockerization for easy deployment

🧑‍💻 Author
Ndubi Reagan

Feel free to open issues or contribute!

