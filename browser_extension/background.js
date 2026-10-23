/**
 * Exocortex Cognitive Telemetry - Background Service Worker (Manifest V3).
 * Surveille les transitions d'onglets actifs et transmet les échanges IA
 * vers le récepteur local 127.0.0.1:8502.
 */

const RECEIVER_BASE_URL = "http://127.0.0.1:8502";

// Débounce pour éviter d'envoyer trop de requêtes lors d'un zapping rapide
let lastSentUrl = null;
let lastSentTime = 0;

/**
 * Transmet l'onglet actif au récepteur local.
 */
async function sendActiveTabTelemetry(tab) {
  if (!tab || !tab.url) return;

  const url = tab.url;
  // Ignorer les protocoles internes de navigation
  if (
    url.startsWith("chrome://") ||
    url.startsWith("chrome-extension://") ||
    url.startsWith("edge://") ||
    url.startsWith("about:") ||
    url.startsWith("brave://")
  ) {
    return;
  }

  const now = Date.now();
  if (url === lastSentUrl && now - lastSentTime < 3000) {
    return;
  }

  try {
    const domain = new URL(url).hostname;
    const payload = {
      url: url,
      title: tab.title || "",
      domain: domain,
      h1: "",
    };

    const res = await fetch(`${RECEIVER_BASE_URL}/telemetry/tab`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok || res.status === 204) {
      lastSentUrl = url;
      lastSentTime = now;
    }
  } catch (err) {
    // Le démon local n'est pas nécessairement démarré : silence radio
  }
}

/**
 * Transmet un tour de conversation IA (Gemini, Claude, ChatGPT) au récepteur local.
 */
async function sendChatTurnTelemetry(turnData) {
  try {
    await fetch(`${RECEIVER_BASE_URL}/telemetry/chat_turn`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(turnData),
    });
  } catch (err) {
    // Silence radio si récepteur éteint
  }
}

// Événement 1 : Changement d'onglet actif
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    await sendActiveTabTelemetry(tab);
  } catch (e) {}
});

// Événement 2 : Navigation ou rafraîchissement d'onglet
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.active) {
    await sendActiveTabTelemetry(tab);
  }
});

// Événement 3 : Messages reçus des Content Scripts (H1 ou tour de chat IA)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || !message.action) return false;

  if (message.action === "NEW_CHAT_TURN") {
    sendChatTurnTelemetry(message.payload);
    sendResponse({ status: "acknowledged" });
  } else if (message.action === "ACTIVE_TAB_HEADING") {
    if (sender.tab && sender.tab.active) {
      const payload = {
        url: sender.tab.url,
        title: sender.tab.title || "",
        h1: message.h1 || "",
        domain: new URL(sender.tab.url).hostname,
      };
      fetch(`${RECEIVER_BASE_URL}/telemetry/tab`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).catch(() => {});
    }
    sendResponse({ status: "acknowledged" });
  }
  return false;
});

