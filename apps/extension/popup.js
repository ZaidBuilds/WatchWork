const DEFAULT_API_URL = "http://localhost:8000";

async function getApiUrl() {
  const { api_url } = await chrome.storage.sync.get("api_url");
  return api_url || DEFAULT_API_URL;
}

async function getAuthToken() {
  const { auth_token } = await chrome.storage.sync.get("auth_token");
  return auth_token || null;
}

document.getElementById("capture").addEventListener("click", async () => {
  const status = document.getElementById("status");
  const apiBase = await getApiUrl();
  const token = await getAuthToken();

  if (!token) {
    status.textContent = "Not logged in. Right-click the extension icon and open Options to log in.";
    return;
  }

  status.textContent = "Reading current tab...";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.url || !tab.url.includes("youtube.com/watch")) {
      status.textContent = "Open a YouTube video first.";
      return;
    }

    const [{ result }] = await chrome.scripting.executeScript({
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

    status.textContent = "Sending...";

    const response = await fetch(`${apiBase}/api/ingest/browser-capture`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(result),
    });

    if (response.ok) {
      status.textContent = "Captured. Open the dashboard to generate the plan.";
      return;
    }

    if (response.status === 401) {
      status.textContent = "Session expired. Please log in again via Options.";
      return;
    }

    const error = await response.json().catch(() => ({ detail: "Capture failed." }));
    status.textContent = error.detail || "Capture failed.";
  } catch (err) {
    status.textContent = "Network error. Check if the API server is running.";
  }
});
