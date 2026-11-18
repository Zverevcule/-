/* صَنْعَة San3a — site script (theme, language menu, workshop animations, forms) */
(function () {
  "use strict";
  var CFG = window.SAN3A_CONFIG || {};
  var I18N = window.SAN3A_I18N || {};
  var root = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function t(key, vars) {
    var s = I18N[key] || key;
    if (vars) Object.keys(vars).forEach(function (k) { s = s.replace("{" + k + "}", vars[k]); });
    return s;
  }
  function icon(name) { return '<svg class="icon" aria-hidden="true" focusable="false"><use href="#i-' + name + '"></use></svg>'; }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- Theme ---------- */
  var themeBtn = $(".theme-btn"), metaTheme = $('meta[name="theme-color"]');
  function applyTheme(mode, save) {
    root.setAttribute("data-theme", mode);
    if (save) store("san3a-theme", mode);
    if (metaTheme) metaTheme.setAttribute("content", mode === "dark" ? "#0E1B17" : "#174B3F");
    if (themeBtn) {
      themeBtn.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
      themeBtn.title = mode === "dark" ? t("themeLight") : t("themeDark");
    }
  }
  applyTheme(root.getAttribute("data-theme") || "light", false);
  if (themeBtn) themeBtn.addEventListener("click", function () {
    applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true);
  });
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onSys = function (e) { if (!store("san3a-theme")) applyTheme(e.matches ? "dark" : "light", false); };
    if (mq.addEventListener) mq.addEventListener("change", onSys);
  }

  /* ---------- Language menu (details) ---------- */
  var lang = $(".lang");
  if (lang) {
    document.addEventListener("click", function (e) { if (lang.open && !lang.contains(e.target)) lang.open = false; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && lang.open) { lang.open = false; $("summary", lang).focus(); } });
  }

  /* ---------- Mobile nav ---------- */
  var menuBtn = $(".menu-btn"), nav = $("#site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.innerHTML = open ? icon("x") : icon("menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { menuBtn.click(); menuBtn.focus(); }
    });
  }

  /* ---------- Tape-measure scroll progress ---------- */
  var measure = $(".measure"), ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      if (measure) { measure.style.setProperty("--p", p.toFixed(4)); measure.classList.toggle("is-on", window.scrollY > 24); }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- In-view triggers & off-screen pausing ---------- */
  function countUp(el) {
    var to = +el.getAttribute("data-count-to") || 0;
    if (reduceMotion) { el.textContent = to; return; }
    var start = null, dur = 1500;
    function step(ts) {
      if (!start) start = ts;
      var k = Math.min(1, (ts - start) / dur), eased = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(to * eased);
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$("[data-count-to]");
  if (!reduceMotion) counters.forEach(function (el) { el.textContent = "0"; });

  function swingPegs(scope) {
    $$(".peg .swing", scope).forEach(function (g, i) {
      setTimeout(function () { g.classList.remove("swing-now"); void g.getBoundingClientRect(); g.classList.add("swing-now"); }, reduceMotion ? 0 : i * 90);
    });
  }

  if ("IntersectionObserver" in window) {
    var once = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add("in-view");
        $$("[data-count-to]", el).forEach(countUp);
        if (el.hasAttribute("data-pegs") && !reduceMotion) swingPegs(el);
        once.unobserve(el);
      });
    }, { threshold: 0.3 });
    $$("[data-inview]").forEach(function (el) { once.observe(el); });

    var loops = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle("is-paused", !en.isIntersecting); });
    });
    $$("[data-loop]").forEach(function (el) { loops.observe(el); });
  } else {
    $$("[data-inview]").forEach(function (el) { el.classList.add("in-view"); });
    counters.forEach(function (el) { el.textContent = el.getAttribute("data-count-to"); });
  }
  document.addEventListener("visibilitychange", function () {
    $$("[data-loop]").forEach(function (el) { if (document.hidden) el.classList.add("is-paused"); });
  });

  /* ---------- Pegboard: tool swings when you reach for it ---------- */
  $$(".peg").forEach(function (peg) {
    var g = $(".swing", peg);
    if (!g) return;
    var go = function () { if (reduceMotion) return; g.classList.remove("swing-now"); void g.getBoundingClientRect(); g.classList.add("swing-now"); };
    peg.addEventListener("pointerenter", go);
    peg.addEventListener("focus", go);
    g.addEventListener("animationend", function () { g.classList.remove("swing-now"); });
  });

  /* ---------- Marquee pause control ---------- */
  var band = $(".tape-band"), pauseBtn = $(".tape-pause");
  if (band && pauseBtn) {
    pauseBtn.addEventListener("click", function () {
      var stopped = band.classList.toggle("is-stopped");
      pauseBtn.setAttribute("aria-pressed", stopped ? "true" : "false");
      pauseBtn.title = stopped ? t("tapePlay") : t("tapePause");
      store("san3a-tape", stopped ? "stopped" : "running");
    });
    if (store("san3a-tape") === "stopped") pauseBtn.click();
  }

  /* ---------- Config: WhatsApp / socials / contact ---------- */
  var waNumber = (CFG.whatsappNumber || "").replace(/\D/g, "");
  function waLink(text) { return "https://wa.me/" + waNumber + (text ? "?text=" + encodeURIComponent(text) : ""); }
  $$("[data-wa]").forEach(function (a) {
    if (waNumber) {
      a.href = waLink(a.getAttribute("data-wa-text") || t("waHello"));
      a.target = "_blank"; a.rel = "noopener";
    } else {
      a.setAttribute("aria-disabled", "true"); a.removeAttribute("href"); a.title = t("waSoonTitle");
      var lbl = $("[data-wa-label]", a); if (lbl) lbl.textContent = t("waSoon");
    }
  });
  var fab = $(".fab-wa");
  if (fab && waNumber) { fab.href = waLink(t("waHello")); fab.classList.add("is-visible"); }
  $$("[data-social]").forEach(function (a) {
    var url = (CFG.social || {})[a.getAttribute("data-social")];
    if (url) { a.href = url; a.target = "_blank"; a.rel = "noopener"; a.removeAttribute("aria-disabled"); }
    else { a.removeAttribute("href"); a.setAttribute("aria-disabled", "true"); a.title = (a.getAttribute("aria-label") || "") + " (" + t("soonSuffix") + ")"; }
  });
  $$("[data-contact]").forEach(function (el) {
    var key = el.getAttribute("data-contact"), val = CFG[key];
    if (!val) return;
    el.textContent = val;
    var soon = el.parentNode.querySelector(".soon"); if (soon) soon.remove();
    var a = el.closest("a");
    if (a && key === "phone") a.href = "tel:" + val.replace(/[^\d+]/g, "");
    if (a && key === "email") a.href = "mailto:" + val;
  });

  /* ---------- Form helpers ---------- */
  function toLatinDigits(s) {
    return String(s || "").replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); })
      .replace(/[۰-۹]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹".indexOf(d); });
  }
  function validPhone(v) {
    v = toLatinDigits(v).replace(/[\s\-().]/g, "");
    if (/^01[0125]\d{8}$/.test(v)) return true;               // Egyptian mobile
    if (/^(\+|00)20?1[0125]\d{8}$/.test(v)) return true;      // Egyptian, international form
    return /^(\+|00)\d{8,15}$/.test(v);                       // any international number
  }
  function orderId() { return "SN-" + Date.now().toString(36).slice(-6).toUpperCase(); }
  function validateFields(scope) {
    var ok = true, first = null;
    $$("[data-required]", scope).forEach(function (wrap) {
      var type = wrap.getAttribute("data-required"), bad;
      if (type === "radio" || type === "checkbox") bad = !$("input:checked", wrap);
      else {
        var v = ($("input, textarea, select", wrap).value || "").trim();
        bad = type === "phone" ? !validPhone(v) : type === "min15" ? v.length < 15 : !v;
      }
      wrap.classList.toggle("has-error", bad);
      var inp = $("input:not([type=radio]):not([type=checkbox]), textarea, select", wrap);
      if (inp) inp.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad && !first) first = wrap;
      if (bad) ok = false;
    });
    if (first) {
      var f = $("input, textarea, select", first);
      first.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
      if (f) f.focus({ preventScroll: true });
    }
    return ok;
  }
  $$("[data-required]").forEach(function (wrap) {
    var clear = function () { wrap.classList.remove("has-error"); };
    wrap.addEventListener("input", clear); wrap.addEventListener("change", clear);
  });
  function submitData(type, fd) {
    fd.append("form_type", type);
    fd.append("lang", root.getAttribute("lang") || "ar");
    fd.append("submitted_at", new Date().toISOString());
    if (CFG.formEndpoint) {
      return fetch(CFG.formEndpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return { demo: false }; });
    }
    return new Promise(function (resolve) {
      try {
        var obj = {}; fd.forEach(function (v, k) { if (!(v instanceof File)) obj[k] = v; });
        var list = JSON.parse(store("san3a_demo_submissions") || "[]"); list.push(obj);
        store("san3a_demo_submissions", JSON.stringify(list.slice(-50)));
      } catch (e) { /* demo storage is optional */ }
      setTimeout(function () { resolve({ demo: true }); }, 700);
    });
  }

  /* ---------- Request form (3 steps) ---------- */
  var form = $("#requestForm");
  if (form) (function () {
    var steps = $$(".form-step", form), prog = $$(".progress li"), cur = 0, files = [];
    var MAX_FILES = 5, MAX_MB = 8;
    var hash = (location.hash || "").replace("#svc-", "");
    var qs = new URLSearchParams(location.search).get("service");
    var pre = $('input[name="service"][value="' + (qs || hash) + '"]', form);
    if (pre) pre.checked = true;

    function show(i) {
      steps.forEach(function (s, n) { s.classList.toggle("active", n === i); });
      prog.forEach(function (p, n) { p.classList.toggle("active", n === i); p.classList.toggle("done", n < i); if (n === i) p.setAttribute("aria-current", "step"); else p.removeAttribute("aria-current"); });
      cur = i;
      if (i === steps.length - 1) buildReview();
      var top = form.getBoundingClientRect().top + window.scrollY - 120;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: reduceMotion ? "auto" : "smooth" });
      var h = $("h2", steps[i]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
    }
    $$("[data-next]", form).forEach(function (b) { b.addEventListener("click", function () { if (validateFields(steps[cur])) show(cur + 1); }); });
    $$("[data-prev]", form).forEach(function (b) { b.addEventListener("click", function () { show(cur - 1); }); });

    var fileInput = $("#photos", form), drop = $(".upload", form), thumbs = $(".thumbs", form), fileErr = $("#photoError", form), countEl = $("#photoCount", form);
    function renderThumbs() {
      thumbs.innerHTML = "";
      files.forEach(function (f, i) {
        var d = document.createElement("div"); d.className = "thumb";
        var img = document.createElement("img"); img.alt = t("imgAlt", { n: i + 1 }); img.src = URL.createObjectURL(f);
        var b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", t("imgRemove", { n: i + 1 })); b.innerHTML = icon("x");
        b.addEventListener("click", function () { files.splice(i, 1); renderThumbs(); });
        d.appendChild(img); d.appendChild(b); thumbs.appendChild(d);
      });
      countEl.textContent = files.length ? t("imgCount", { n: files.length }) : "";
    }
    function addFiles(list) {
      var msg = "";
      Array.prototype.forEach.call(list, function (f) {
        if (!/^image\//.test(f.type)) { msg = t("imgOnly"); return; }
        if (f.size > MAX_MB * 1048576) { msg = t("imgBig"); return; }
        if (files.length >= MAX_FILES) { msg = t("imgMax"); return; }
        files.push(f);
      });
      fileErr.textContent = msg; fileErr.style.display = msg ? "block" : "none";
      renderThumbs();
    }
    if (fileInput) {
      fileInput.addEventListener("change", function () { addFiles(fileInput.files); fileInput.value = ""; });
      ["dragenter", "dragover"].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("is-drag"); }); });
      ["dragleave", "drop"].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove("is-drag"); }); });
      drop.addEventListener("drop", function (e) { addFiles(e.dataTransfer.files); });
    }

    var locBtn = $("#useLocation", form), locStatus = $("#locStatus", form), locInput = $("#locationUrl", form);
    if (locBtn) locBtn.addEventListener("click", function () {
      if (!navigator.geolocation) { locStatus.textContent = t("locNo"); return; }
      locStatus.textContent = t("locWait");
      navigator.geolocation.getCurrentPosition(function (p) {
        locInput.value = "https://maps.google.com/?q=" + p.coords.latitude.toFixed(6) + "," + p.coords.longitude.toFixed(6);
        locStatus.textContent = t("locOk");
      }, function () { locStatus.textContent = t("locFail"); }, { enableHighAccuracy: true, timeout: 10000 });
    });

    function val(name) { var el = form.elements[name]; return el && el.value !== undefined ? String(el.value).trim() : ""; }
    function label(name) { var c = $('input[name="' + name + '"]:checked', form); return c ? c.getAttribute("data-label") : ""; }
    function selText(name) { var s = form.elements[name]; return s && s.selectedIndex > 0 ? s.options[s.selectedIndex].text : ""; }
    function summary() {
      return [
        [t("rService"), label("service")], [t("rDesc"), val("description")],
        [t("rPhotos"), files.length ? t("nPhotos", { n: files.length }) : t("noPhotos")], [t("rUrg"), label("urgency")],
        [t("rName"), val("name")], [t("rPhone"), toLatinDigits(val("phone"))], [t("rArea"), selText("area")],
        [t("rAddr"), val("address")], [t("rMap"), locInput && locInput.value ? t("mapSet") : "—"], [t("rTime"), label("timeslot")]
      ];
    }
    function buildReview() {
      var dl = $("#reviewList", form); dl.innerHTML = "";
      summary().forEach(function (row) {
        var d = document.createElement("div"), dt = document.createElement("dt"), dd = document.createElement("dd");
        dt.textContent = row[0]; dd.textContent = row[1] || "—"; d.appendChild(dt); d.appendChild(dd); dl.appendChild(d);
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateFields(steps[cur])) return;
      var btn = $("[type=submit]", form), span = $("span", btn), old = span.textContent;
      btn.disabled = true; span.textContent = t("sending");
      var id = orderId(), fd = new FormData(form);
      fd.append("order_id", id);
      files.forEach(function (f, i) { fd.append("photo_" + (i + 1), f, f.name); });
      submitData("service_request", fd).then(function (res) { showSuccess(id, res.demo); }).catch(function () {
        btn.disabled = false; span.textContent = old;
        var n = $("#submitError", form); n.textContent = t("sendFail"); n.style.display = "block";
      });
    });

    function showSuccess(id, demo) {
      var box = $("#requestSuccess");
      form.hidden = true; $(".progress").hidden = true; box.hidden = false;
      $("#orderId", box).textContent = id;
      if (demo) $("#demoNote", box).hidden = false;
      var text = t("waOrder", { id: id }) + "\n" + summary().map(function (r) { return r[0] + ": " + (r[1] || "—"); }).join("\n") +
        (locInput && locInput.value ? "\n" + t("waLoc") + ": " + locInput.value : "") + (files.length ? "\n" + t("waPhotos") : "");
      var wa = $("#successWa", box);
      if (waNumber) { wa.href = waLink(text); wa.target = "_blank"; wa.rel = "noopener"; }
      else { wa.setAttribute("aria-disabled", "true"); wa.removeAttribute("href"); $("[data-wa-label]", wa).textContent = t("waSoon"); }
      box.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      var h = $("h2", box); h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true });
    }
  })();

  /* ---------- Simple forms (business / technicians / contact) ---------- */
  $$(".simple-form").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateFields(f)) return;
      var btn = $("[type=submit]", f), span = $("span", btn), old = span.textContent;
      btn.disabled = true; span.textContent = t("sending");
      submitData(f.getAttribute("data-form"), new FormData(f)).then(function (res) {
        var ok = document.getElementById(f.getAttribute("data-success"));
        f.hidden = true; ok.hidden = false;
        var dn = $("[data-demo-note]", ok); if (dn && res.demo) dn.hidden = false;
        var h = $("h2, h3", ok); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
      }).catch(function () {
        btn.disabled = false; span.textContent = old;
        var n = $(".submit-error", f); if (n) { n.textContent = t("sendFail"); n.style.display = "block"; }
      });
    });
  });
})();
