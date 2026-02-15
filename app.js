const modules = ["codex", "counseling", "logistics", "dreamworld", "ai-terminal"];

const state = {
  power: "awake",
  mode: "idle",
  activeModule: "codex",
  observer: "ORBIT-01",
};

const ui = {
  timeSync: document.getElementById("time-sync"),
  observerId: document.getElementById("observer-id"),
  coreState: document.getElementById("core-state"),
  systemStatus: document.getElementById("system-status"),
  systemDot: document.getElementById("system-dot"),
  moduleTrack: document.getElementById("module-track"),
  moduleNodes: [...document.querySelectorAll(".module-node")],
  navItems: [...document.querySelectorAll(".nav-item")],
  panels: [...document.querySelectorAll(".module-panel")],
};

function titleCase(input) {
  return input
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function syncClock() {
  ui.timeSync.textContent = new Date().toLocaleTimeString([], { hour12: false });
}

function renderState() {
  ui.observerId.textContent = state.observer;
  ui.systemStatus.textContent = `System: ${titleCase(state.power)} · ${titleCase(state.mode)}`;
  ui.coreState.textContent = `${state.power} · ${state.mode === "active" ? titleCase(state.activeModule) : "idle"}`;
  ui.systemDot.style.background = state.power === "awake" ? "#84ff9c" : "#ffd37a";
  ui.systemDot.style.boxShadow = `0 0 12px ${state.power === "awake" ? "#84ff9c" : "#ffd37a"}`;

  [...ui.moduleNodes, ...ui.navItems].forEach((button) => {
    button.classList.toggle("active", button.dataset.module === state.activeModule);
    button.setAttribute("aria-pressed", String(button.dataset.module === state.activeModule));
  });
}

function activateModule(moduleName, source = "router") {
  if (!modules.includes(moduleName)) return;

  state.activeModule = moduleName;
  state.mode = "active";

  const panelIndex = modules.indexOf(moduleName);
  ui.moduleTrack.scrollTo({ left: ui.moduleTrack.clientWidth * panelIndex, behavior: source === "swipe" ? "auto" : "smooth" });
  renderState();
}

function setIdle() {
  state.mode = "idle";
  renderState();
}

function installRouter() {
  [...ui.moduleNodes, ...ui.navItems].forEach((button) => {
    button.addEventListener("click", () => activateModule(button.dataset.module));
  });

  ui.moduleTrack.addEventListener("scroll", () => {
    const index = Math.round(ui.moduleTrack.scrollLeft / ui.moduleTrack.clientWidth);
    const moduleName = modules[index];
    if (moduleName && moduleName !== state.activeModule) {
      activateModule(moduleName, "swipe");
    }
  });

  let idleTimeout;
  const queueIdle = () => {
    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(setIdle, 12000);
  };

  ["click", "touchstart", "scroll"].forEach((eventName) => {
    window.addEventListener(eventName, queueIdle, { passive: true });
  });

  queueIdle();
}

(function boot() {
  syncClock();
  setInterval(syncClock, 1000);
  installRouter();
  renderState();
})();
