const DEFAULT_API_URL = "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 15000;

async function loadSettings() {
  const { api_url, auth_token, user_email } = await chrome.storage.local.get(["api_url", "auth_token", "user_email"]);
  document.getElementById("api_url").value = api_url || DEFAULT_API_URL;
  document.getElementById("email").value = user_email || "";

  const authStatus = document.getElementById("auth-status");
  const logoutBtn = document.getElementById("logout");
  if (auth_token) {
    authStatus.textContent = `Logged in as ${user_email || "unknown"}`;
    authStatus.className = "hint logged-in";
    logoutBtn.style.display = "block";
  } else {
    authStatus.textContent = "Not logged in";
    authStatus.className = "hint logged-out";
    logoutBtn.style.display = "none";
  }
}

document.getElementById("save").addEventListener("click", async () => {
  const api_url = document.getElementById("api_url").value.trim() || DEFAULT_API_URL;
  await chrome.storage.local.set({ api_url });
  document.getElementById("status").textContent = "API URL saved.";
  setTimeout(() => { document.getElementById("status").textContent = ""; }, 2000);
});

document.getElementById("login").addEventListener("click", async () => {
  const api_url = document.getElementById("api_url").value.trim() || DEFAULT_API_URL;
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    document.getElementById("auth-status").textContent = "Enter email and password.";
    return;
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const res = await fetch(`${api_url}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Login failed." }));
      document.getElementById("auth-status").textContent = err.detail || "Login failed.";
      document.getElementById("auth-status").className = "hint logged-out";
      return;
    }

    const data = await res.json();
    await chrome.storage.local.set({
      auth_token: data.access_token,
      user_email: data.email,
    });
    document.getElementById("auth-status").textContent = `Logged in as ${data.email}`;
    document.getElementById("auth-status").className = "hint logged-in";
    document.getElementById("password").value = "";
    document.getElementById("logout").style.display = "block";
  } catch (err) {
    if (err.name === "AbortError") {
      document.getElementById("auth-status").textContent = "Request timed out. Check the API URL.";
    } else {
      document.getElementById("auth-status").textContent = "Network error. Check the API URL.";
    }
    document.getElementById("auth-status").className = "hint logged-out";
  }
});

document.getElementById("register").addEventListener("click", async () => {
  const api_url = document.getElementById("api_url").value.trim() || DEFAULT_API_URL;
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    document.getElementById("auth-status").textContent = "Enter email and password.";
    return;
  }

  if (password.length < 6) {
    document.getElementById("auth-status").textContent = "Password must be at least 6 characters.";
    return;
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const res = await fetch(`${api_url}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Registration failed." }));
      document.getElementById("auth-status").textContent = err.detail || "Registration failed.";
      document.getElementById("auth-status").className = "hint logged-out";
      return;
    }

    const data = await res.json();
    await chrome.storage.local.set({
      auth_token: data.access_token,
      user_email: data.email,
    });
    document.getElementById("auth-status").textContent = `Account created and logged in as ${data.email}`;
    document.getElementById("auth-status").className = "hint logged-in";
    document.getElementById("password").value = "";
    document.getElementById("logout").style.display = "block";
  } catch (err) {
    if (err.name === "AbortError") {
      document.getElementById("auth-status").textContent = "Request timed out. Check the API URL.";
    } else {
      document.getElementById("auth-status").textContent = "Network error. Check the API URL.";
    }
    document.getElementById("auth-status").className = "hint logged-out";
  }
});

document.getElementById("logout").addEventListener("click", async () => {
  await chrome.storage.local.remove(["auth_token", "user_email"]);
  document.getElementById("auth-status").textContent = "Logged out.";
  document.getElementById("auth-status").className = "hint logged-out";
  document.getElementById("logout").style.display = "none";
});

loadSettings();
