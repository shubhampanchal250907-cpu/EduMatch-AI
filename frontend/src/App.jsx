import React, { useState, useEffect, useCallback } from 'react';
import StudentForm from './components/StudentForm';
import RecommendationList from './components/RecommendationList';
import './App.css';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function App() {
  const [profile, setProfile] = useState({
    name: 'Alex',
    subject: 'Python',
    level: 'Beginner',
    goal: 'Concept Understanding',
    preferred_type: 'Video',
    max_duration_minutes: 60,
    top_n: 5
  });

  const [recommendations, setRecommendations] = useState([]);
  const [studentInfo, setStudentInfo] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking'); // 'online' | 'offline' | 'checking'
  const [meta, setMeta] = useState({
    subjects: ['Python', 'DSA', 'Mathematics', 'Physics', 'Web Development'],
    levels: ['Beginner', 'Intermediate', 'Advanced'],
    goals: ['Exam Preparation', 'Concept Understanding', 'Practice', 'Project Building'],
    types: ['Video', 'Notes', 'PPT', 'Interactive Practice', 'Quiz', 'Course'],
    time_presets: [
      { label: 'Any duration (no limit)', minutes: '' },
      { label: '25 - 30 Minutes (Quick Sprint)', minutes: 30 },
      { label: '45 Minutes (Class Period)', minutes: 45 },
      { label: '1 Hour (Standard Session)', minutes: 60 },
      { label: '1.5 Hours (Deep Study)', minutes: 90 },
      { label: '2 Hours (Intensive)', minutes: 120 },
      { label: '3+ Hours (Masterclass)', minutes: 180 },
    ]
  });
  const [errorMsg, setErrorMsg] = useState(null);

  // Check Backend Status & Load Meta
  const checkBackendAndFetchMeta = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/meta`);
      if (res.ok) {
        const data = await res.json();
        setBackendStatus('online');
        if (data.subjects) {
          setMeta(data);
        }
      } else {
        setBackendStatus('offline');
      }
    } catch (err) {
      setBackendStatus('offline');
    }
  };

  // Fetch Recommendations
  const fetchRecommendations = useCallback(async (currentProfile) => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentProfile)
      });

      if (!res.ok) {
        throw new Error(`Server returned status: ${res.status}`);
      }

      const result = await res.json();
      if (result.success && result.data) {
        setRecommendations(result.data.recommendations || []);
        setStudentInfo(result.data.student || currentProfile);
        setBackendStatus('online');
      } else {
        throw new Error('Invalid response structure from backend');
      }
    } catch (err) {
      console.warn('API fetch failed:', err);
      setBackendStatus('offline');
      setErrorMsg(`Could not connect to FastAPI server at ${API_BASE_URL}. Ensure 'uvicorn backend.main:app' is running.`);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkBackendAndFetchMeta();
    fetchRecommendations(profile);
  }, []);

  // Quick Preset Handlers
  const applyPreset = (preset) => {
    const updated = { ...profile, ...preset };
    setProfile(updated);
    fetchRecommendations(updated);
  };

  return (
    <div className="app-container">
      {/* Navbar */}
      <header className="navbar">
        <div className="nav-brand">
          <span className="brand-icon">🎓</span>
          <h1 className="brand-title">
            EduMatch AI
            <span className="brand-badge">Engine v1.1 • Time-Aware</span>
          </h1>
        </div>

        <div className="nav-status">
          <div className="status-indicator">
            <span
              className={`status-dot ${backendStatus === 'online' ? 'online' : 'offline'}`}
            />
            <span style={{ color: backendStatus === 'online' ? '#34d399' : '#f87171' }}>
              {backendStatus === 'online' ? 'FastAPI Connected (Port 8000)' : 'FastAPI Offline'}
            </span>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <h2 className="hero-title">
          Smart Education <span>Recommendation Engine</span>
        </h2>
        <p className="hero-subtitle">
          Intelligent matching that considers your available study session time (e.g. videos ≤ 1 hour),
          curriculum depth, and provides direct downloads for PPT slide decks and revision notes.
        </p>

        {/* Quick Testing Presets */}
        <div className="quick-presets">
          <span className="preset-label">Instant Test Presets:</span>
          <button
            type="button"
            className="preset-btn"
            id="preset-py-video-1hr"
            onClick={() => applyPreset({ subject: 'Python', level: 'Beginner', goal: 'Concept Understanding', preferred_type: 'Video', max_duration_minutes: 60 })}
          >
            ⏱️ Python Video (≤ 1 Hour)
          </button>
          <button
            type="button"
            className="preset-btn"
            id="preset-py-ppt"
            onClick={() => applyPreset({ subject: 'Python', level: 'Beginner', goal: 'Exam Preparation', preferred_type: 'PPT', max_duration_minutes: 45 })}
          >
            📥 Python PPT Deck (Download)
          </button>
          <button
            type="button"
            className="preset-btn"
            id="preset-dsa-practice"
            onClick={() => applyPreset({ subject: 'DSA', level: 'Intermediate', goal: 'Practice', preferred_type: '', max_duration_minutes: 45 })}
          >
            ⚡ DSA Practice (≤ 45 mins)
          </button>
          <button
            type="button"
            className="preset-btn"
            id="preset-math-concepts"
            onClick={() => applyPreset({ subject: 'Mathematics', level: 'Beginner', goal: 'Concept Understanding', preferred_type: 'PPT', max_duration_minutes: 30 })}
          >
            📊 Math PPT Deck (≤ 30 mins)
          </button>
        </div>
      </section>

      {/* Optional Warning Banner if backend is offline */}
      {errorMsg && (
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto 1.5rem',
          padding: '0.75rem 1.5rem',
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '8px',
          color: '#fca5a5',
          fontSize: '0.875rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem'
        }}>
          <div>⚠️ {errorMsg}</div>
          <button
            onClick={() => {
              checkBackendAndFetchMeta();
              fetchRecommendations(profile);
            }}
            style={{
              background: '#ef4444',
              color: 'white',
              padding: '4px 10px',
              borderRadius: '4px',
              fontSize: '0.8rem',
              fontWeight: 600
            }}
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Main Grid: Left Form, Right Recommendations */}
      <main className="main-content">
        <StudentForm
          profile={profile}
          onChange={setProfile}
          onSubmit={fetchRecommendations}
          isLoading={isLoading}
          meta={meta}
        />

        <RecommendationList
          recommendations={recommendations}
          student={studentInfo}
          isLoading={isLoading}
        />
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>
          EduMatch AI • Smart Education GitHub Architecture Demo • Time-Constrained Recommendations & PPT/Notes Offline Download Ready
        </p>
      </footer>
    </div>
  );
}
