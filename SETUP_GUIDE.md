# 🚀 Quick Setup Guide - Get Running in 30 Minutes

## ✅ Checklist Before Starting

- [ ] Claude API key (get from https://console.anthropic.com/)
- [ ] Supabase account (reuse from DrinkUp or create new)
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed

---

## 📋 Step-by-Step Setup

### Step 1: Get Claude API Key (5 min)

1. Go to https://console.anthropic.com/
2. Sign in / Create account
3. Click "Get API Keys"
4. Create new key
5. Copy it (starts with `sk-ant-api03-...`)

**Cost:** $5 credit free, then ~$0.01 per conversation

---

### Step 2: Set Up Supabase Database (5 min)

**Option A: Use existing DrinkUp project**

1. Go to https://supabase.com/dashboard/project/yicbsjkdioiknonuuhvf
2. Click "SQL Editor"
3. Click "New Query"
4. Copy contents of `backend/supabase_schema.sql`
5. Paste and click "Run"
6. Done! Table created.

**Option B: Create new project**

1. Go to https://supabase.com/
2. Click "New Project"
3. Name: "ai-coach-bot"
4. Wait 2 minutes for provisioning
5. Go to SQL Editor
6. Run `backend/supabase_schema.sql`
7. Copy URL and anon key from Settings

---

### Step 3: Configure Backend (5 min)

```bash
cd /Users/pmcodesprint/.openclaw/workspace/ai-coach-bot/backend

# Create .env file
cp .env.example .env

# Edit .env (use your favorite editor)
nano .env

# Add your keys:
CLAUDE_API_KEY=sk-ant-api03-... (from Step 1)
SUPABASE_URL=https://yicbsjkdioiknonuuhvf.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Save and exit (Ctrl+X, Y, Enter)
```

---

### Step 4: Install & Run Backend (10 min)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test it:**
```bash
# Open new terminal
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "claude_api": "configured",
  "supabase": "configured"
}
```

✅ **Backend is running!**

---

### Step 5: Test with Simple HTML (5 min)

Create a test file:

```bash
cd /Users/pmcodesprint/.openclaw/workspace/ai-coach-bot
cat > test.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AI Coach Bot Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        #response {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
            white-space: pre-wrap;
        }
        button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>🤖 AI Coach Bot Test</h1>
    
    <input 
        type="text" 
        id="message" 
        placeholder="Ask a question (e.g., 'What's your pricing?')"
        value="What's your pricing?"
    />
    
    <button onclick="sendMessage()">Send Message</button>
    
    <div id="response"></div>

    <script>
        async function sendMessage() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('response');
            
            responseDiv.textContent = '⏳ Thinking...';
            
            try {
                const response = await fetch('http://localhost:8000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                responseDiv.textContent = `🤖 Bot: ${data.response}`;
            } catch (error) {
                responseDiv.textContent = `❌ Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
EOF

# Open in browser
open test.html
```

Click "Send Message" → Should get instant response about pricing!

✅ **Bot is working!**

---

## 🎥 Record Demo Video (10 min)

Now that it's working, record your demo:

### What to show:

1. **Open test.html** (or the widget)
2. **Ask these questions:**
   - "What's your pricing?" → Shows packages
   - "How do I book a call?" → Provides link
   - "Do you offer career coaching?" → Says yes
   - "What's included in a 3-month package?" → Details

3. **Screen record** (use QuickTime or OBS)
4. **Keep it under 2 minutes**

### Video Script:

"This is an AI chatbot I built for coaching businesses. 
Watch how it answers client questions instantly...
[Ask questions]
...This saves coaches 15-20 hours per week of repetitive questions.
Setup takes 5-7 days. Interested? DM me."

---

## 📦 Next: Deploy to Production

Once you've tested locally, deploy:

### Option 1: Railway (Easiest)

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway init
railway up
```

**You get:** `https://your-app.railway.app`

### Option 2: Vercel (Free)

```bash
npm install -g vercel

cd backend
vercel --prod
```

**You get:** `https://your-app.vercel.app`

---

## 🎯 You're Done!

You now have:
✅ Working AI chatbot
✅ Demo you can show
✅ Ready to customize for clients

**Cost to run:** $5-10/month
**Time to set up for client:** 5-7 days
**Price to charge:** $997-2,497

---

## 🚨 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Claude API error"
- Check your API key is correct
- Verify you have credits: https://console.anthropic.com/

### "Supabase error"
- Run the SQL schema again
- Check your keys in .env
- Try with DrinkUp database first (you know that works)

### Port 8000 already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

---

## 📞 Need Help?

**DM me on Twitter or email hello@pmcodesprint.com**

But honestly, if you got DrinkUp working, this is 10x easier. You got this! 🚀
