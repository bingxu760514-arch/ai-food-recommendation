import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  restaurants?: Restaurant[];
  timestamp: Date;
}

interface Restaurant {
  id: number;
  name: string;
  cuisine: string;
  price: number;
  rating: number;
  delivery_time: number;
  description: string;
  signature_dish?: string;
  reviews?: string;
  image1?: string;
  image2?: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '你好！我是AI外卖推荐助手🍽️。告诉我你想吃什么，我会根据你的位置和需求为你推荐合适的餐厅！',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      // 构建对话历史（只发送role和content，排除欢迎消息）
      const conversationHistory = messages
        .filter(msg => {
          // 排除欢迎消息和错误消息
          if (msg.role === 'assistant' && msg.content.includes('你好！我是AI外卖推荐助手')) {
            return false;
          }
          return true;
        })
        .map(msg => ({
          role: msg.role,
          content: msg.content
        }));

      const response = await axios.post('/api/chat', {
        message: userMessage.content,
        conversation_history: conversationHistory
      });

      // 检查响应数据
      if (response.data && response.data.message) {
        // 确保餐厅数据包含所有字段（包括图片）
        const restaurants = (response.data.restaurants || []).map((r: any) => {
          console.log('[前端] 接收到的餐厅数据:', r);
          console.log('[前端] 图片URL - image1:', r.image1, 'image2:', r.image2);
          return {
            ...r,
            image1: r.image1 || '',
            image2: r.image2 || ''
          };
        });
        
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.data.message,
          restaurants: restaurants,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('响应数据格式错误');
      }
    } catch (error: any) {
      console.error('发送消息失败:', error);
      if (error.response) {
        console.error('响应数据:', error.response.data);
      }
      
      // 尝试从错误响应中获取详细错误信息
      let errorMsg = '抱歉，发送消息时出现错误，请稍后重试。';
      if (error.response && error.response.data) {
        if (error.response.data.detail) {
          errorMsg = `错误：${error.response.data.detail}`;
        } else if (error.response.data.message) {
          errorMsg = error.response.data.message;
        }
      } else if (error.message) {
        errorMsg = `错误：${error.message}`;
      }
      
      const errorMessage: Message = {
        role: 'assistant',
        content: errorMsg,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.role === 'assistant' && (
                <div className="avatar">🤖</div>
              )}
              <div className="message-bubble">
                <div className="message-text">{message.content}</div>
                {message.restaurants && message.restaurants.length > 0 && (
                  <div className="restaurants-list">
                    {message.restaurants.map((restaurant) => (
                      <div key={restaurant.id} className="restaurant-card">
                        <div className="restaurant-header">
                          <h4>{restaurant.name}</h4>
                          <span className="cuisine-tag">{restaurant.cuisine}</span>
                        </div>
                        <div className="restaurant-info">
                          <div className="info-row">
                            <span className="price">💰 人均¥{restaurant.price}</span>
                            <span className="rating">⭐ {restaurant.rating}</span>
                            <span className="delivery">⏱️ {restaurant.delivery_time}分钟</span>
                          </div>
                        </div>

                        {restaurant.signature_dish && (
                          <div className="signature-dish">
                            <div className="signature-label">🍜 招牌菜</div>
                            <div className="dish-list">{restaurant.signature_dish}</div>
                            {(restaurant.image1 || restaurant.image2) && (
                              <div className="dish-images">
                                {restaurant.image1 && (
                                  <div className="dish-image-wrapper">
                                    <img 
                                      src={restaurant.image1} 
                                      alt={`${restaurant.name}招牌菜1`}
                                      className="dish-image"
                                      onLoad={() => {
                                        console.log('[前端] 图片1加载成功:', restaurant.image1);
                                      }}
                                      onError={(e) => {
                                        console.error('[前端] 图片1加载失败:', restaurant.image1);
                                        const img = e.target as HTMLImageElement;
                                        img.style.display = 'none';
                                        // 显示占位符
                                        const placeholder = document.createElement('div');
                                        placeholder.className = 'image-placeholder';
                                        placeholder.textContent = '图片加载失败';
                                        img.parentElement?.appendChild(placeholder);
                                      }}
                                    />
                                  </div>
                                )}
                                {restaurant.image2 && (
                                  <div className="dish-image-wrapper">
                                    <img 
                                      src={restaurant.image2} 
                                      alt={`${restaurant.name}招牌菜2`}
                                      className="dish-image"
                                      onLoad={() => {
                                        console.log('[前端] 图片2加载成功:', restaurant.image2);
                                      }}
                                      onError={(e) => {
                                        console.error('[前端] 图片2加载失败:', restaurant.image2);
                                        const img = e.target as HTMLImageElement;
                                        img.style.display = 'none';
                                        // 显示占位符
                                        const placeholder = document.createElement('div');
                                        placeholder.className = 'image-placeholder';
                                        placeholder.textContent = '图片加载失败';
                                        img.parentElement?.appendChild(placeholder);
                                      }}
                                    />
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        )}

                        {restaurant.reviews && (
                          <div className="reviews-section">
                            <div className="reviews-label">💬 用户评价</div>
                            <div className="reviews-list">
                              {restaurant.reviews.split('|').map((review, idx) => (
                                <div key={idx} className="review-item">
                                  <span className="review-icon">💭</span>
                                  <span className="review-text">{review}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        <p className="restaurant-desc">{restaurant.description}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              {message.role === 'user' && (
                <div className="avatar">👤</div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="avatar">🤖</div>
              <div className="message-bubble">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          ref={inputRef}
          type="text"
          className="chat-input"
          placeholder="告诉我你想吃什么..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button
          className="send-button"
          onClick={handleSend}
          disabled={loading || !inputMessage.trim()}
        >
          发送
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;

