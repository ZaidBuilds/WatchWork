const DEFAULT_API_URL = "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 15000;

async function getApiUrl() {
  const { api_url } = await chrome.storage.local.get("api_url");
  return api_url || DEFAULT_API_URL;
}

async function getAuthToken() {
  const { auth_token } = await chrome.storage.local.get("auth_token");
  return auth_token || null;
}

document.getElementById("capture").addEventListener("click", async () => {
  const status = document.getElementById("status");
  const button = document.getElementById("capture");
  const apiBase = await getApiUrl();
  const token = await getAuthToken();

  if (!token) {
    status.textContent = "Not logged in. Right-click the extension icon and open Options to log in.";
    status.className = "error";
    return;
  }

  button.disabled = true;
  button.textContent = "Sending...";
  status.textContent = "Reading current tab...";
  status.className = "";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.url || !tab.url.includes("youtube.com/watch")) {
      status.textContent = "Open a YouTube video first.";
      status.className = "error";
      button.disabled = false;
      button.textContent = "Send to WatchWork";
      return;
    }

    let result;
    try {
      const injectionResults = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          const title = document.querySelector("h1 yt-formatted-string")?.textContent?.trim() || document.title;
          const channelName =
            document.querySelector("#owner #channel-name a")?.textContent?.trim() ||
            document.querySelector("ytd-channel-name a")?.textContent?.trim();
          const thumbnailUrl = `https://img.youtube.com/vi/${new URL(location.href).searchParams.get("v")}/hqdefault.jpg`;
          return {
            platform: "youtube",
            source_url: location.href,
            title,
            channel_name: channelName,
            thumbnail_url: thumbnailUrl,
            captured_at: new Date().toISOString(),
          };
        },
      });
      if (!injectionResults || injectionResults.length === 0) {
        throw new Error("INJECTION_FAILED");
      }
      result = injectionResults[0].result;
    } catch {
      status.textContent = "Could not read video info. Refresh the page and try again.";
      status.className = "error";
      button.disabled = false;
      button.textContent = "Send to WatchWork";
      return;
    }

    status.textContent = "Sending to server...";

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const response = await fetch(`${apiBase}/api/ingest/browser-capture`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(result),
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      status.textContent = "Captured! Open the dashboard to generate your plan.";
      status.className = "success";
    } else if (response.status === 401) {
      status.textContent = "Session expired. Please log in again via Options.";
      status.className = "error";
    } else if (response.status === 429) {
      status.textContent = "Daily limit reached. Try again tomorrow.";
      status.className = "error";
    } else {
      const error = await response.json().catch(() => ({ detail: "Capture failed." }));
      status.textContent = error.detail || "Capture failed.";
      status.className = "error";
    }
  } catch (err) {
    if (err.name === "AbortError") {
      status.textContent = "Request timed out. Check if the API server is running.";
    } else {
      status.textContent = "Network error. Check if the API server is running.";
    }
    status.className = "error";
  } finally {
    button.disabled = false;
    button.textContent = "Send to WatchWork";
  }
});
