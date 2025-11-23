import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🍽️ AI外卖推荐助手</h1>
        <p>聊天式交互，根据您的位置和需求智能推荐美食</p>
      </header>

      <main className="App-main">
        <div className="container">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}

export default App;




