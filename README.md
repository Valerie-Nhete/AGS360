# AgriSense360 - Farming Assistant

---

## Problem

Smallholder farmers, who form the backbone of food production in regions like Sub-Saharan Africa, are facing a serious crisis.  
They depend heavily on rain-fed agriculture, yet climate change has made rainfall patterns highly unpredictable, causing frequent droughts, poor yields, and food insecurity.

Despite advances in agricultural science, access to localized data-driven advice on crop selection, soil management, and climate adaptation remains extremely limited for rural farmers.  
Without timely information, farmers often make planting decisions based on outdated traditions instead of real-time environmental conditions — leading to avoidable losses, economic instability, and worsening poverty.

---

## Solution

**AgriSense360** is a socially-driven smart farming platform designed to bridge this technology gap.  
It empowers farmers through:

- Real-time collection of **weather** and **soil condition** data
- **Personalized crop recommendations** optimized for current conditions
- **Yield and profit forecasting** to support smarter financial planning
- **Historical data tracking** (daily, weekly, monthly) for better farm management
- **Community connectivity** via a **Social Hub**, providing vital local updates and shared farming knowledge

By combining modern APIs, intuitive mobile-first design, and localized farming insights, AgriSense360 aims to drive food security, improve farmer incomes, and build more resilient rural economies in the face of climate uncertainty.

This is not just a tool — it is a lifeline for empowering rural communities towards sustainable agriculture and economic upliftment.

---

## Features

- **Weather Forecast Integration** (via AgroMonitoring API)
- **Soil Condition Tracking** (Soil pH, Microbial Health, Moisture)
- **Crop Recommendations** based on live environmental data
- **Yield & Profit Estimation Engine**
- **Daily Reports and Exportable CSV Files**
- **Historical Analysis:** Daily, Weekly, and Monthly Farm Performance
- **Social Hub for Community Messages and Agricultural Updates**

---

## Technologies Used

| Layer | Technology |
|------|------------|
| Frontend | HTML, CSS (Bootstrap), JavaScript |
| Backend | Python (Flask), REST APIs |
| APIs | AgroMonitoring API, OpenWeatherMap API (optional) |
| Hosting | Glitch (for combined backend and frontend) |
| Security | Environment Variables (Secrets Hidden) |

---

## Repository Structure

# /backend
# server.py         
Flask server (backend API endpoints)
# main.py            
Initial backend testing
# data_storage.py   
Data storage and export logic
# requirements.txt   
Python packages required

# /frontend
index.html         
Welcome Page
# dashboard.html     
Main Dashboard
# data_collection.html 
Dynamic Data Collection
# daily_report.html  
Daily Summary Reports
# history.html       
History of Data (Daily/Weekly/Monthly)
# social_hub.html    
Social Communication Hub
# script.js          
Frontend Dynamic Logic
# ags_logo.jpg       
Project Logo
# farming_bottom.jpg 
Footer Decoration Image

---

## Important Security Note

> **API keys and polygon ID are intentionally excluded from public view.**  
> 
> Before running the backend, users must manually insert their own API credentials into `server.py` and `main.py` or configure them through environment variables to enable full functionality.

---

## How to Run (Development Instructions)

1. **Backend Setup:**
    - Install Python 3.10+ and Flask
    - Install required packages:
      ```bash
      pip install -r backend/requirements.txt
      ```
    - Insert your personal API keys and polygon ID in `backend/server.py`
    - Start the Flask server:
      ```bash
      python backend/server.py
      ```

2. **Frontend Setup:**
    - Open the `frontend/index.html` in any modern web browser
    - Ensure the backend URL is correctly configured in `frontend/script.js`
    - Submit field data via Data Collection page and view real-time reports

---

## Team

- **Valerie Nhete** — Full Stack Developer, UI/UX Designer, Innovator

---


