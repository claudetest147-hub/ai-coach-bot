# 🤖 AI Coach Chatbot - Demo for PM Codesprint

Complete AI chatbot for coaching businesses. Built with FastAPI + Claude + React.

## 🎯 What This Is

Demo chatbot for **Mountain Coaching** - a life coach helping with career transitions.

**Features:**
- ✅ Natural conversations with Claude AI
- ✅ Trained on specific coaching business (pricing, process, FAQs)
- ✅ Handles 80% of common questions
- ✅ Escalates to human when needed
- ✅ Stores conversations in Supabase
- ✅ Beautiful React widget
- ✅ Mobile-responsive

## 📁 Project Structure

```
ai-coach-bot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── supabase_schema.sql  # Database schema
├── frontend/
│   ├── ChatWidget.tsx       # React chat component
│   └── ChatWidget.css       # Styles
└── deployment/
    ├── vercel.json          # Vercel config (coming)
    └── railway.json         # Railway config (coming)
```

## 🚀 Quick Start (Local Development)

### Prerequisites:
- Python 3.9+
- Node.js 18+
- Claude API key
- Supabase account

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your keys:
# - CLAUDE_API_KEY (from https://console.anthropic.com/)
# - SUPABASE_URL (from your Supabase project)
# - SUPABASE_KEY (anon key from Supabase)

# Run the server
python main.py
```

Backend will run at: http://localhost:8000

### Step 2: Database Setup

```bash
# Go to your Supabase project SQL editor
# Run the SQL from backend/supabase_schema.sql
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies (if using Create React App)
npm install

# Set API URL
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Run development server
npm start
```

Frontend will run at: http://localhost:3000

---

## 📦 Deployment

### Option 1: Deploy Backend to Railway (Easiest)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway init

# Add environment variables in Railway dashboard:
# - CLAUDE_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY

# Deploy
railway up
```

**Cost:** ~$5/month

### Option 2: Deploy Backend to Vercel (Serverless)

```bash
# Install Vercel CLI
npm install -g vercel

cd backend

# Create vercel.json (see deployment/ folder)
# Deploy
vercel --prod
```

**Cost:** Free tier available

### Option 3: Deploy Frontend as Widget

**Embed on any website:**

```html
<!-- Add to your website -->
<div id="chat-widget-root"></div>
<script src="https://your-domain.com/chat-widget.js"></script>
```

**Or use as standalone demo page**

---

## 🔧 Configuration

### Customizing for Different Coaches

Edit `backend/main.py` → `COACH_SYSTEM_PROMPT`

Change:
- Business name
- Pricing
- Services offered
- Coaching style
- Booking links
- Testimonials

### Customizing Widget Appearance

Edit `frontend/ChatWidget.css`:
- Colors (lines 15-17: gradient)
- Fonts (line 28)
- Sizing (lines 30-34)

---

## 💰 Cost Breakdown

**Running this demo:**

| Service | Cost | What it covers |
|---------|------|----------------|
| Claude API | ~$0.01/conversation | AI responses |
| Supabase | $0/month | Database (free tier) |
| Railway/Vercel | $0-5/month | Backend hosting |
| Frontend | $0 | Static hosting |

**Total: ~$5-10/month for unlimited conversations**

---

## 📊 Analytics

View conversation stats:

```bash
curl http://localhost:8000/stats
```

Returns:
```json
{
  "total_conversations": 42,
  "timestamp": "2026-03-07T15:00:00"
}
```

---

## 🧪 Testing

### Test the API:

```bash
# Health check
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your pricing?"}'
```

### Test the widget:

1. Open `frontend/index.html` in browser
2. Click chat bubble
3. Ask questions:
   - "What's your pricing?"
   - "How do I book a call?"
   - "Do you work with career transitions?"

---

## 🎨 Using This for Client Demos

### Demo Script:

1. **Show the widget:**
   - "This is what your clients will see on your website"
   - Click the bubble, show it opens

2. **Ask sample questions:**
   - "What's your pricing?" → Instant answer
   - "How do I book a call?" → Provides Calendly link
   - "Do you offer group coaching?" → Accurate answer

3. **Show edge cases:**
   - "I'm feeling suicidal" → Escalates appropriately
   - "Can you diagnose my depression?" → Declines properly

4. **Show admin view:**
   - Open Supabase dashboard
   - Show conversation logs
   - "You can see what clients are asking most"

### Customization Demo:

"I can customize this for YOUR coaching business in 5-7 days:
- Your pricing
- Your services
- Your brand voice
- Your booking link
- Embed on your website"

---

## 🔄 Updating the Bot Knowledge

To add new FAQs or change responses:

1. Edit `COACH_SYSTEM_PROMPT` in `backend/main.py`
2. Restart the server
3. Test new responses

**No retraining needed** - just update the prompt!

---

## 🚨 Common Issues

### "Claude API error"
- Check your API key in `.env`
- Verify you have credits at console.anthropic.com

### "Supabase connection failed"
- Check URL and key in `.env`
- Verify table exists (run schema SQL)

### "CORS error"
- Check `allow_origins` in `main.py` line 18
- Add your frontend domain

### Widget doesn't appear
- Check console for errors
- Verify API_URL in frontend `.env`

---

## 📈 Next Steps

### To Productize This:

1. **Multi-tenancy:**
   - Add `coach_id` to database
   - Support multiple coaches from one backend

2. **Admin Dashboard:**
   - View all conversations
   - Analytics (most asked questions)
   - Update knowledge base without code

3. **Advanced Features:**
   - Calendar integration (Google Calendar)
   - CRM integration (Zapier webhook)
   - Email notifications when human needed
   - Chat history per user

4. **White-label:**
   - Remove "Powered by AI" branding
   - Custom colors per client
   - Custom domain per client

---

## 💡 Sales Pitch (Copy-Paste)

"This chatbot can answer 80% of your client questions instantly:
- Pricing
- Booking
- Services
- Process

It works 24/7, never takes a day off, and costs less than $10/month to run.

Setup time: 5-7 days
Investment: $997

Want to see it in action?"

---

## 📞 Support

Questions? Email: hello@pmcodesprint.com

---

## ⚖️ License

Proprietary - PM Codesprint LLC © 2026

**Do not redistribute without permission.**
