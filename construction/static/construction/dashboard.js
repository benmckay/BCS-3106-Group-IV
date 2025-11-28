const endpoints = {
  stats: "/api/dashboard-stats/",
  charts: "/api/dashboard-charts/",
  export: "/api/export-dashboard/",
  materials: "/api/materials/top-by-cost/",
};
const refreshInterval = 300000;
const CACHE_KEY = "bidii_dashboard_cache_v1";
let refreshTimer;
let toastTimer;
let isRefreshing = false;
const STATS_TIMEOUT = 3000;
const CHARTS_TIMEOUT = 10000;
const MATERIALS_TIMEOUT = 6000;
const MATERIALS_LIMIT = 6;
const REFRESH_DEBOUNCE = 800;

function nowIso() {
  return new Date().toISOString();
}

function formatNumber(value) {
  if (value === undefined || value === null || Number.isNaN(Number(value))) {
    return "0";
  }
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(
    Number(value)
  );
}

function formatCurrency(value) {
  if (value === undefined || value === null || Number.isNaN(Number(value))) {
    return "$0";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

function batchUpdate(fn) {
  if ("requestAnimationFrame" in window) {
    requestAnimationFrame(fn);
  } else {
    setTimeout(fn, 0);
  }
}

function updateStats(data) {
  batchUpdate(() => {
    document.querySelectorAll(".stat-card").forEach((card) => {
      const key = card.dataset.key;
      if (!(key in data)) return;
      const prefix = card.dataset.prefix || "";
      const valueEl = card.querySelector(".value");
      valueEl.textContent =
        prefix === "$" ? formatCurrency(data[key]) : formatNumber(data[key]);
    });
    document.querySelectorAll("[data-secondary]").forEach((node) => {
      const key = node.dataset.secondary;
      if (key in data) node.textContent = formatNumber(data[key]);
    });

    const availability = document.getElementById("worker-availability");
    if (availability) {
      const pct = data.worker_availability ?? 0;
      availability.textContent = `${(Number(pct) || 0).toFixed(1)}%`;
    }

    const breakdown = document.getElementById("worker-breakdown");
    if (breakdown) {
      const counts = data.worker_counts || {};
      const total = counts.total || 0;
      const available = counts.available || 0;
      breakdown.textContent = `${available} of ${total} workers available`;
    }

    const material = document.getElementById("material-spend");
    if (material) material.textContent = formatCurrency(data.material_spend);

    const duration = document.getElementById("avg-duration");
    if (duration) {
      const days = data.average_job_duration ?? 0;
      duration.textContent = `${days} days`;
    }

    const satisfaction = document.getElementById("customer-satisfaction");
    if (satisfaction) {
      const score = data.customer_satisfaction ?? 0;
      satisfaction.textContent = `${(Number(score) || 0).toFixed(1)}%`;
    }

    const timestamp = data.last_updated
      ? new Date(data.last_updated)
      : new Date();
    document.getElementById("last-refresh").textContent =
      timestamp.toLocaleString();

    updateActivity(data.recent_activity || []);
  });
}

function updateActivity(items) {
  batchUpdate(() => {
    const feed = document.getElementById("activity-feed");
    feed.innerHTML = "";
    if (!items.length) {
      const li = document.createElement("li");
      li.textContent = "No recent updates";
      feed.appendChild(li);
      return;
    }
    items.slice(0, 8).forEach((item) => {
      const li = document.createElement("li");
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = (item.type || "Update").toUpperCase();
      const wrapper = document.createElement("div");
      const title = document.createElement("p");
      title.textContent = item.title || "N/A";
      const meta = document.createElement("small");
      const status = item.status ? `${item.status}` : "";
      const time = item.timestamp
        ? new Date(item.timestamp).toLocaleString()
        : "";
      meta.textContent = `${status}${status && time ? " · " : ""}${time}`;
      wrapper.appendChild(title);
      wrapper.appendChild(meta);
      li.appendChild(badge);
      li.appendChild(wrapper);
      feed.appendChild(li);
    });
  });
}

function renderCharts(charts) {
  if (!charts) return;
  batchUpdate(() => {
    Object.entries(charts).forEach(([key, chart]) => {
      let card =
        document.querySelector(`[data-chart="${key}"]`) ||
        document.querySelector(`[data-chart="${key.replace(/s$/i, "")}"]`) ||
        document.querySelector(`[data-chart="${key.replace(/_/g, "-")}"]`);
      if (!card) {
        const normalized = key
          .toLowerCase()
          .replace(/[\s-]+/g, "_")
          .replace(/s$/i, "");
        card = document.querySelector(`[data-chart="${normalized}"]`);
      }
      if (!card) return;

      const title = card.querySelector(".chart-title");
      if (title && chart.title) title.textContent = chart.title;

      const img = card.querySelector("img");
      let fallback = card.querySelector(".chart-fallback");
      if (!fallback) {
        fallback = document.createElement("div");
        fallback.className = "chart-fallback";
        card.appendChild(fallback);
      }

      if (chart.image) {
        fallback.style.display = "none";
        if (img) {
          img.style.display = "";
          img.src = `data:image/png;base64,${chart.image}`;
          if (img.decode) img.decode().catch(() => {});
        }
      } else {
        if (img) {
          img.removeAttribute("src");
          img.style.display = "none";
        }
        fallback.style.display = "flex";
        fallback.textContent = chart.empty_text || "No chart data available";
      }
    });
  });
}

function extractMaterials(payload) {
  if (!payload) return [];
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.results)) return payload.results;
  return [];
}

