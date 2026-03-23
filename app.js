const runBtn = document.getElementById("runBtn");
const statusEl = document.getElementById("status");
const summaryEl = document.getElementById("summary");

function card(label, value) {
  return `<div class="card metric"><div class="metric-label">${label}</div><div class="metric-value">${value}</div></div>`;
}

async function runSimulation() {
  const steps = document.getElementById("steps").value;
  const twins = document.getElementById("twins").value;
  const policy = document.getElementById("policy").value;

  statusEl.textContent = "Running...";
  runBtn.disabled = true;

  try {
    const res = await fetch(`/api/simulate?steps=${encodeURIComponent(steps)}&twins=${encodeURIComponent(twins)}&policy=${encodeURIComponent(policy)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const routes = Object.entries(data.route_counts || {})
      .map(([k, v]) => `<li><strong>${k}</strong>: ${v}</li>`)
      .join("");

    const rows = (data.recent_records || []).map(r => `
      <tr>
        <td>${r.step_id}</td>
        <td>${r.twin_id}</td>
        <td>${r.route}</td>
        <td>${r.exec_ms}</td>
        <td>${r.objective_value}</td>
        <td>${r.confidence}</td>
      </tr>
    `).join("");

    summaryEl.innerHTML = `
      <div class="metrics">
        ${card("Records", data.records ?? "—")}
        ${card("Mean objective", data.mean_objective ?? "—")}
        ${card("Mean exec ms", data.mean_exec_ms ?? "—")}
        ${card("Policy", data.policy ?? "—")}
      </div>

      <div class="card">
        <h2>Route distribution</h2>
        <ul>${routes}</ul>
      </div>

      <div class="card">
        <h2>Recent records</h2>
        <table>
          <thead>
            <tr>
              <th>Step</th>
              <th>Twin</th>
              <th>Route</th>
              <th>Exec ms</th>
              <th>Objective</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;

    statusEl.textContent = "Completed.";
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  } finally {
    runBtn.disabled = false;
  }
}

runBtn.addEventListener("click", runSimulation);
