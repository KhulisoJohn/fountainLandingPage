(async () => {
  const user = await requireAuth();
  if (!user) return;
  renderAuthNav(user);

  const listEl = document.getElementById("prayersList");
  const formMessage = document.getElementById("formMessage");

  function renderStatus(status) {
    return `<span class="status-badge ${status}">${status}</span>`;
  }

  async function loadPrayers() {
    try {
      const response = await authFetch("/prayers/mine");
      if (!response) return;
      const data = await response.json();

      if (!response.ok) {
        listEl.innerHTML = `<p class="text-danger">${data.error || "Could not load your requests."}</p>`;
        return;
      }

      if (data.prayers.length === 0) {
        listEl.innerHTML = "<p>You haven't submitted any prayer requests yet.</p>";
        return;
      }

      listEl.innerHTML = data.prayers.map((p) => {
        const date = new Date(p.created_at).toLocaleDateString();
        return `
          <div class="card-item">
            <p class="mb-2">${p.request_text}</p>
            <p class="mb-0 text-muted small">${date} &nbsp; ${renderStatus(p.status)}</p>
          </div>
        `;
      }).join("");
    } catch (err) {
      listEl.innerHTML = `<p class="text-danger">Something went wrong loading your requests.</p>`;
    }
  }

  document.getElementById("prayerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    formMessage.textContent = "";
    formMessage.className = "auth-message";

    const requestText = document.getElementById("requestText").value.trim();
    if (!requestText) return;

    try {
      const response = await authFetch("/prayers", {
        method: "POST",
        body: JSON.stringify({ request_text: requestText }),
      });
      if (!response) return;
      const data = await response.json();

      if (!response.ok) {
        formMessage.textContent = data.error || "Could not submit your request.";
        formMessage.classList.add("error");
        return;
      }

      formMessage.textContent = data.message;
      formMessage.classList.add("success");
      document.getElementById("prayerForm").reset();
      loadPrayers();
    } catch (err) {
      formMessage.textContent = "Something went wrong. Please try again.";
      formMessage.classList.add("error");
    }
  });

  loadPrayers();
})();
