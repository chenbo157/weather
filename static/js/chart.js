async function queryWeather() {
  const lat = document.getElementById("lat").value;
  const lon = document.getElementById("lon").value;
  const time = document.getElementById("time").value;
  const variable = document.getElementById("var").value;

  const res = await fetch("/weather", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lat, lon, time, var: variable })
  });

  const data = await res.json();
  document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}
