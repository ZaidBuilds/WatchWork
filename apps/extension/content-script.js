const BUTTON_ID = "action-engine-capture-button";
const DEFAULT_API_URL = "http://localhost:8000";

async function getApiUrl() {
  const { api_url } = await chrome.storage.sync.get("api_url");
  return api_url || DEFAULT_API_URL;
}

async function getAuthToken() {
  const { auth_token } = await chrome.storage.sync.get("auth_token");
  return auth_token || null;
}

function addCaptureButton() {
  if (document.getElementById(BUTTON_ID)) return;
  const actions = document.querySelector("#top-level-buttons-computed");
  if (!actions) return;

  const button = document.createElement("button");
  button.id = BUTTON_ID;
  button.textContent = "Action Engine";
  button.style.border = "0";
  button.style.borderRadius = "18px";
  button.style.background = "#2C1810";
  button.style.color = "#FAF7F2";
  button.style.cursor = "pointer";
  button.style.fontWeight = "700";
  button.style.marginLeft = "8px";
  button.style.padding = "8px 14px";
  button.title = "Send this video to Action Engine";
  button.addEventListener("click", async () => {
    const apiBase = await getApiUrl();
    const token = await getAuthToken();

    if (!token) {
      button.textContent = "Login required";
      window.setTimeout(() => { button.textContent = "Action Engine"; }, 3000);
      return;
    }

    const videoId = new URL(location.href).searchParams.get("v");
    const payload = {
      platform: "youtube",
      source_url: location.href,
      title: document.querySelector("h1 yt-formatted-string")?.textContent?.trim() || document.title,
      channel_name:
        document.querySelector("#owner #channel-name a")?.textContent?.trim() ||
        document.querySelector("ytd-channel-name a")?.textContent?.trim(),
      thumbnail_url: videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : null,
      captured_at: new Date().toISOString(),
    };

    try {
      const response = await fetch(`${apiBase}/api/ingest/browser-capture`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        button.textContent = "Captured";
      } else if (response.status === 401) {
        button.textContent = "Login required";
      } else {
        button.textContent = "Failed";
      }
    } catch {
      button.textContent = "Error";
    }

    window.setTimeout(() => {
      button.textContent = "Action Engine";
    }, 2000);
  });

  actions.appendChild(button);
}

let debounceTimer = null;
const observer = new MutationObserver(() => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(addCaptureButton, 300);
});
observer.observe(document.body, { childList: true, subtree: true });
addCaptureButton();
