const DEFAULT_API_URL = "http://localhost:8000";

async function loadSettings() {
  const { api_url, auth_token, user_email } = await chrome.storage.sync.get(["api_url", "auth_token", "user_email"]);
  document.getElementById("api_url").value = api_url || DEFAULT_API_URL;
  document.getElementById("email").value = user_email || "";

  const authStatus = document.getElementById("auth-status");
  if (auth_token) {
    authStatus.textContent = `Logged in as ${user_email || "unknown"}`;
    authStatus.className = "hint logged-in";
  } else {
    authStatus.textContent = "Not logged in";
    authStatus.className = "hint logged-out";
  }
}

document.getElementById("save").addEventListener("click", async () => {
  const api_url = document.getElementById("api_url").value.trim() || DEFAULT_API_URL;
  await chrome.storage.sync.set({ api_url });
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
    const res = await fetch(`${api_url}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Login failed." }));
      document.getElementById("auth-status").textContent = err.detail || "Login failed.";
      document.getElementById("auth-status").className = "hint logged-out";
      return;
    }

    const data = await res.json();
    await chrome.storage.sync.set({
      auth_token: data.access_token,
      user_email: data.email,
      user_name: data.name,
    });
    document.getElementById("auth-status").textContent = `Logged in as ${data.email}`;
    document.getElementById("auth-status").className = "hint logged-in";
    document.getElementById("password").value = "";
  } catch {
    document.getElementById("auth-status").textContent = "Network error. Check the API URL.";
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
    const res = await fetch(`${api_url}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Registration failed." }));
      document.getElementById("auth-status").textContent = err.detail || "Registration failed.";
      document.getElementById("auth-status").className = "hint logged-out";
      return;
    }

    const data = await res.json();
    await chrome.storage.sync.set({
      auth_token: data.access_token,
      user_email: data.email,
      user_name: data.name,
    });
    document.getElementById("auth-status").textContent = `Account created and logged in as ${data.email}`;
    document.getElementById("auth-status").className = "hint logged-in";
    document.getElementById("password").value = "";
  } catch {
    document.getElementById("auth-status").textContent = "Network error. Check the API URL.";
    document.getElementById("auth-status").className = "hint logged-out";
  }
});

loadSettings();
