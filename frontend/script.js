async function getLyrics() {
  const artist = document.getElementById("artist").value;
  const title = document.getElementById("title").value;

  const response = await fetch(`http://127.0.0.1:5000/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const data = await response.json();

  const lyricsList = document.getElementById("lyrics");
  lyricsList.innerHTML = "";

  if (data.lyrics) {
    data.lyrics.forEach(line => {
      const li = document.createElement("li");
      li.textContent = line;
      lyricsList.appendChild(li);
    });
  } else {
    lyricsList.innerHTML = "<li>Şarkı bulunamadı.</li>";
  }
}
