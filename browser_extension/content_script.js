/**
 * Exocortex Cognitive Telemetry - Content Script.
 * Détecte les en-têtes H1 de la page courante et capture au fil de l'eau
 * les échanges avec les LLMs (Gemini Web, Claude.ai, ChatGPT).
 * Depuis v0.5.2, injecté uniquement sur ces trois plateformes (manifest) : aucun autre site
 * n'est observé ; les onglets ordinaires ne remontent que leur URL et leur titre.
 */

(function () {
  "use strict";

  const hostname = window.location.hostname.toLowerCase();
  const url = window.location.href;

  // 1. Détection de l'en-tête H1 pour enrichir ocr_snippet
  try {
    const h1El = document.querySelector("h1");
    if (h1El && h1El.innerText.trim()) {
      chrome.runtime.sendMessage({
        action: "ACTIVE_TAB_HEADING",
        h1: h1El.innerText.trim().slice(0, 200),
      });
    }
  } catch (e) {}

  // 2. Détection de plateforme IA
  let platform = null;
  if (hostname.includes("gemini.google.com")) {
    platform = "gemini";
  } else if (hostname.includes("claude.ai")) {
    platform = "claude";
  } else if (hostname.includes("chatgpt.com") || hostname.includes("openai.com")) {
    platform = "chatgpt";
  }

  if (!platform) {
    return; // Page standard, rien d'autre à faire
  }

  /**
   * Extrait un identifiant de session stable depuis l'URL courante.
   */
  function extractSessionId() {
    const path = window.location.pathname;
    let match = null;

    if (platform === "gemini") {
      match = path.match(/app\/([a-zA-Z0-9_-]+)/);
    } else if (platform === "claude") {
      match = path.match(/chat\/([a-zA-Z0-9_-]+)/);
    } else if (platform === "chatgpt") {
      match = path.match(/c\/([a-zA-Z0-9_-]+)/);
    }

    if (match && match[1]) {
      return `${platform}_${match[1]}`;
    }

    // Fallback : slug basé sur le chemin ou date
    const cleanPath = path.replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 32);
    return `${platform}_live_${cleanPath || "session"}`;
  }

  // Cache des derniers prompts envoyés pour éviter le spam
  const sentTurnHashes = new Set();

  function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return hash;
  }

  /**
   * Scanne le DOM pour trouver les paires (User Prompt, AI Response).
   */
  function inspectChatTurns() {
    const sessionId = extractSessionId();
    let turns = [];

    if (platform === "gemini") {
      const userQueries = document.querySelectorAll(".user-query, user-query-content, .query-text");
      const modelResponses = document.querySelectorAll("model-response, .response-content, message-content");

      const count = Math.min(userQueries.length, modelResponses.length);
      for (let i = 0; i < count; i++) {
        const uText = userQueries[i].innerText.trim();
        const aText = modelResponses[i].innerText.trim();
        if (uText && aText) {
          turns.push({ user_prompt: uText, ai_response: aText });
        }
      }
    } else if (platform === "claude") {
      const userNodes = document.querySelectorAll("[data-testid='user-message'], .font-user-message");
      const claudeNodes = document.querySelectorAll(".font-claude-message, .standard-markdown");

      const count = Math.min(userNodes.length, claudeNodes.length);
      for (let i = 0; i < count; i++) {
        const uText = userNodes[i].innerText.trim();
        const aText = claudeNodes[i].innerText.trim();
        if (uText && aText) {
          turns.push({ user_prompt: uText, ai_response: aText });
        }
      }
    } else if (platform === "chatgpt") {
      const userNodes = document.querySelectorAll("[data-message-author-role='user']");
      const assistantNodes = document.querySelectorAll("[data-message-author-role='assistant']");

      const count = Math.min(userNodes.length, assistantNodes.length);
      for (let i = 0; i < count; i++) {
        const uText = userNodes[i].innerText.trim();
        const aText = assistantNodes[i].innerText.trim();
        if (uText && aText) {
          turns.push({ user_prompt: uText, ai_response: aText });
        }
      }
    }

    for (const turn of turns) {
      const key = `${sessionId}_${simpleHash(turn.user_prompt)}_${simpleHash(turn.ai_response)}`;
      if (!sentTurnHashes.has(key)) {
        sentTurnHashes.add(key);
        chrome.runtime.sendMessage({
          action: "NEW_CHAT_TURN",
          payload: {
            platform: platform,
            session_id: sessionId,
            user_prompt: turn.user_prompt,
            ai_response: turn.ai_response,
            url: window.location.href,
          },
        });
      }
    }
  }

  // MutationObserver debouncé pour suivre l'arrivée de nouveaux messages
  let debounceTimer = null;
  const observer = new MutationObserver(() => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(inspectChatTurns, 2000);
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });

  // Premier passage au chargement de la page
  setTimeout(inspectChatTurns, 2500);
})();

