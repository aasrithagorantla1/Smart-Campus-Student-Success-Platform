import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="page-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Smart Campus</p>
          <h1>Student Success Platform</h1>
        </div>
        <button class="primary-btn">Login</button>
      </header>

      <main class="content">
        <section class="hero panel">
          <div>
            <span class="badge">Rules-based analytics</span>
            <h2>College and department overview</h2>
            <p>Monitor academic risk, placement readiness, interventions, and student support needs.</p>
          </div>

          <div class="stats-grid">
            <div class="stat-box"><strong>150</strong><span>Students</span></div>
            <div class="stat-box"><strong>6</strong><span>Monthly periods</span></div>
            <div class="stat-box"><strong>3</strong><span>Departments</span></div>
          </div>
        </section>

        <section class="cards-grid">
          <article class="panel">
            <h3>Academic risk list</h3>
            <ul>
              <li><span class="dot high"></span> 9 high-risk students</li>
              <li><span class="dot medium"></span> 27 medium-risk students</li>
              <li><span class="dot low"></span> 114 low-risk students</li>
            </ul>
          </article>

          <article class="panel">
            <h3>Placement readiness</h3>
            <ul>
              <li>Strong academics, low placement readiness</li>
              <li>Skills-led candidates</li>
              <li>Placement data pending review</li>
            </ul>
          </article>

          <article class="panel">
            <h3>Segments</h3>
            <ul>
              <li>Improving after intervention</li>
              <li>Declining attendance and results</li>
              <li>Consistently performing well</li>
            </ul>
          </article>
        </section>
      </main>
    </div>
  `,
  styles: [
    `
      :host { display: block; min-height: 100vh; background: #f3f8fb; color: #102d3a; font-family: Arial, sans-serif; }
      .page-shell { max-width: 1200px; margin: 0 auto; padding: 32px 20px 60px; }
      .topbar { background: #0d2033; color: white; border-radius: 18px; padding: 20px 24px; display:flex; justify-content:space-between; align-items:center; }
      .eyebrow { margin: 0 0 6px; text-transform: uppercase; letter-spacing: 0.12em; font-size: 12px; color: #9acfe8; }
      h1 { margin: 0; font-size: clamp(1.8rem, 3vw, 2.5rem); }
      .primary-btn { background: #18a9ad; color: white; border: none; padding: 0.9rem 1.2rem; border-radius: 12px; font-weight: 700; }
      .content { margin-top: 24px; }
      .panel { background: white; border: 1px solid #dfeaf2; border-radius: 18px; box-shadow: 0 10px 18px rgba(16,45,58,0.06); padding: 24px; }
      .hero { display:flex; justify-content:space-between; gap: 20px; align-items:center; }
      .badge { display:inline-block; background:#defaf8; color:#0f6e73; border-radius: 999px; padding: 6px 10px; font-size: 12px; font-weight:700; }
      h2 { margin-top: 12px; margin-bottom: 8px; }
      .stats-grid { display:flex; gap:16px; flex-wrap: wrap; }
      .stat-box { background:#f5fbff; border:1px solid #dfeaf2; border-radius: 12px; min-width: 120px; padding: 18px 16px; text-align: center; }
      .stat-box strong { display:block; font-size: 2rem; }
      .stat-box span { color:#547087; }
      .cards-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:18px; margin-top: 18px; }
      ul { list-style:none; padding:0; margin:0; }
      li { margin: 8px 0; }
      .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px; }
      .dot.high { background:#d94d4d; }
      .dot.medium { background:#f2a93b; }
      .dot.low { background:#4aa7d8; }
      @media (max-width: 720px) { .hero { flex-direction: column; align-items:flex-start; } .topbar { flex-direction: column; align-items:flex-start; gap: 10px; } }
    `
  ]
})
export class AppComponent {}
