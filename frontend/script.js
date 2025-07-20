async function getLyrics() {
  const artist = document.getElementById("artist").value;
  const title = document.getElementById("title").value;

  const response = await fetch(`http://127.0.0.1:5000/lyrics?artist=${encodeURIComponent(artist)}&title=${encodeURIComponent(title)}`);
  const data = await response.json();

  const lyricsDiv = document.getElementById("lyrics");
  lyricsDiv.innerHTML = "";

  if (data.lyrics) {
    data.lyrics.forEach((lineObj, index) => {
      const lineBlock = document.createElement("div");
      lineBlock.style.marginBottom = "15px";

      lineBlock.innerHTML = `
        <p><strong>${index + 1}.</strong></p>
        <p><strong>Original:</strong> ${lineObj.original}</p>
        <p><strong>English:</strong> ${lineObj.en}</p>
        <p><strong>Türkçe:</strong> ${lineObj.tr}</p>
        <p><strong>Español:</strong> ${lineObj.es}</p>
        <hr />
      `;

      lyricsDiv.appendChild(lineBlock);
    });
  } else {
    lyricsDiv.innerHTML = "<p>Şarkı bulunamadı.</p>";
  }
}
