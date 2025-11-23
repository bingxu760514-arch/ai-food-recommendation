import React from 'react';
import './RestaurantList.css';

interface Restaurant {
  id: number;
  name: string;
  cuisine: string;
  price: number;
  rating: number;
  delivery_time: number;
  description: string;
}

interface RestaurantListProps {
  restaurants: Restaurant[];
  loading: boolean;
}

const RestaurantList: React.FC<RestaurantListProps> = ({ restaurants, loading }) => {
  if (loading) {
    return (
      <div className="restaurant-list">
        <div className="loading">加载中...</div>
      </div>
    );
  }

  if (restaurants.length === 0) {
    return (
      <div className="restaurant-list">
        <div className="empty-state">
          <p>😕 没有找到符合条件的餐厅</p>
          <p>请尝试调整筛选条件</p>
        </div>
      </div>
    );
  }

  const renderStars = (rating: number) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const stars = [];

    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i} className="star full">★</span>);
    }
    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">★</span>);
    }

    return <div className="stars">{stars}</div>;
  };

  return (
    <div className="restaurant-list">
      <h2>推荐结果 ({restaurants.length})</h2>
      <div className="restaurant-grid">
        {restaurants.map(restaurant => (
          <div key={restaurant.id} className="restaurant-card">
            <div className="restaurant-header">
              <h3>{restaurant.name}</h3>
              <span className="cuisine-tag">{restaurant.cuisine}</span>
            </div>
            
            <p className="description">{restaurant.description}</p>
            
            <div className="restaurant-info">
              <div className="info-item">
                {renderStars(restaurant.rating)}
                <span className="rating-text">{restaurant.rating}</span>
              </div>
              
              <div className="info-item">
                <span className="price">¥{restaurant.price}</span>
              </div>
              
              <div className="info-item">
                <span className="delivery">⏱️ {restaurant.delivery_time}分钟</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RestaurantList;




