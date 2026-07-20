function App() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get("code");
  const state = params.get("state");

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: 500, margin: "0 auto" }}>
      <h1>Bzorp</h1>
      <p>Connect your Gmail to get daily email summaries on Telegram.</p>

      {code && state ? (
        <p>Connecting... (check backend logs)</p>
      ) : (
        <>
          <input
            type="text"
            placeholder="Telegram ID"
            id="telegramId"
            style={{ padding: 8, width: "100%", marginBottom: 12 }}
          />
          <button
            onClick={() => {
              const id = (document.getElementById("telegramId") as HTMLInputElement).value;
              if (!id) return alert("Enter your Telegram ID");
              fetch(`/api/auth/google/login?telegram_id=${id}`)
                .then((r) => r.json())
                .then((d) => { if (d.auth_url) window.location.href = d.auth_url; })
                .catch(() => alert("Failed to connect"));
            }}
            style={{ padding: "10px 20px", fontSize: 16 }}
          >
            Connect Gmail
          </button>
        </>
      )}
    </div>
  );
}

export default App;
