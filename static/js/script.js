const state = { resume: null, job_description: null };

const slots = document.querySelectorAll(".slot");
const scanBtn = document.getElementById("scan-btn");
const statusLine = document.getElementById("status-line");
const resultsSection = document.getElementById("results");

function setStatus(text, mode) {
  statusLine.textContent = text || "";
  statusLine.className = "status-line" + (mode ? " " + mode : "");
}

function bindSlot(slot) {
  const role = slot.dataset.role;
  const drop = slot.querySelector(".slot-drop");
  const input = slot.querySelector("input[type=file]");
  const filenameEl = slot.querySelector(".slot-filename");

  drop.addEventListener("click", () => input.click());

  input.addEventListener("change", () => {
    if (input.files[0]) handleFile(role, input.files[0], slot, filenameEl);
  });

  ["dragover", "dragenter"].forEach(evt =>
    drop.addEventListener(evt, e => {
      e.preventDefault();
      drop.classList.add("drag-over");
    })
  );
  ["dragleave", "dragend"].forEach(evt =>
    drop.addEventListener(evt, () => drop.classList.remove("drag-over"))
  );
  drop.addEventListener("drop", e => {
    e.preventDefault();
    drop.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file) handleFile(role, file, slot, filenameEl);
  });
}

function handleFile(role, file, slot, filenameEl) {
  const ok = /\.(pdf|docx|txt)$/i.test(file.name);
  if (!ok) {
    setStatus(`"${file.name}" isn't a supported type — use .pdf, .docx, or .txt`, "error");
    return;
  }
  state[role] = file;
  slot.classList.add("filled");
  filenameEl.textContent = file.name;
  setStatus("", null);
  updateScanButton();
}

function updateScanButton() {
  scanBtn.disabled = !(state.resume && state.job_description);
}

slots.forEach(bindSlot);

scanBtn.addEventListener("click", runScan);

async function runScan() {
  if (!(state.resume && state.job_description)) return;

  scanBtn.disabled = true;
  resultsSection.hidden = true;
  setStatus("Scanning documents…", "busy");

  const formData = new FormData();
  formData.append("resume", state.resume);
  formData.append("job_description", state.job_description);

  try {
    const res = await fetch("/api/analyze", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      setStatus(data.error || "Something went wrong during the scan.", "error");
      scanBtn.disabled = false;
      return;
    }

    setStatus("Scan complete.", null);
    renderResults(data);
  } catch (err) {
    setStatus("Couldn't reach the server. Is it running?", "error");
  } finally {
    scanBtn.disabled = false;
  }
}

function renderResults(data) {
  resultsSection.hidden = false;

  // gauge
  const circumference = 578; // 2 * PI * 92, matches CSS dasharray
  const offset = circumference - (circumference * Math.min(data.score, 100)) / 100;
  const gaugeFill = document.getElementById("gauge-fill");
  const gaugeNumber = document.getElementById("gauge-number");

  let color = "var(--rust)";
  let verdict = "Needs work — tailor your resume before applying.";
  if (data.score >= 70) {
    color = "var(--teal)";
    verdict = "Strong overlap — you're well aligned with this posting.";
  } else if (data.score >= 40) {
    color = "var(--amber)";
    verdict = "Partial overlap — worth adding a few missing keywords.";
  }

  gaugeFill.style.stroke = color;
  requestAnimationFrame(() => {
    gaugeFill.style.strokeDashoffset = offset;
  });

  animateNumber(gaugeNumber, data.score);

  document.getElementById("meta-cosine").textContent = `${data.skill_coverage.toFixed(1)}%`;
  document.getElementById("meta-coverage").textContent = `${data.keyword_coverage.toFixed(1)}%`;
  document.getElementById("meta-resume-words").textContent = data.resume_word_count.toLocaleString();
  document.getElementById("meta-job-words").textContent = data.job_word_count.toLocaleString();
  document.getElementById("meta-verdict").textContent = verdict;

  renderChips("chips-match", "count-match", data.common, "chip-match");
  renderChips("chips-missing", "count-missing", data.missing, "chip-missing");

  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function animateNumber(el, target) {
  const duration = 900;
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = (target * eased).toFixed(1);
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = target.toFixed(1);
  }
  requestAnimationFrame(tick);
}

function renderChips(containerId, countId, words, chipClass) {
  const container = document.getElementById(containerId);
  const countEl = document.getElementById(countId);
  container.innerHTML = "";
  countEl.textContent = `(${words.length})`;

  if (words.length === 0) {
    const empty = document.createElement("p");
    empty.style.color = "var(--text-low)";
    empty.style.fontFamily = "var(--mono)";
    empty.style.fontSize = "12.5px";
    empty.textContent = "— none —";
    container.appendChild(empty);
    return;
  }

  words.slice(0, 40).forEach((word, i) => {
    const chip = document.createElement("span");
    chip.className = `chip ${chipClass}`;
    chip.textContent = word;
    chip.style.animationDelay = `${i * 18}ms`;
    container.appendChild(chip);
  });
}
