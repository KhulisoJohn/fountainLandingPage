(async () => {
  const user = await requireAuth();
  if (!user) return;
  renderAuthNav(user);

  const listEl = document.getElementById("eventsList");

  try {
    const response = await authFetch("/events");
    if (!response) return;
    const data = await response.json();

    if (!response.ok) {
      listEl.innerHTML = `<p class="text-danger">${data.error || "Could not load events."}</p>`;
      return;
    }

    if (data.events.length === 0) {
      listEl.innerHTML = "<p>No upcoming events at the moment. Check back soon.</p>";
      return;
    }

    listEl.innerHTML = data.events.map((event) => {
      const date = new Date(event.event_date);
      const formatted = date.toLocaleDateString(undefined, {
        weekday: "long", year: "numeric", month: "long", day: "numeric",
      });
      return `
        <div class="card-item">
          <h5 class="fw-bold">${event.title}</h5>
          <p class="mb-1"><strong>Date:</strong> ${formatted}</p>
          ${event.location ? `<p class="mb-1"><strong>Location:</strong> ${event.location}</p>` : ""}
          ${event.description ? `<p class="mb-0">${event.description}</p>` : ""}
        </div>
      `;
    }).join("");
  } catch (err) {
    listEl.innerHTML = `<p class="text-danger">Something went wrong loading events.</p>`;
  }
})();
