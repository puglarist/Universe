import {
  getLatestState,
  initializeMemory,
  putRecord,
  saveSystemSnapshot,
} from './app/memory.js';

/**
 * Bootstraps the app by hydrating persisted state before initial render,
 * then wires autosave hooks for critical state transitions.
 */
export async function startUniverseApp({
  renderModuleUI,
  applyPersistedState,
  getRuntimeState,
  moduleBus,
}) {
  if (typeof renderModuleUI !== 'function') {
    throw new Error('startUniverseApp requires a renderModuleUI callback.');
  }

  await initializeMemory();

  const persistedState = await getLatestState();

  if (typeof applyPersistedState === 'function' && persistedState) {
    await applyPersistedState(persistedState);
  }

  await renderModuleUI();

  const recordTransition = async (eventType, payload) => {
    const runtimeState = typeof getRuntimeState === 'function' ? getRuntimeState() : undefined;
    await putRecord('system_events', {
      eventType,
      moduleId: runtimeState?.activeModule ?? payload?.moduleId ?? 'unknown',
      payload,
    });

    await saveSystemSnapshot({
      moduleId: runtimeState?.activeModule ?? payload?.moduleId ?? 'system',
      transition: eventType,
      state: runtimeState,
      signal: payload,
    });
  };

  if (moduleBus?.onModuleSwitch) {
    moduleBus.onModuleSwitch((nextModule) => {
      void recordTransition('module_switch', {
        moduleId: nextModule?.id ?? nextModule,
      });
    });
  }

  if (moduleBus?.onObserverUpdate) {
    moduleBus.onObserverUpdate((observerProfile) => {
      void putRecord('observer_profile', {
        id: observerProfile?.id ?? 'primary_observer',
        ...observerProfile,
      });

      void recordTransition('observer_update', {
        observerId: observerProfile?.id,
      });
    });
  }

  if (moduleBus?.onInteractionSignal) {
    moduleBus.onInteractionSignal((signal) => {
      void recordTransition('interaction_signal', signal);
    });
  }

  return {
    persistedState,
    recordTransition,
  };
}
