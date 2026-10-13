"use strict";

/* Browser demonstration of the existing agents/workers.py rule conditions.
 * Thresholds are generic prototype constants, not clinical reference intervals.
 */
function validateDemoInput(input) {
  for (const key of ["task_id", "target_identifier"]) {
    if (typeof input[key] !== "string" || !/^[A-Za-z0-9_-]{1,64}$/.test(input[key])) {
      throw new Error("Use synthetic IDs of 1–64 letters, numbers, underscores or hyphens.");
    }
  }
  for (const key of ["primary_metric", "secondary_metric"]) {
    if (typeof input[key] !== "number" || !Number.isFinite(input[key]) || Math.abs(input[key]) > 1e9) {
      throw new Error("Both metrics must be finite numeric values within ±1,000,000,000.");
    }
  }
  if (typeof input.status_descriptor !== "string" || input.status_descriptor.length > 256) {
    throw new Error("Invalid status descriptor.");
  }
  return input;
}

function evaluateDemo(raw) {
  const input = validateDemoInput(raw);
  const alerts = [];
  if (input.primary_metric > 25) {
    alerts.push({origin_worker: "InvariantQCWorker", urgency: "ELEVATED_RISK",
      summary: "Primary metric exceeds demonstration threshold (25)"});
  }
  if (input.is_critical_flag || input.secondary_metric > 12) {
    alerts.push({origin_worker: "SafetyEscalationWorker",
      urgency: input.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      summary: "Simulated flag or secondary threshold (12) triggered"});
  }
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"]
    .some(word => input.status_descriptor.toUpperCase().includes(word))) {
    alerts.push({origin_worker: "ProtocolConformanceWorker", urgency: "ELEVATED_RISK",
      summary: "Status descriptor contains an anomaly keyword"});
  }
  const critical = alerts.some(a => a.urgency === "CRITICAL_STAT_PANIC");
  return {
    mode: "LOCAL_DEMONSTRATION_ONLY",
    task_id: input.task_id,
    target_identifier: input.target_identifier,
    overall_urgency: critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE",
    integrity_status: critical ? "RECALIBRATION_REQUIRED" : alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length,
    critical_alerts_count: alerts.filter(a => a.urgency === "CRITICAL_STAT_PANIC").length,
    alerts,
    clinical_validity: "NOT_VALIDATED_FOR_CLINICAL_USE",
    audit_signature: null
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {validateDemoInput, evaluateDemo};
}

if (typeof document !== "undefined") {
  const form = document.getElementById("audit-form");
  const output = document.getElementById("output");
  const error = document.getElementById("error");
  const download = document.getElementById("download");
  let lastResult = null;
  let runs = 0;

  form.addEventListener("submit", event => {
    event.preventDefault();
    error.textContent = "";
    try {
      const input = {
        task_id: document.getElementById("task-id").value.trim(),
        target_identifier: document.getElementById("target-id").value.trim(),
        primary_metric: Number(document.getElementById("primary").value),
        secondary_metric: Number(document.getElementById("secondary").value),
        status_descriptor: document.getElementById("descriptor").value,
        is_critical_flag: document.getElementById("critical").checked
      };
      if (document.getElementById("primary").value.trim() === "" ||
          document.getElementById("secondary").value.trim() === "") {
        throw new Error("Enter both numeric metrics.");
      }
      lastResult = evaluateDemo(input);
      output.textContent = JSON.stringify(lastResult, null, 2);
      document.getElementById("runs").textContent = String(++runs);
      download.disabled = false;
    } catch (exception) {
      error.textContent = exception.message;
      output.textContent = "No result generated. Correct the input and try again.";
      lastResult = null;
      download.disabled = true;
    }
  });

  download.addEventListener("click", () => {
    if (!lastResult) return;
    const objectURL = URL.createObjectURL(new Blob([JSON.stringify(lastResult, null, 2)], {type:"application/json"}));
    const anchor = document.createElement("a");
    anchor.href = objectURL;
    anchor.download = "rule-demonstration.json";
    anchor.click();
    URL.revokeObjectURL(objectURL);
  });
}
