import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Fab,
  Paper,
  TextField,
  IconButton,
  List,
  ListItem,
  Typography,
  CircularProgress,
  useTheme,
  Fade
} from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

const N8nChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "안녕하세요! 무엇을 도와드릴까요?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const theme = useTheme();

  // Replace this with your actual n8n webhook URL
  const WEBHOOK_URL = 'YOUR_N8N_WEBHOOK_URL_HERE';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Check if URL is configured
      if (WEBHOOK_URL === 'YOUR_N8N_WEBHOOK_URL_HERE') {
        setTimeout(() => {
          setMessages(prev => [...prev, { 
            text: "⚠️ n8n Webhook URL이 설정되지 않았습니다. 코드에서 URL을 업데이트해주세요.", 
            sender: 'bot' 
          }]);
          setIsLoading(false);
        }, 1000);
        return;
      }

      const response = await fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      // Assuming n8n returns { output: "response text" } or similar. Adjust based on your n8n workflow.
      const botResponseText = data.output || data.text || data.message || JSON.stringify(data);

      setMessages(prev => [...prev, { text: botResponseText, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { text: "죄송합니다. 오류가 발생했습니다.", sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="chat"
        onClick={() => setIsOpen(!isOpen)}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          zIndex: 1000,
        }}
      >
        {isOpen ? <CloseIcon /> : <ChatIcon />}
      </Fab>

      {/* Chat Window */}
      <Fade in={isOpen}>
        <Paper
          elevation={6}
          sx={{
            position: 'fixed',
            bottom: 90,
            right: 24,
            width: 350,
            height: 500,
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          {/* Header */}
          <Box
            sx={{
              p: 2,
              bgcolor: 'primary.main',
              color: 'primary.contrastText',
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}
          >
            <SmartToyIcon />
            <Typography variant="h6">AI Assistant</Typography>
          </Box>

          {/* Messages Area */}
          <List sx={{ flexGrow: 1, overflow: 'auto', p: 2, bgcolor: '#f5f5f5' }}>
            {messages.map((msg, index) => (
              <ListItem
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 1,
                  px: 0
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 1.5,
                    maxWidth: '80%',
                    bgcolor: msg.sender === 'user' ? 'primary.light' : 'white',
                    color: msg.sender === 'user' ? 'primary.contrastText' : 'text.primary',
                    borderRadius: 2,
                    borderTopRightRadius: msg.sender === 'user' ? 0 : 2,
                    borderTopLeftRadius: msg.sender === 'bot' ? 0 : 2,
                  }}
                >
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                    {msg.text}
                  </Typography>
                </Paper>
              </ListItem>
            ))}
            {isLoading && (
              <ListItem sx={{ justifyContent: 'flex-start', px: 0 }}>
                <Paper sx={{ p: 1.5, bgcolor: 'white', borderRadius: 2 }}>
                  <CircularProgress size={20} />
                </Paper>
              </ListItem>
            )}
            <div ref={messagesEndRef} />
          </List>

          {/* Input Area */}
          <Box sx={{ p: 2, bgcolor: 'white', borderTop: 1, borderColor: 'divider', display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="메시지를 입력하세요..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              multiline
              maxRows={3}
            />
            <IconButton 
              color="primary" 
              onClick={handleSend} 
              disabled={!input.trim() || isLoading}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Paper>
      </Fade>
    </>
  );
};

export default N8nChat;