function renderTopMaterials(payload) {
  const list = document.getElementById("materials-list");
  const totalNode = document.getElementById("materials-sum");
  if (!list) return;
  const items = extractMaterials(payload);
  list.innerHTML = "";
  if (!items.length) {
    const empty = document.createElement("li");
    empty.className = "materials-empty";
    empty.textContent = "No material purchases recorded";
    list.appendChild(empty);
    if (totalNode) totalNode.textContent = "$0";
    return;
  }
  const qtyFormatter = new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 2,
  });
  let total = 0;
  items.slice(0, MATERIALS_LIMIT).forEach((item) => {
    const li = document.createElement("li");
    li.className = "materials-row";
    const name = document.createElement("span");
    name.className = "material-name";
    name.textContent = item.name || "Unnamed material";
    const meta = document.createElement("span");
    meta.className = "material-meta";
    if (item.quantity !== undefined && item.quantity !== null) {
      const numeric = Number(item.quantity);
      if (!Number.isNaN(numeric)) {
        const qtyText = qtyFormatter.format(numeric);
        const unitText = item.unit ? ` ${item.unit}` : "";
        meta.textContent = `× ${qtyText}${unitText}`;
      } else {
        meta.textContent = "";
      }
    } else {
      meta.textContent = "";
    }
    const cost = document.createElement("span");
    cost.className = "material-cost";
    cost.textContent = formatCurrency(item.total_cost);
    total += Number(item.total_cost || 0);
    li.appendChild(name);
    li.appendChild(meta);
    li.appendChild(cost);
    list.appendChild(li);
  });
  if (totalNode) totalNode.textContent = formatCurrency(total);
}

function fetchWithTimeout(url, options = {}, timeout = 5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  const cfg = Object.assign({}, options, {
    signal: controller.signal,
    credentials: "include",
  });
  return fetch(url, cfg).finally(() => clearTimeout(id));
}

function saveCache(patch) {
  try {
    const current = loadCache() || {};
    const merged = Object.assign({}, current, patch);
    const stamp = nowIso();
    if (patch && Object.prototype.hasOwnProperty.call(patch, "stats")) {
      merged.stats_timestamp =
        (patch.stats && patch.stats.last_updated) || stamp;
    }
    if (patch && Object.prototype.hasOwnProperty.call(patch, "charts")) {
      merged.charts_timestamp = stamp;
    }
    if (patch && Object.prototype.hasOwnProperty.call(patch, "materials")) {
      merged.materials_timestamp = stamp;
    }
    merged.fetched_at = stamp;
    localStorage.setItem(CACHE_KEY, JSON.stringify(merged));
  } catch (e) {}
}

