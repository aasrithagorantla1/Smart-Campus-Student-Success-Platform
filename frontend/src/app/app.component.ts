import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div class="shell">
      <header class="topbar">
        <div>
          <h1>Smart Campus Student Success Platform</h1>
          <p>Academic, attendance, placement, and intervention monitoring</p>
        </div>
        <button class="primary">Login</button>
      </header>

      <main class="content">
        <section class="panel hero">
          <div>
            <span class="chip">Rules-based analytics</span>
            <h2>Overview</h2>
            <p>Staff can monitor student risk, findings, interventions, and score history in one view.</p>
          </div>
          <div class="stats">
            <div><strong>150</strong><span>Students</span></div>
            <div><strong>6</strong><span>Periods</span></div>
            <div><strong>3</strong><span>Departments</span></div>
          </div>
        </section>

        <section class="grid">
          <article class="panel">
            <h3>Academic risk list</h3>
            <ul>
              <li><span class="dot high"></span> 9 students high risk</li>
              <li><span class="dot medium"></span> 27 students medium risk</li>
              <li><span class="dot low"></span> 114 students low risk</li>
            </ul>
          </article>
          <article class="panel">
            <h3>Placement readiness</h3>
            <ul>
              <li>Strong academics, low placement readiness</li>
              <li>Skills-led candidates</li>
              <li>Placement readiness pending</li>
            </ul>
          </article>
          <article class="panel">
            <h3>Segments</h3>
            <ul>
              <li>Improving after intervention</li>
              <li>Declining attendance</li>
              <li>Consistently performing well</li>
            </ul>
          </article>
        </section>
      </main>
    </div>
  `,
  styles: [
    `
      :host { display:block; font-family: Inter, Arial, sans-serif; background: #f4f8fb; color: #13314b; }
      .shell { max-width: 1200px; margin: 0 auto; padding: 32px 20px 52px; }
      .topbar { display:flex; justify-content:space-between; align-items:center; background:#0d2238; color:#fff; border-radius: 18px; padding: 20px 24px; }
      .topbar h1 { margin:0; font-size: 1.7rem; }
      .topbar p { margin:4px 0 0; color:#cfeaf7; }
      .primary { background:#15b7b8; color:#fff; border:none; border-radius:10px; padding:12px 18px; font-weight:700; }
      .content { margin-top: 22px; }
      .panel { background: white; border: 1px solid #dfeaf2; border-radius: 18px; box-shadow: 0 10px 20px rgba(19,49,75,0.06); padding: 22px; }
      .hero { display:flex; justify-content:space-between; gap:12px; align-items:center; }
      .chip { display:inline-block; background:#dff7f5; color:#0e6d7d; border-radius: 999px; padding: 6px 10px; font-size: 0.75rem; font-weight:700; }
      .stats { display:flex; gap:18px; }
      .stats div { background:#f3fbfd; border-radius: 12px; min-width: 100px; padding: 16px; text-align:center; }
      .stats strong { display:block; font-size: 2rem; }
      .stats span { color: #4d6982; }
      .grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap:18px; margin-top: 18px; }
      .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px; }
      .dot.high { background:#d9534f; }
      .dot.medium { background:#f0ad4e; }
      .dot.low { background:#5bc0de; }
      ul { padding-left: 0; list-style:none; margin:0; }
      li { margin-bottom:10px; }
      @media (max-width: 720px) { .topbar, .hero { flex-direction: column; align-items:flex-start; } }
    `
  ]
})
export class AppComponent {}
