const memoryStore = {
  events: [],
  record(event) {
    this.events.push({ ...event });
  },
};

const signalSubscribers = new Map();

function onSignal(type, handler) {
  if (!signalSubscribers.has(type)) {
    signalSubscribers.set(type, new Set());
  }

  signalSubscribers.get(type).add(handler);

  return () => {
    const handlers = signalSubscribers.get(type);
    if (!handlers) return;

    handlers.delete(handler);
    if (handlers.size === 0) {
      signalSubscribers.delete(type);
    }
  };
}

function emitSignal(type, payload = {}) {
  const signal = {
    type,
    payload,
    at: Date.now(),
  };

  coreEngine.signals.push(signal);

  const handlers = signalSubscribers.get(type);
  if (handlers) {
    handlers.forEach((handler) => handler(signal));
  }

  return signal;
}

const coreEngine = {
  time: {
    monotonic: 0,
    wallClock: Date.now(),
    bootWallClock: Date.now(),
    lastTick: Date.now(),
  },
  observer: { id: "observer:primary" },
  state: "awake",
  activeModule: null,
  signals: [],
};

const HEARTBEAT_MS = 100;
const IDLE_TIMEOUT_MS = 2500;
let heartbeatTimer = null;
let lastInteractionAt = Date.now();

function transitionState(nextState) {
  if (coreEngine.state === nextState) return;

  const previous = coreEngine.state;
  coreEngine.state = nextState;

  memoryStore.record({
    event: "system.state.changed",
    previous,
    next: nextState,
    at: coreEngine.time.wallClock,
  });
}

function updateTime() {
  const now = Date.now();
  const delta = Math.max(0, now - coreEngine.time.lastTick);

  coreEngine.time.monotonic += delta;
  coreEngine.time.wallClock = coreEngine.time.bootWallClock + coreEngine.time.monotonic;
  coreEngine.time.lastTick = now;
}

function processSignal(signal) {
  switch (signal.type) {
    case "tap":
    case "swipe": {
      lastInteractionAt = coreEngine.time.wallClock;
      transitionState("active");
      memoryStore.record({
        event: `interaction.${signal.type}`,
        payload: signal.payload,
        observer: coreEngine.observer,
        at: coreEngine.time.wallClock,
      });
      break;
    }
    case "module-switch": {
      const previous = coreEngine.activeModule;
      coreEngine.activeModule = signal.payload?.module ?? null;
      lastInteractionAt = coreEngine.time.wallClock;
      transitionState("active");

      memoryStore.record({
        event: "system.module.changed",
        previous,
        next: coreEngine.activeModule,
        at: coreEngine.time.wallClock,
      });
      break;
    }
    default: {
      memoryStore.record({
        event: "signal.unknown",
        signal,
        at: coreEngine.time.wallClock,
      });
    }
  }
}

function processSignals() {
  while (coreEngine.signals.length > 0) {
    const signal = coreEngine.signals.shift();
    processSignal(signal);
  }
}

function updateStateFromActivity() {
  const idleFor = coreEngine.time.wallClock - lastInteractionAt;

  if (idleFor >= IDLE_TIMEOUT_MS) {
    transitionState("idle");
  } else if (coreEngine.state === "idle") {
    transitionState("awake");
  } else if (coreEngine.state === "active" && idleFor > HEARTBEAT_MS * 2) {
    transitionState("awake");
  }
}

function heartbeat() {
  updateTime();
  updateStateFromActivity();
  processSignals();

  memoryStore.record({
    event: "system.heartbeat",
    state: coreEngine.state,
    activeModule: coreEngine.activeModule,
    queueDepth: coreEngine.signals.length,
    time: { ...coreEngine.time },
    at: coreEngine.time.wallClock,
  });
}

function startCoreEngine() {
  if (heartbeatTimer) return;
  heartbeatTimer = setInterval(heartbeat, HEARTBEAT_MS);
}

function stopCoreEngine() {
  if (!heartbeatTimer) return;
  clearInterval(heartbeatTimer);
  heartbeatTimer = null;
}

const api = {
  coreEngine,
  memoryStore,
  emitSignal,
  onSignal,
  startCoreEngine,
  stopCoreEngine,
  heartbeat,
};

if (typeof module !== "undefined" && module.exports) {
  module.exports = api;
}

if (typeof window !== "undefined") {
  window.UniverseEngine = api;
}
