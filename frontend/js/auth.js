// ---- Configuration ----
// Point this at your deployed Flask backend.
const API_BASE = "https://your-backend.onrender.com/api";

// ---- Token helpers ----
function setToken(token) {
  localStorage.setItem("fountain_token", token);
}

function getToken() {
  return localStorage.getItem("fountain_token");
}

function clearToken() {
  localStorage.removeItem("fountain_token");
}

function setCurrentUser(user) {
  localStorage.setItem("fountain_user", JSON.stringify(user));
}

function getCurrentUser() {
  const raw = localStorage.getItem("fountain_user");
  return raw ? JSON.parse(raw) : null;
}

function logout() {
  clearToken();
  localStorage.removeItem("fountain_user");
  window.location.href = "login.html";
}

// ---- Authenticated fetch wrapper ----
async function authFetch(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (response.status === 401) {
    // Token missing/expired/invalid — send the user back to login
    clearToken();
    localStorage.removeItem("fountain_user");
    window.location.href = "login.html";
    return null;
  }

  return response;
}

// ---- Page guard: call this at the top of any protected page ----
async function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = "login.html";
    return null;
  }

  const response = await authFetch("/auth/me");
  if (!response) return null;

  if (!response.ok) {
    clearToken();
    window.location.href = "login.html";
    return null;
  }

  const data = await response.json();
  setCurrentUser(data.user);
  return data.user;
}

// ---- Shared UI: show user name + logout in nav if elements exist ----
function renderAuthNav(user) {
  const slot = document.getElementById("authNavSlot");
  if (!slot || !user) return;
  slot.innerHTML = `
    <span class="text-white me-3 d-none d-md-inline">Hi, ${user.name.split(" ")[0]}</span>
    <button id="logoutBtn" class="btn btn-sm contact__btn text-white">Logout</button>
  `;
  document.getElementById("logoutBtn").addEventListener("click", logout);
}
