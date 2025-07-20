document.getElementById("getLyrics").addEventListener("click", getLyrics);

async function getLyrics() {
  const artist = document.getElementById("artist").value;
  const title = document.getElementById("title").value;
  const container = document.getElementById("lyricsContainer");
  container.innerHTML = "";

  // 🎵 Spotify
  const spotifyRes = await fetch(`http://127.0.0.1:5000/spotify?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const spotifyData = await spotifyRes.json();

  if (spotifyData.track_id) {
    // 🎧 Üst bilgi kartı (Kapak + bilgiler)
    const infoCard = document.createElement("div");
    infoCard.className = "e-card";
    infoCard.style.marginBottom = "20px";

    infoCard.innerHTML = `
      <div class="e-card-header">
        <img src="${spotifyData.album_image}" alt="Album Cover" style="height: 100px; border-radius: 8px; margin-right: 10px;" />
        <div class="e-card-header-caption">
          <div class="e-card-title">${spotifyData.track_name}</div>
          <div class="e-card-sub-title">${spotifyData.artist_name} • ${spotifyData.album_name} (${spotifyData.release_date})</div>
        </div>
      </div>
      <div class="e-card-content">
        <a href="${spotifyData.spotify_url}" target="_blank">🔗 Spotify'da Aç</a>
      </div>
    `;
    container.appendChild(infoCard);

    const iframe = document.createElement("iframe");
    iframe.src = `https://open.spotify.com/embed/track/${spotifyData.track_id}`;
    iframe.width = "100%";
    iframe.height = "80";
    iframe.frameBorder = "0";
    iframe.allow = "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture";
    iframe.allowFullscreen = true;
    iframe.style.borderRadius = "10px";
    container.appendChild(iframe);
  }

  // 🎤 Lyrics
  const response = await fetch(`http://127.0.0.1:5000/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const data = await response.json();

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
            <p style="color: blue;"><strong>🇬🇧 English:</strong> ${lineObj.en}</p>
            <p style="color: black;"><strong>🇹🇷 Türkçe:</strong> ${lineObj.tr}</p>
            <p style="color: red;"><strong>🇪🇸 Español:</strong> ${lineObj.es}</p>
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

