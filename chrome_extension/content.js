// Create the floating panel
const panel = document.createElement('div');
panel.id = 'ai-assistant-panel';
panel.innerHTML = `
  <div class="ai-panel-collapsed">
    <span class="ai-icon">🤖</span>
    <span>Ask AI</span>
  </div>
  <div class="ai-panel-expanded" style="display: none;">
    <div class="ai-panel-header">
      <span>🤖 AI Assistant</span>
      <button class="close-btn">✕</button>
    </div>
    <div class="ai-chat-container">
      <div id="ai-messages"></div>
    </div>
    <div class="ai-input-container">
      <input type="text" id="ai-input" placeholder="Ask me anything...">
      <button id="ai-send-btn">➤</button>
    </div>
  </div>
`;

document.body.appendChild(panel);

const collapsed = panel.querySelector('.ai-panel-collapsed');
const expanded = panel.querySelector('.ai-panel-expanded');
const closeBtn = panel.querySelector('.close-btn');
const sendBtn = panel.querySelector('#ai-send-btn');
const input = panel.querySelector('#ai-input');
const messages = panel.querySelector('#ai-messages');

// Toggle panel - open
collapsed.addEventListener('click', () => {
  collapsed.style.display = 'none';
  expanded.style.display = 'flex';
  input.focus(); // Auto-focus input when opened
});

// Toggle panel - close
closeBtn.addEventListener('click', () => {
  expanded.style.display = 'none';
  collapsed.style.display = 'flex';
});

// Send message
sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'  // For Development
  : 'https://production-api.com';  // For Production (replace with your actual domain)

async function sendMessage() {
  const question = input.value.trim();
  if (!question) return;
  
  addMessage(question, 'user');
  input.value = '';
  
  addTypingIndicator();
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        page_url: window.location.href,
        question: question
      })
    });
    
    if (response.status !== 200) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    removeTypingIndicator();
    
    addMessage(data.response, 'ai');
    
  } catch (error) {
    removeTypingIndicator();
    addMessage(`❌ Error: Could not connect to AI server. Make sure your Python server is running on http://localhost:8000 and the error is ${error.message}`, 'ai');
    console.error('API Error:', error);
  }
}

function addMessage(text, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${sender}-message`;
  msgDiv.textContent = text;
  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight;
}

function addTypingIndicator() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'typing-indicator';
  typingDiv.id = 'typing';
  typingDiv.innerHTML = '<span></span><span></span><span></span>';
  messages.appendChild(typingDiv);
  messages.scrollTop = messages.scrollHeight;
}

function removeTypingIndicator() {
  const typing = document.getElementById('typing');
  if (typing) typing.remove();
}