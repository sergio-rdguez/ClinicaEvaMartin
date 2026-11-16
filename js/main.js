(function () {
  "use strict";

  /* ---------- Menú móvil ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  /* ---------- Borde de la cabecera al hacer scroll ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Horario: abierto / cerrado (hora de Madrid) ---------- */
  // Tramos de apertura por día de la semana (0 = domingo). Minutos desde las 00:00.
  var weekday = [[600, 810], [960, 1230]]; // 10:00–13:30 y 16:00–20:30
  var schedule = { 0: [], 1: weekday, 2: weekday, 3: weekday, 4: weekday, 5: weekday, 6: [] };
  var dayNames = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];

  function madridNow() {
    try {
      var parts = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Madrid",
        weekday: "short",
        hour: "2-digit",
        minute: "2-digit",
        hourCycle: "h23"
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      return { day: days[map.weekday], minutes: parseInt(map.hour, 10) * 60 + parseInt(map.minute, 10) };
    } catch (err) {
      var d = new Date();
      return { day: d.getDay(), minutes: d.getHours() * 60 + d.getMinutes() };
    }
  }

  function fmt(mins) {
    var h = Math.floor(mins / 60);
    var m = mins % 60;
    return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m;
  }

  function nextOpening(now) {
    // Busca el siguiente tramo, empezando por hoy.
    for (var i = 0; i < 8; i++) {
      var day = (now.day + i) % 7;
      var slots = schedule[day];
      for (var j = 0; j < slots.length; j++) {
        if (i > 0 || slots[j][0] > now.minutes) {
          return { offset: i, day: day, time: slots[j][0] };
        }
      }
    }
    return null;
  }

  function updateStatus() {
    var box = document.querySelector("[data-status]");
    var now = madridNow();

    // Fila de hoy en la tabla
    document.querySelectorAll("[data-hours] tr").forEach(function (row) {
      row.classList.toggle("is-today", Number(row.getAttribute("data-day")) === now.day);
    });

    if (!box) return;
    var title = box.querySelector("[data-status-title]");
    var detail = box.querySelector("[data-status-detail]");

    var open = null;
    schedule[now.day].forEach(function (s) {
      if (now.minutes >= s[0] && now.minutes < s[1]) open = s;
    });

    if (open) {
      box.classList.add("is-open");
      title.textContent = "Abierto ahora";
      detail.textContent = "Hasta las " + fmt(open[1]) + ". Llámanos sin compromiso.";
      return;
    }

    box.classList.remove("is-open");
    title.textContent = "Ahora estamos cerrados";
    var next = nextOpening(now);
    if (!next) return;
    var when;
    if (next.offset === 0) when = "hoy";
    else if (next.offset === 1) when = "mañana";
    else when = "el " + dayNames[next.day];
    detail.textContent = "Abrimos " + when + " a las " + fmt(next.time) + ".";
  }

  updateStatus();
  setInterval(updateStatus, 60 * 1000);

  /* ---------- Mapa bajo demanda (sin cookies de Google hasta que se pide) ---------- */
  var mapBtn = document.querySelector("[data-map-load]");
  if (mapBtn) {
    mapBtn.addEventListener("click", function () {
      var holder = document.querySelector("[data-map]");
      var iframe = document.createElement("iframe");
      iframe.src = "https://www.google.com/maps?q=" +
        encodeURIComponent("Avenida de la Reina Sofía 10, 28919 Leganés, Madrid") +
        "&z=16&output=embed";
      iframe.title = "Mapa de la clínica en Avenida de la Reina Sofía 10, Leganés";
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      holder.innerHTML = "";
      holder.appendChild(iframe);
    });
  }

  /* ---------- Barra de llamada: aparece al dejar atrás los botones del hero ---------- */
  var callBar = document.querySelector(".call-bar");
  var heroActions = document.querySelector(".hero-actions");
  if (callBar && heroActions) {
    var updateCallBar = function () {
      callBar.classList.toggle("is-hidden", heroActions.getBoundingClientRect().bottom > 0);
    };
    window.addEventListener("scroll", updateCallBar, { passive: true });
    window.addEventListener("resize", updateCallBar);
    updateCallBar();
  }

  /* ---------- Año del pie ---------- */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
