import React from 'react';

export default function StudentForm({
  profile,
  onChange,
  onSubmit,
  isLoading,
  meta = {}
}) {
  const subjects = meta.subjects?.length
    ? meta.subjects
    : ['Python', 'DSA', 'Mathematics', 'Physics', 'Web Development'];

  const levels = meta.levels?.length
    ? meta.levels
    : ['Beginner', 'Intermediate', 'Advanced'];

  const goals = meta.goals?.length
    ? meta.goals
    : ['Exam Preparation', 'Concept Understanding', 'Practice', 'Project Building'];

  const types = meta.types?.length
    ? meta.types
    : ['Video', 'Notes', 'PPT', 'Interactive Practice', 'Quiz', 'Course'];

  const timePresets = meta.time_presets?.length
    ? meta.time_presets
    : [
        { label: 'Any duration (no limit)', minutes: '' },
        { label: '25 - 30 Minutes (Quick Sprint)', minutes: 30 },
        { label: '45 Minutes (Class Period)', minutes: 45 },
        { label: '1 Hour (Standard Session)', minutes: 60 },
        { label: '1.5 Hours (Deep Study)', minutes: 90 },
        { label: '2 Hours (Intensive)', minutes: 120 },
        { label: '3+ Hours (Masterclass)', minutes: 180 },
      ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange({
      ...profile,
      [name]: name === 'max_duration_minutes' ? (value ? Number(value) : null) : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(profile);
  };

  return (
    <div className="form-card">
      <div className="form-header">
        <div className="form-header-icon">🎯</div>
        <div className="form-header-text">
          <h3>Student Profile</h3>
          <p>Personalize your learning trajectory</p>
        </div>
      </div>

      <form id="student-form" className="student-form" onSubmit={handleSubmit}>
        {/* Name Input */}
        <div className="form-group">
          <label htmlFor="student-name" className="form-label">
            <span>👤</span> Your Name
          </label>
          <input
            id="student-name"
            name="name"
            type="text"
            className="form-input"
            placeholder="e.g. Alex"
            value={profile.name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Subject Select */}
        <div className="form-group">
          <label htmlFor="subject-select" className="form-label">
            <span>📚</span> Target Subject
          </label>
          <select
            id="subject-select"
            name="subject"
            className="form-select"
            value={profile.subject}
            onChange={handleChange}
            required
          >
            {subjects.map((sub) => (
              <option key={sub} value={sub}>
                {sub}
              </option>
            ))}
          </select>
        </div>

        {/* Proficiency Level */}
        <div className="form-group">
          <label htmlFor="level-select" className="form-label">
            <span>📈</span> Current Level
          </label>
          <select
            id="level-select"
            name="level"
            className="form-select"
            value={profile.level}
            onChange={handleChange}
            required
          >
            {levels.map((lvl) => (
              <option key={lvl} value={lvl}>
                {lvl}
              </option>
            ))}
          </select>
        </div>

        {/* Primary Goal */}
        <div className="form-group">
          <label htmlFor="goal-select" className="form-label">
            <span>🎯</span> Primary Goal
          </label>
          <select
            id="goal-select"
            name="goal"
            className="form-select"
            value={profile.goal}
            onChange={handleChange}
            required
          >
            {goals.map((g) => (
              <option key={g} value={g}>
                {g}
              </option>
            ))}
          </select>
        </div>

        {/* Available Study Time Selection */}
        <div className="form-group">
          <label htmlFor="time-select" className="form-label">
            <span>⏱️</span> Available Study Time
          </label>
          <select
            id="time-select"
            name="max_duration_minutes"
            className="form-select"
            value={profile.max_duration_minutes || ''}
            onChange={handleChange}
          >
            {timePresets.map((tp, idx) => (
              <option key={idx} value={tp.minutes ?? ''}>
                {tp.label}
              </option>
            ))}
          </select>
        </div>

        {/* Preferred Format (Optional) */}
        <div className="form-group">
          <label htmlFor="type-select" className="form-label">
            <span>✨</span> Preferred Format
          </label>
          <select
            id="type-select"
            name="preferred_type"
            className="form-select"
            value={profile.preferred_type || ''}
            onChange={handleChange}
          >
            <option value="">Any format (balanced)</option>
            {types.map((t) => (
              <option key={t} value={t}>
                {t === 'PPT' ? 'PPT (Presentation Slides)' : t}
              </option>
            ))}
          </select>
        </div>

        {/* Submit Button */}
        <button
          id="find-recommendations-btn"
          type="submit"
          className="submit-btn"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <div className="spinner" />
              <span>Analyzing Match Factors...</span>
            </>
          ) : (
            <>
              <span>⚡ Find Best Matches</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
