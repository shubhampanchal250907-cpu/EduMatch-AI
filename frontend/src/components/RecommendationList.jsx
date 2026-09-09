import React, { useState } from 'react';
import ResourceCard from './ResourceCard';

export default function RecommendationList({
  recommendations = [],
  student = {},
  isLoading = false,
  totalCandidates = 0,
}) {
  const [activeTypeFilter, setActiveTypeFilter] = useState('All');

  // Filter recommendations by type tab if requested
  const filteredRecommendations = activeTypeFilter === 'All'
    ? recommendations
    : recommendations.filter(item => item.type?.toLowerCase() === activeTypeFilter.toLowerCase());

  // Available categories for tabs
  const categories = ['All', 'Video', 'PPT', 'Notes', 'Interactive Practice', 'Quiz', 'Course'];

  if (isLoading) {
    return (
      <div className="recommendations-section">
        <div className="empty-state">
          <div className="spinner" style={{ width: '40px', height: '40px', margin: '0 auto 1rem' }} />
          <h3>Curating Personalized Trajectory</h3>
          <p>Scoring curriculum resources using multi-factor weighted matching...</p>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-section">
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h3>No Recommendations Match Criteria</h3>
          <p>
            Try increasing your available study time or changing your format preference to explore more resources.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="recommendations-section">
      {/* Results Header */}
      <div className="results-header">
        <div className="results-summary">
          <h2>
            <span>✨</span> Recommended For You
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 500 }}>
              ({filteredRecommendations.length} of {recommendations.length} matched)
            </span>
          </h2>
          <div className="student-tag-list">
            {student.name && <span className="student-chip highlight">👤 {student.name}</span>}
            {student.subject && <span className="student-chip">📚 {student.subject}</span>}
            {student.level && <span className="student-chip">📶 {student.level}</span>}
            {student.goal && <span className="student-chip">🎯 {student.goal}</span>}
            {student.max_duration_minutes && (
              <span className="student-chip highlight-time">
                ⏱️ Max {student.max_duration_minutes} mins
              </span>
            )}
            {student.preferred_type && (
              <span className="student-chip">
                ✨ Format: {student.preferred_type}
              </span>
            )}
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="filter-tabs">
          {categories.map((cat) => {
            const count = cat === 'All'
              ? recommendations.length
              : recommendations.filter(r => r.type?.toLowerCase() === cat.toLowerCase()).length;

            if (cat !== 'All' && count === 0) return null;

            return (
              <button
                key={cat}
                type="button"
                className={`tab-btn ${activeTypeFilter === cat ? 'active' : ''}`}
                onClick={() => setActiveTypeFilter(cat)}
              >
                {cat} ({count})
              </button>
            );
          })}
        </div>
      </div>

      {/* Resource Cards Grid */}
      <div className="cards-grid">
        {filteredRecommendations.map((resource, idx) => (
          <ResourceCard key={resource.id || idx} resource={resource} index={idx} />
        ))}
      </div>
    </div>
  );
}
