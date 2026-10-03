# TeleMedicine Platform - Distribution Package

A comprehensive telemedicine solution connecting patients with remote doctors, integrating local pharmacies for medicine availability, and managing follow-ups digitally.

## 📦 Package Contents

This package is distributed in two separate folders:

### 📁 `frontend/`
- Patient-friendly web interface
- HTML, CSS, JavaScript
- No installation required
- Just open in browser

### 📁 `backend/`
- Flask API server
- Python application
- SQLite database (auto-created)
- Includes sample data

## 🚀 Quick Start

### Step 1: Start the Backend

1. Navigate to the `backend` folder
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. The backend will start on `http://localhost:5000`
5. Database is automatically created with sample data

### Step 2: Open the Frontend

1. Navigate to the `frontend` folder
2. Double-click `index.html`, OR
3. Run a local server:
   ```bash
   python -m http.server 8000
   ```
4. Open `http://localhost:8000` in your browser

### Step 3: Test the Application

Login with sample credentials:
- **Email**: john.smith@email.com
- **Password**: patient123

## ✨ Features

- ✅ Patient registration and authentication
- ✅ Browse 100+ real doctors with various specializations
- ✅ Request remote consultations
- ✅ Search medicines at local pharmacies
- ✅ View consultation history
- ✅ Digital follow-up management
- ✅ Prescription tracking

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (no frameworks)
- **Backend**: Python + Flask
- **Database**: SQLite (built into Python)

## 📋 System Requirements

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for CDN resources if any)

## 📖 Detailed Documentation

- **Backend Setup**: See `backend/README.md`
- **Frontend Setup**: See `frontend/README.md`

## 🔑 Sample Data Included

- 100 real doctors (Cardiologists, Neurologists, Pediatricians, etc.)
- 5 pharmacies
- 30 common medicines
- 5 sample patients for testing

## 🌐 Sharing This Package

You can share this package in several ways:

1. **As a ZIP file**: Compress the entire `telemedicine-dist` folder
2. **Via GitHub**: Upload to GitHub repository
3. **Cloud storage**: Upload to Google Drive, Dropbox, OneDrive
4. **Direct share**: Send the frontend and backend folders separately

## 📝 Notes

- The backend must be running before using the frontend
- The SQLite database is created automatically on first run
- All sample data is loaded automatically
- No MySQL or external database installation required

## 🆘 Troubleshooting

**Backend won't start?**
- Check if Python 3.8+ is installed
- Verify all dependencies are installed
- Check if port 5000 is already in use

**Frontend can't connect to backend?**
- Ensure backend is running on http://localhost:5000
- Check browser console for errors (F12)
- Verify both are on the same port configuration

**Database not created?**
- The database is created automatically
- Check if the `database` folder exists in backend
- Look for `telemedicine.db` file

## 📄 License

This project is for educational purposes.

---

**Need Help?** Check the individual README files in the `frontend/` and `backend/` folders for detailed setup instructions.
