async function getLyrics() {
  const artist = document.getElementById("artist").value;
  const title = document.getElementById("title").value;

  const response = await fetch(`http://127.0.0.1:5000/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const data = await response.json();

  const lyricsList = document.getElementById("lyrics");
  lyricsList.innerHTML = "";

  if (data.lyrics) {
    data.lyrics.forEach((lineObj, index) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <p><strong>${index + 1}.</strong></p>
        <p><strong>Original:</strong> ${lineObj.original}</p>
        <p><strong>English:</strong> ${lineObj.en}</p>
        <p><strong>Türkçe:</strong> ${lineObj.tr}</p>
        <p><strong>Español:</strong> ${lineObj.es}</p>
        <hr/>
      `;
      lyricsList.appendChild(li);
    });
  } else {
    lyricsList.innerHTML = "<li>Şarkı bulunamadı.</li>";
  }
}
