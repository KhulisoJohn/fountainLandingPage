(async () => {
  const user = await requireAuth();
  if (!user) return;
  renderAuthNav(user);

  const listEl = document.getElementById("sermonsList");

  try {
    const response = await authFetch("/sermons");
    if (!response) return;
    const data = await response.json();

    if (!response.ok) {
      listEl.innerHTML = `<p class="text-danger">${data.error || "Could not load sermons."}</p>`;
      return;
    }

    if (data.sermons.length === 0) {
      listEl.innerHTML = "<p>No sermons posted yet. Check back soon.</p>";
      return;
    }

    listEl.innerHTML = data.sermons.map((sermon) => {
      const date = new Date(sermon.sermon_date).toLocaleDateString();
      return `
        <div class="card-item">
          <h5 class="fw-bold">${sermon.title}</h5>
          ${sermon.speaker ? `<p class="mb-1"><strong>Speaker:</strong> ${sermon.speaker}</p>` : ""}
          <p class="mb-1 text-muted small">${date}</p>
          ${sermon.description ? `<p class="mb-2">${sermon.description}</p>` : ""}
          ${sermon.video_url ? `<a href="${sermon.video_url}" target="_blank" class="contact__btn btn text-white btn-sm">Watch</a>` : ""}
        </div>
      `;
    }).join("");
  } catch (err) {
    listEl.innerHTML = `<p class="text-danger">Something went wrong loading sermons.</p>`;
  }
})();
