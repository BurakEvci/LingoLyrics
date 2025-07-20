document.getElementById("getLyrics").addEventListener("click", getLyrics);

async function getLyrics() {
  const artist = document.getElementById("artist").value;
  const title = document.getElementById("title").value;

  const response = await fetch(`http://127.0.0.1:5000/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const data = await response.json();

  const container = document.getElementById("lyricsContainer");
  container.innerHTML = "";

  // 🎧 Spotify butonunu göster
  const spotifyBtn = document.createElement("button");
  spotifyBtn.innerText = "🎧 Şarkıyı Spotify'da Dinle";
  spotifyBtn.style.marginBottom = "20px";
  spotifyBtn.onclick = async () => {
    const res = await fetch(`http://127.0.0.1:5000/spotify?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
    const json = await res.json();
    if (json.url) window.open(json.url, '_blank');
    else alert("Spotify şarkısı bulunamadı.");
  };
  container.appendChild(spotifyBtn);

  if (data.lyrics && Array.isArray(data.lyrics)) {
    data.lyrics.forEach((lineObj, index) => {
      const card = document.createElement("div");
      card.className = "lyrics-card";

      const html = `
        <div class="e-card">
          <div class="e-card-header">
            <div class="e-card-header-caption">
              <div class="e-card-title">🎵 Satır ${index + 1}</div>
              <div class="e-card-sub-title">${lineObj.original}</div>
            </div>
          </div>
          <div class="e-card-content">
            <p style="color:blue;"><strong>🇬🇧 English:</strong> ${lineObj.en}</p>
            <p style="color:black;"><strong>🇹🇷 Türkçe:</strong> ${lineObj.tr}</p>
            <p style="color:red;"><strong>🇪🇸 Español:</strong> ${lineObj.es}</p>
          </div>
        </div>
      `;
      card.innerHTML = html;
      container.appendChild(card);
    });
  } else {
    container.innerHTML += "<p>Şarkı bulunamadı veya çeviri başarısız oldu.</p>";
  }
}
