import React from 'react';

export default function ResourceCard({ resource, index }) {
  const {
    title,
    description,
    subject,
    level,
    type,
    score = 85.0,
    rating = 4.8,
    duration = '2 hours',
    duration_minutes,
    author = 'EduMatch Expert',
    url = '#',
    download_url,
    downloadable = false,
    tags = [],
    explanation = {},
    breakdown = {}
  } = resource;

  const isHighScore = score >= 90;
  const scoreClass = isHighScore ? 'high' : 'medium';

  // Format type icons
  const typeIcons = {
    'Video': '🎥',
    'Notes': '📝',
    'PPT': '📊',
    'Interactive Practice': '💻',
    'Quiz': '🧠',
    'Course': '🎓',
  };
  const icon = typeIcons[type] || '📖';

  // Check if resource can be downloaded (PPTs, Notes, or marked downloadable)
  const isDownloadable = downloadable || type === 'Notes' || type === 'PPT' || Boolean(download_url);
  const downloadLink = download_url || url;

  return (
    <div className="resource-card" id={`resource-card-${resource.id || index}`}>
      {/* Top Row: Badges & Score */}
      <div className="card-top-row">
        <div className="badge-group">
          <span className="badge badge-type">
            {icon} {type}
          </span>
          <span className="badge badge-level">
            📶 {level}
          </span>
          <span className="badge badge-subject">
            {subject}
          </span>
          {breakdown?.time_fits && breakdown?.max_minutes && (
            <span className="badge badge-time-fit" title="Fits inside your selected study time">
              ⏱️ Fits {breakdown.max_minutes}m limit
            </span>
          )}
        </div>

        <div className={`score-pill ${scoreClass}`} title="Calculated by multi-factor engine">
          <span>✨</span>
          <span>{score}% Match</span>
        </div>
      </div>

      {/* Title & Description */}
      <h3 className="card-title">{title}</h3>
      <p className="card-desc">{description}</p>

      {/* Metadata */}
      <div className="card-meta">
        <span className="meta-item rating">
          ⭐ {rating} / 5.0
        </span>
        <span className="meta-item">
          ⏱️ {duration} {duration_minutes ? `(~${duration_minutes} mins)` : ''}
        </span>
        <span className="meta-item">
          👨‍🏫 {author}
        </span>
        {isDownloadable && (
          <span className="meta-item downloadable-indicator">
            💾 Offline Download Ready
          </span>
        )}
      </div>

      {/* Explainable AI Callout */}
      {explanation && explanation.summary && (
        <div className="xai-box">
          <div className="xai-header">
            <span>💡</span> Why Recommended
          </div>
          <p className="xai-summary">{explanation.summary}</p>
          {explanation.reasons && explanation.reasons.length > 0 && (
            <ul className="xai-reasons-list">
              {explanation.reasons.map((reason, rIdx) => (
                <li key={rIdx}>{reason}</li>
              ))}
            </ul>
          )}
          {explanation.badges && explanation.badges.length > 0 && (
            <div className="xai-badges-row">
              {explanation.badges.map((badge, bIdx) => (
                <span key={bIdx} className="xai-pill-badge">
                  {badge}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Footer / Action */}
      <div className="card-footer">
        <div className="tag-list">
          {tags.slice(0, 4).map((tag, tIdx) => (
            <span key={tIdx} className="tag-item">
              #{tag}
            </span>
          ))}
        </div>

        <div className="card-actions-group">
          {/* Dedicated Download Option for Notes or PPT */}
          {isDownloadable && (
            <a
              href={downloadLink}
              target="_blank"
              rel="noopener noreferrer"
              download
              className="download-resource-btn"
              id={`download-btn-${resource.id || index}`}
              title={`Download ${type === 'PPT' ? 'PowerPoint Presentation (.pptx)' : 'Notes (.pdf)'}`}
            >
              <span>📥 Download {type === 'PPT' ? 'PPT Deck' : 'Notes'}</span>
            </a>
          )}

          {/* Open Material Online */}
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="open-resource-btn"
            id={`open-btn-${resource.id || index}`}
          >
            <span>{type === 'Video' ? '▶ Watch Video' : 'Open Material'}</span>
            <span>↗</span>
          </a>
        </div>
      </div>
    </div>
  );
}
