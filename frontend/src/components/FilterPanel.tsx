import React, { useState } from 'react';
import './FilterPanel.css';

interface FilterOptions {
  cuisine: string;
  minPrice: number | null;
  maxPrice: number | null;
  minRating: number | null;
  maxDeliveryTime: number | null;
  keyword: string;
}

interface FilterPanelProps {
  cuisines: string[];
  filters: FilterOptions;
  onFilter: (filters: FilterOptions) => void;
  loading: boolean;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ cuisines, filters, onFilter, loading }) => {
  const [localFilters, setLocalFilters] = useState<FilterOptions>(filters);

  const handleChange = (key: keyof FilterOptions, value: any) => {
    setLocalFilters(prev => ({
      ...prev,
      [key]: value === '' ? null : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onFilter(localFilters);
  };

  const handleReset = () => {
    const resetFilters: FilterOptions = {
      cuisine: '',
      minPrice: null,
      maxPrice: null,
      minRating: null,
      maxDeliveryTime: null,
      keyword: ''
    };
    setLocalFilters(resetFilters);
    onFilter(resetFilters);
  };

  return (
    <div className="filter-panel">
      <h2>筛选条件</h2>
      <form onSubmit={handleSubmit}>
        <div className="filter-row">
          <div className="filter-group">
            <label>菜系类型</label>
            <select
              value={localFilters.cuisine}
              onChange={(e) => handleChange('cuisine', e.target.value)}
            >
              <option value="">全部</option>
              {cuisines.map(cuisine => (
                <option key={cuisine} value={cuisine}>{cuisine}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>价格范围（元）</label>
            <div className="price-range">
              <input
                type="number"
                placeholder="最低"
                value={localFilters.minPrice || ''}
                onChange={(e) => handleChange('minPrice', e.target.value ? parseFloat(e.target.value) : null)}
                min="0"
              />
              <span> - </span>
              <input
                type="number"
                placeholder="最高"
                value={localFilters.maxPrice || ''}
                onChange={(e) => handleChange('maxPrice', e.target.value ? parseFloat(e.target.value) : null)}
                min="0"
              />
            </div>
          </div>

          <div className="filter-group">
            <label>最低评分</label>
            <select
              value={localFilters.minRating || ''}
              onChange={(e) => handleChange('minRating', e.target.value ? parseFloat(e.target.value) : null)}
            >
              <option value="">不限</option>
              <option value="4.0">4.0分以上</option>
              <option value="4.2">4.2分以上</option>
              <option value="4.4">4.4分以上</option>
              <option value="4.5">4.5分以上</option>
              <option value="4.6">4.6分以上</option>
            </select>
          </div>

          <div className="filter-group">
            <label>最长配送时间（分钟）</label>
            <select
              value={localFilters.maxDeliveryTime || ''}
              onChange={(e) => handleChange('maxDeliveryTime', e.target.value ? parseInt(e.target.value) : null)}
            >
              <option value="">不限</option>
              <option value="20">20分钟内</option>
              <option value="30">30分钟内</option>
              <option value="40">40分钟内</option>
              <option value="50">50分钟内</option>
            </select>
          </div>
        </div>

        <div className="filter-row">
          <div className="filter-group keyword-group">
            <label>关键词搜索</label>
            <input
              type="text"
              placeholder="输入餐厅名或菜品关键词"
              value={localFilters.keyword}
              onChange={(e) => handleChange('keyword', e.target.value)}
            />
          </div>
        </div>

        <div className="filter-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? '搜索中...' : '开始推荐'}
          </button>
          <button type="button" className="btn-secondary" onClick={handleReset}>
            重置筛选
          </button>
        </div>
      </form>
    </div>
  );
};

export default FilterPanel;




