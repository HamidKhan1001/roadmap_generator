'use client';

import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function Home() {
  const [options, setOptions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [roadmap, setRoadmap] = useState(null);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    name: '',
    email: '',
    country: 'Pakistan',
    interest: '',
    goal: '',
    level: 'beginner',
    weekly_hours: 8,
    language_preference: 'Urdu/Hindi',
    preferred_platforms: ['youtube', 'docs'],
    skills: ''
  });

  useEffect(() => {
    fetch(`${API_URL}/api/options`)
      .then((res) => res.json())
      .then(setOptions)
      .catch(() => setOptions(null));
  }, []);

  function updateField(name, value) {
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  function togglePlatform(platform) {
    setForm((prev) => {
      const current = new Set(prev.preferred_platforms);
      current.has(platform) ? current.delete(platform) : current.add(platform);
      return { ...prev, preferred_platforms: Array.from(current) };
    });
  }

  async function submit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    setRoadmap(null);

    const payload = {
      ...form,
      weekly_hours: Number(form.weekly_hours),
      skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean)
    };

    try {
      const res = await fetch(`${API_URL}/api/roadmaps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(JSON.stringify(data.errors || data));
      setRoadmap(data);
    } catch (err) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <div className="heroText">
          <p className="badge">Mittu AI Roadmap Builder</p>
          <h1>Turn your interest into a clear learning roadmap.</h1>
          <p className="subtitle">
            Mittu reads your profile, chooses a practical track, saves your roadmap in MongoDB,
            and generates the PDF only when you download it.
          </p>
        </div>
        <div className="robotWrap">
          <div className="robot">
            <div className="antenna" />
            <div className="head">
              <span className="eye" />
              <span className="eye" />
            </div>
            <div className="bodyBot">M</div>
          </div>
        </div>
      </section>

      <section className="grid">
        <form className="card form" onSubmit={submit}>
          <h2>Create roadmap</h2>
          <label>Name<input value={form.name} onChange={(e) => updateField('name', e.target.value)} required /></label>
          <label>Email<input value={form.email} onChange={(e) => updateField('email', e.target.value)} /></label>
          <label>Country<input value={form.country} onChange={(e) => updateField('country', e.target.value)} /></label>
          <label>Interest<textarea value={form.interest} onChange={(e) => updateField('interest', e.target.value)} required placeholder="Example: I want to learn AI, Python, frontend, freelancing..." /></label>
          <label>Goal<textarea value={form.goal} onChange={(e) => updateField('goal', e.target.value)} placeholder="Example: get a job, build SaaS, start freelancing..." /></label>
          <div className="row">
            <label>Level
              <select value={form.level} onChange={(e) => updateField('level', e.target.value)}>
                {(options?.levels || ['beginner', 'intermediate', 'advanced']).map((level) => <option key={level}>{level}</option>)}
              </select>
            </label>
            <label>Hours/week<input type="number" min="1" max="80" value={form.weekly_hours} onChange={(e) => updateField('weekly_hours', e.target.value)} /></label>
          </div>
          <label>Language preference
            <select value={form.language_preference} onChange={(e) => updateField('language_preference', e.target.value)}>
              {(options?.languages || ['English', 'Urdu/Hindi', 'Mixed']).map((language) => <option key={language}>{language}</option>)}
            </select>
          </label>
          <label>Current skills, comma separated<input value={form.skills} onChange={(e) => updateField('skills', e.target.value)} placeholder="python basics, editing, excel" /></label>
          <div>
            <p className="miniTitle">Preferred platforms</p>
            <div className="chips">
              {(options?.platforms || ['youtube', 'docs', 'course', 'practice']).map((p) => (
                <button type="button" key={p} className={form.preferred_platforms.includes(p) ? 'chip active' : 'chip'} onClick={() => togglePlatform(p)}>{p}</button>
              ))}
            </div>
          </div>
          <button className="submit" disabled={loading}>{loading ? 'Generating...' : 'Generate roadmap'}</button>
          {error && <pre className="error">{error}</pre>}
        </form>

        <section className="card result">
          {!roadmap ? (
            <div className="empty">
              <h2>Your roadmap will appear here</h2>
              <p>It will include phases, resources, projects, next steps, and a PDF download.</p>
            </div>
          ) : (
            <Roadmap data={roadmap} />
          )}
        </section>
      </section>

      <footer>Made with ❤️ by Hamid</footer>
    </main>
  );
}

function Roadmap({ data }) {
  const r = data.roadmap;
  return (
    <div>
      <p className="badge">{r.duration_weeks} weeks · {r.weekly_hours} hrs/week</p>
      <h2>{r.track_name}</h2>
      <p>{r.summary}</p>
      <a className="download" href={`${API_URL}/api/roadmap/${data.request_id}/pdf`}>Download PDF</a>
      <div className="timeline">
        {r.phases.map((phase) => (
          <article className="phase" key={phase.title}>
            <strong>{phase.weeks}: {phase.title}</strong>
            <ul>{phase.outcomes.map((item) => <li key={item}>{item}</li>)}</ul>
            <p><b>Project:</b> {phase.project}</p>
          </article>
        ))}
      </div>
      <h3>Resources</h3>
      <div className="resources">
        {r.resources.map((resource) => (
          <a href={resource.url} target="_blank" rel="noreferrer" key={resource.title}>
            <span>{resource.type}</span>
            {resource.title}
          </a>
        ))}
      </div>
    </div>
  );
}
