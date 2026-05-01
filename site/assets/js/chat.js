/* iPhloat chat widget — persistent "Ask iPhloat" floating button + side panel.
   Calls /api/chat/turn on the iphloat back-end, displays responses with
   inline citations. Conversation history is per-session (in-memory). */

(function () {
  "use strict";

  const PRIOR_TURNS_LIMIT = 12; // keep the last N turns
  const priorTurns = [];

  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function linkifyCitations(text, citations) {
    // Replace [N] with a clickable citation chip
    return escapeHtml(text).replace(/\[(\d+)\]/g, (m, n) => {
      const idx = parseInt(n, 10) - 1;
      const c = citations[idx];
      if (!c) return m;
      const target = c.source_path && c.source_path !== "/__brand__" ? c.source_path : "/about";
      const title = escapeHtml(`${c.heading_anchor} — ${c.snippet}`);
      return `<a class="cite" href="${escapeHtml(target)}" title="${title}" target="_self">[${n}]</a>`;
    });
  }

  // ── Build the widget DOM ───────────────────────────────────────────────

  const button = el("button", "iphloat-chat-button");
  button.setAttribute("aria-label", "Ask iPhloat");
  button.innerHTML = `
    <span class="ic" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </span>
    <span class="lbl">Ask iPhloat</span>
  `;

  const panel = el("aside", "iphloat-chat-panel");
  panel.setAttribute("aria-hidden", "true");
  panel.innerHTML = `
    <header class="ic-header">
      <div class="ic-title">Ask iPhloat</div>
      <button class="ic-close" aria-label="Close">&times;</button>
    </header>
    <div class="ic-messages" role="log" aria-live="polite"></div>
    <form class="ic-form">
      <input type="text" class="ic-input" placeholder="Will it fit my iPhone 17 Pro Max?" autocomplete="off" required>
      <button type="submit" class="ic-send" aria-label="Send">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </form>
  `;

  // ── Behavior ───────────────────────────────────────────────────────────

  function open() {
    panel.classList.add("open");
    panel.setAttribute("aria-hidden", "false");
    button.classList.add("hidden");
    setTimeout(() => panel.querySelector(".ic-input").focus(), 50);
    if (!panel.dataset.greeted) {
      addAssistantMessage(
        "I'm the Weaver for iPhloat. Ask me anything about the case, the insurance, or how it works.",
        []
      );
      panel.dataset.greeted = "1";
    }
  }
  function close() {
    panel.classList.remove("open");
    panel.setAttribute("aria-hidden", "true");
    button.classList.remove("hidden");
  }

  function addUserMessage(text) {
    const msgs = panel.querySelector(".ic-messages");
    const m = el("div", "ic-msg ic-msg-user", `<div class="ic-bubble">${escapeHtml(text)}</div>`);
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addAssistantMessage(text, citations) {
    const msgs = panel.querySelector(".ic-messages");
    const html = linkifyCitations(text, citations || []);
    const m = el("div", "ic-msg ic-msg-weaver", `<div class="ic-bubble">${html}</div>`);
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function addTyping() {
    const msgs = panel.querySelector(".ic-messages");
    const m = el("div", "ic-msg ic-msg-weaver ic-typing",
      `<div class="ic-bubble"><span class="ic-dot"></span><span class="ic-dot"></span><span class="ic-dot"></span></div>`);
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
    return m;
  }

  function addError(text) {
    const msgs = panel.querySelector(".ic-messages");
    const m = el("div", "ic-msg ic-msg-error", `<div class="ic-bubble">${escapeHtml(text)}</div>`);
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }

  async function sendTurn(userInput) {
    addUserMessage(userInput);
    const typing = addTyping();
    const sendBtn = panel.querySelector(".ic-send");
    const inputEl = panel.querySelector(".ic-input");
    sendBtn.disabled = true;
    inputEl.disabled = true;
    try {
      const r = await fetch("/api/chat/turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userInput, prior_turns: priorTurns }),
      });
      typing.remove();
      if (r.status === 401) {
        addError("You've been signed out. Reload the page to sign in again.");
        return;
      }
      if (r.status === 503) {
        addError("The chat isn't quite ready yet. Try again in a moment.");
        return;
      }
      if (!r.ok) {
        addError(`Something went wrong (HTTP ${r.status}). Try again?`);
        return;
      }
      const data = await r.json();
      addAssistantMessage(data.text, data.citations || []);
      priorTurns.push({ role: "user", content: userInput });
      priorTurns.push({ role: "assistant", content: data.text });
      while (priorTurns.length > PRIOR_TURNS_LIMIT) priorTurns.shift();
    } catch (e) {
      typing.remove();
      addError("I couldn't reach the loom. Check your connection and try again.");
    } finally {
      sendBtn.disabled = false;
      inputEl.disabled = false;
      inputEl.focus();
    }
  }

  // ── Wire events ───────────────────────────────────────────────────────

  button.addEventListener("click", open);
  panel.querySelector(".ic-close").addEventListener("click", close);
  panel.querySelector(".ic-form").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const inp = panel.querySelector(".ic-input");
    const text = inp.value.trim();
    if (!text) return;
    inp.value = "";
    sendTurn(text);
  });
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && panel.classList.contains("open")) close();
  });

  // ── Mount on load ────────────────────────────────────────────────────

  function mount() {
    document.body.appendChild(button);
    document.body.appendChild(panel);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