function loadCache() {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

async function loadStats() {
  const cached = loadCache();
  if (cached && cached.stats) {
    const cachedTimestamp = cached.stats_timestamp || cached.fetched_at;
    updateStats(
      Object.assign({}, cached.stats, { last_updated: cachedTimestamp })
    );
  }
  try {
    const resp = await fetchWithTimeout(endpoints.stats, {}, STATS_TIMEOUT);
    if (!resp.ok) throw new Error("Failed to load stats");
    const data = await resp.json();
    updateStats(data);
    saveCache({ stats: data });
    return data;
  } catch (err) {
    if (!cached || !cached.stats) throw err;
    return cached.stats;
  }
}

async function loadTopMaterials() {
  const cached = loadCache();
  if (cached && cached.materials) {
    try {
      renderTopMaterials(cached.materials);
    } catch (e) {}
  }
  try {
    const resp = await fetchWithTimeout(
      `${endpoints.materials}?limit=${MATERIALS_LIMIT}`,
      {},
      MATERIALS_TIMEOUT
    );
    if (!resp.ok) throw new Error("Failed to load materials");
    const data = await resp.json();
    renderTopMaterials(data);
    saveCache({ materials: data });
    return data;
  } catch (err) {
    if (cached && cached.materials) {
      return cached.materials;
    }
    throw err;
  }
}

async function loadChartsDeferred() {
  const cached = loadCache();
  if (cached && cached.charts) {
    renderCharts(cached.charts);
  }
  const run = () =>
    fetchWithTimeout(endpoints.charts, {}, CHARTS_TIMEOUT)
      .then((resp) => {
        if (!resp.ok) throw new Error("Failed to load charts");
        return resp.json();
      })
      .then((data) => {
        renderCharts(data);
        saveCache({ charts: data });
      })
      .catch(() => {});
  if ("requestIdleCallback" in window) {
    requestIdleCallback(() => run(), { timeout: 2000 });
  } else {
    setTimeout(() => run(), 600);
  }
}

function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("visible");
  toast.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 3500);
}

function toggleLoading(state) {
  const overlay = document.getElementById("loading-overlay");
  if (!overlay) return;
  overlay.classList.toggle("hidden", !state);
}

async function refreshDashboard() {
  if (isRefreshing) return;
  isRefreshing = true;
  toggleLoading(true);
  try {
    await loadStats();
    try {
      await loadTopMaterials();
    } catch (materialsError) {
      renderTopMaterials([]);
    }
    loadChartsDeferred();
  } catch (error) {
    showToast(error.message || "Unable to load dashboard");
  } finally {
    toggleLoading(false);
    isRefreshing = false;
  }
}

function bindTabs() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.tab;
      document
        .querySelectorAll(".tab")
        .forEach((btn) => btn.classList.toggle("active", btn === tab));
      document
        .querySelectorAll(".tab-panel")
        .forEach((panel) =>
          panel.classList.toggle("active", panel.dataset.panel === target)
        );
    });
  });
}

function bindExports() {
  document.querySelectorAll("[data-format]").forEach((button) => {
    button.addEventListener("click", () => {
      const format = button.dataset.format;
      const url = `${endpoints.export}?format=${format}`;
      window.open(url, "_blank");
    });
  });
}

let lastRefresh = 0;
document.getElementById("refresh-btn").addEventListener("click", () => {
  const now = Date.now();
  if (now - lastRefresh < REFRESH_DEBOUNCE) return;
  lastRefresh = now;
  refreshDashboard();
  scheduleAutoRefresh();
});

function scheduleAutoRefresh() {
  clearInterval(refreshTimer);
  refreshTimer = setInterval(() => {
    refreshDashboard();
  }, refreshInterval);
}

bindTabs();
bindExports();
const initialCache = loadCache();
if (initialCache && initialCache.stats) {
  try {
    updateStats(
      Object.assign({}, initialCache.stats, {
        last_updated: initialCache.stats_timestamp || initialCache.fetched_at,
      })
    );
  } catch (e) {}
}
if (initialCache && initialCache.materials) {
  try {
    renderTopMaterials(initialCache.materials);
  } catch (e) {}
}
setTimeout(() => {
  refreshDashboard();
  scheduleAutoRefresh();
}, 80);
