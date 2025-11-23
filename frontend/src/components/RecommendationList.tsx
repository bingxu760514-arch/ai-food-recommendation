import React from 'react';
import './RecommendationList.css';

interface Recommendation {
  restaurant_id: number;
  name: string;
  reason: string;
}

interface RecommendationListProps {
  recommendations: Recommendation[];
}

const RecommendationList: React.FC<RecommendationListProps> = ({ recommendations }) => {
  if (recommendations.length === 0) {
    return null;
  }

  return (
    <div className="recommendation-list">
      <h2>🤖 AI智能推荐</h2>
      <div className="recommendation-items">
        {recommendations.map((rec, index) => (
          <div key={rec.restaurant_id || index} className="recommendation-item">
            <div className="recommendation-header">
              <span className="recommendation-number">{index + 1}</span>
              <h3>{rec.name}</h3>
            </div>
            <p className="recommendation-reason">{rec.reason}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationList;




