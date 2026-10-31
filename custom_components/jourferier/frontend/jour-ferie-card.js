/* Carte Lovelace native « Jours fériés » — intégration jourferier */
const CARD_TAG = "jour-ferie-card";
const DEFAULT_TITLE = "Jours fériés 🎉";
const NO_HOLIDAY = ["aucun", "none", "unknown", "unavailable", ""];

class JourFerieCard extends HTMLElement {
  static getConfigForm() {
    return {
      schema: [
        { name: "entity", required: true, selector: { entity: { filter: { domain: "sensor" } } } },
        { name: "title", selector: { text: {} } },
      ],
      computeLabel: (s) => ({ entity: "Capteur jour férié", title: "Titre" }[s.name] || s.name),
    };
  }

  static getStubConfig(hass) {
    const ent = hass && hass.states["sensor.jour_ferie"] ? "sensor.jour_ferie"
      : Object.keys((hass && hass.states) || {}).find((e) => e.startsWith("sensor.jour_ferie")) || "sensor.jour_ferie";
    return { entity: ent, title: DEFAULT_TITLE };
  }

  setConfig(config) {
    if (!config || !config.entity) throw new Error("Indique une entité (ex. sensor.jour_ferie)");
    this._config = { title: DEFAULT_TITLE, ...config };
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this._render();
  }

  set hass(hass) {
    const st = hass.states[this._config.entity];
    const key = st ? st.last_updated + st.state : "none";
    this._hass = hass;
    if (key === this._key) return;
    this._key = key;
    this._render();
  }

  getCardSize() { return 2; }

  static _esc(v) {
    return String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  _render() {
    if (!this.shadowRoot || !this._config) return;
    const esc = JourFerieCard._esc;
    const st = this._hass ? this._hass.states[this._config.entity] : undefined;
    let body;
    if (!st) {
      body = `<p class="warn">Entité introuvable : ${esc(this._config.entity)}</p>`;
    } else {
      const a = st.attributes || {};
      const name = a.holiday_name || st.state;
      const today = NO_HOLIDAY.includes(String(name).toLowerCase())
        ? "Aujourd'hui, pas de jour férié."
        : `Aujourd'hui, c'est <b>${esc(name)}</b>.`;
      let next = "";
      const n = Number(a.days_until);
      if (a.next_holiday && a.days_until !== undefined && a.days_until !== null && !Number.isNaN(n)) {
        next = `<p>Le prochain jour férié est <b>${esc(a.next_holiday)}</b> dans <b>${n} ${Math.abs(n) <= 1 ? "jour" : "jours"}</b>.</p>`;
      }
      body = `<p>${today}</p>${next}`;
    }
    const title = this._config.title ? `<div class="title">${esc(this._config.title)}</div>` : "";
    this.shadowRoot.innerHTML = `
      <style>
        ha-card { padding: 16px; }
        .title { font-size: 1.3em; font-weight: 500; margin-bottom: 8px; color: var(--primary-text-color); }
        p { margin: 4px 0; color: var(--primary-text-color); line-height: 1.5; }
        .warn { color: var(--error-color); }
      </style>
      <ha-card>${title}${body}</ha-card>`;
  }
}

if (!customElements.get(CARD_TAG)) customElements.define(CARD_TAG, JourFerieCard);
window.customCards = window.customCards || [];
if (!window.customCards.some((c) => c.type === CARD_TAG)) {
  window.customCards.push({
    type: CARD_TAG,
    name: "Jours fériés",
    description: "Affiche le jour férié du jour et le prochain jour férié (intégration Jour Férié).",
    preview: true,
    documentationURL: "https://github.com/XAV59213/jourferier",
  });
}
