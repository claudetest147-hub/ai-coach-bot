-- Create conversations table for AI Coach Bot

CREATE TABLE IF NOT EXISTS public.conversations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  session_id TEXT NOT NULL,
  user_message TEXT NOT NULL,
  bot_response TEXT NOT NULL,
  needs_human BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast session lookups
CREATE INDEX IF NOT EXISTS idx_conversations_session_id 
  ON public.conversations(session_id);

-- Index for date-based queries
CREATE INDEX IF NOT EXISTS idx_conversations_created_at 
  ON public.conversations(created_at DESC);

-- Enable RLS (optional - for security)
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations (since this is backend-only)
CREATE POLICY "Allow all operations for service role"
  ON public.conversations
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Comment
COMMENT ON TABLE public.conversations IS 'Stores all chatbot conversations for analytics and improvement';
