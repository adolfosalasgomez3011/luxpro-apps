# FAMS - Freelance Applicator Management System

Mobile-first web application for managing LUX's network of freelance floor coating applicators.

## Tech Stack
- **Frontend**: Streamlit (Python)
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Streamlit Cloud

## Quick Start

### 1. Set up Supabase (5 minutes)
Follow instructions in [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
Edit `.streamlit/secrets.toml` with your Supabase credentials:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGc..."
```

### 4. Run App
```bash
streamlit run app.py
```

App will open at http://localhost:8501

## Features

- 📱 Mobile-optimized UI
- 👥 Freelancer management (CRUD)
- 🔍 Smart search and filters
- 📞 Quick call/WhatsApp actions
- ⭐ Rating system
- 📊 Dashboard with stats
- ☁️ Cloud database (access anywhere)

## Project Structure

```
FreelanceRecruiter/
├── app.py                    # Main Streamlit app
├── database_supabase.py      # Database operations
├── requirements.txt          # Dependencies
├── SUPABASE_SETUP.md        # Setup guide
├── .streamlit/
│   └── secrets.toml         # Supabase credentials (don't commit!)
└── docs/
    ├── System_Design_Document.md
    └── Mobile_MVP_Plan.md
```

## Deployment to Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repo
4. Add secrets in Streamlit Cloud dashboard (Settings → Secrets)
5. Deploy!

Your app will be live at: `https://your-app.streamlit.app`

## Usage

### Add Freelancer
1. Tap ➕ in bottom nav
2. Fill form
3. Save

### Find Available Freelancer
1. Go to 👥 Freelancers
2. Search by name or skill
3. Filter by location
4. Tap 📞 to call or 💬 for WhatsApp

### View Profile
1. Tap "👁️ Ver Más" on any card
2. See full details, skills, notes
3. View rating history
4. Edit or delete

## Mobile Access

Open the app URL on your phone browser, then:
- **iOS**: Tap Share → Add to Home Screen
- **Android**: Tap Menu → Add to Home Screen

App will work like a native app!

## Support

Questions? Contact adolfo.salas@goalpraxis.com
