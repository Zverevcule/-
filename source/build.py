#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for San3a: Arabic at the root, /en, /de, /ru beside it."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C
from icons import sprite, ic
import tools as TL

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
SITE_URL = ""  # e.g. "https://san3a.vercel.app" — enables canonical + hreflang when set
PAGES = ["index.html", "services.html", "how-it-works.html", "request.html", "business.html", "join.html", "contact.html"]

for k, v in C.T.items():
    assert isinstance(v, tuple) and len(v) == 4, k
for k, v in C.JS.items():
    assert len(v) == 4, k

SVC_ICON = {"plumbing": "droplet", "electric": "zap", "ac": "snowflake", "appliances": "washer", "cleaning": "sparkles", "pest": "bug",
            "painting": "roller", "carpentry": "hammer", "heaters": "flame", "b2b": "building"}


class Ctx:
    def __init__(self, lang, fname):
        self.lang, self.fname = lang, fname
        self.i = C.LANGS.index(lang)
        self.P = "" if lang == "ar" else "../"   # path to site root

    def t(self, key, **kw):
        s = C.T[key][self.i]
        return s.format(**kw) if kw else s

    def pick(self, tup):
        return tup[self.i]

    def link_lang(self, target, fname=None):
        fname = fname or self.fname
        if fname == "404.html":
            return "/index.html" if target == "ar" else f"/{target}/index.html"
        if target == self.lang:
            return fname
        if self.lang == "ar":
            return f"{target}/{fname}"
        if target == "ar":
            return f"../{fname}"
        return f"../{target}/{fname}"


# ------------------------------------------------------------------ chrome

def head(c, title, desc):
    m = C.LANG_META[c.lang]
    alt = ""
    canon = ""
    if SITE_URL:
        def url(l):
            return f"{SITE_URL}/{'' if l == 'ar' else l + '/'}{c.fname}"
        canon = f'<link rel="canonical" href="{url(c.lang)}">'
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in C.LANGS)
        alt += f'<link rel="alternate" hreflang="x-default" href="{url("ar")}">'
    og_img = f"{SITE_URL}/assets/img/og.jpg" if SITE_URL else f"{c.P}assets/img/og.jpg"
    if c.lang == "ar":
        fonts = ('<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'
                 '<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@600&display=swap&text=EnglishDeutsch%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9" rel="stylesheet">')
    else:
        fonts = ('<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
                 '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600&display=swap&text=%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9" rel="stylesheet">')
    i18n = json.dumps({k: v[c.i] for k, v in C.JS.items()}, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="{c.lang}" dir="{m["dir"]}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#174B3F">
<script>(function(){{var t=null;try{{t=localStorage.getItem("san3a-theme")}}catch(e){{}}if(!t){{t=window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}}document.documentElement.setAttribute("data-theme",t)}})();</script>
{canon}{alt}
<meta property="og:type" content="website">
<meta property="og:locale" content="{m["og"]}">
<meta property="og:site_name" content="San3a">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{c.P}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{c.P}assets/img/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<link rel="stylesheet" href="{c.P}assets/css/style.css">
<script>window.SAN3A_I18N={i18n};</script>
</head>
<body>
{sprite()}
<a class="skip-link" href="#main">{c.t("skip")}</a>
'''


def topbar(c):
    cur_attr = ' aria-current="true"'
    items = "".join(
        f'<li><a href="{c.link_lang(l)}" hreflang="{l}" lang="{l}"{cur_attr if l == c.lang else ""}>'
        f'<span>{C.LANG_META[l]["name"]}</span><span class="sr-only">{C.LANG_META[l]["code"]}</span></a></li>' for l in C.LANGS)
    return f'''<div class="topbar">
  <div class="container topbar-inner">
    <p class="tb-info" style="margin:0"><span>{ic("pin")}{c.t("tb_location")}</span><span class="hide-sm">{ic("shield")}{c.t("tb_guarantee")}</span></p>
    <div class="tb-tools">
      <details class="lang">
        <summary aria-label="{c.t("lang_label")}: {C.LANG_META[c.lang]["name"]}">{ic("globe")}<span>{C.LANG_META[c.lang]["name"]}</span>{ic("chev", "icon chev")}</summary>
        <ul class="lang-menu">{items}</ul>
      </details>
      <button class="theme-btn" type="button" aria-pressed="false" aria-label="{c.t("theme_label")}" title="{c.t("theme_dark")}">{ic("moon", "icon i-moon")}{ic("sun", "icon i-sun")}</button>
    </div>
  </div>
</div>
'''


def header(c):
    nav = [("index.html", "nav_home"), ("services.html", "nav_services"), ("how-it-works.html", "nav_how"),
           ("business.html", "nav_business"), ("join.html", "nav_join"), ("contact.html", "nav_contact")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == c.fname else ""}>{c.t(k)}</a>' for h, k in nav)
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="{c.t("home_aria")}">
      <img class="logo-on-light" src="{c.P}assets/img/logo.png" alt="{c.t("brand_alt")}" width="138" height="46">
      <img class="logo-on-dark" src="{c.P}assets/img/logo-light.png" alt="{c.t("brand_alt")}" width="138" height="46">
    </a>
    <nav class="nav" id="site-nav" aria-label="{c.t("nav_label")}">{links}</nav>
    <div class="header-cta">
      <a class="btn btn-brass btn-sm" href="request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("cta_short") if c.lang != "ar" else c.t("cta")}</span></a>
      <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="{c.t("menu")}">{ic("menu")}</button>
    </div>
  </div>
  <div class="measure" aria-hidden="true"><span class="measure-fill"></span><span class="measure-hook"></span></div>
</header>
<main id="main">
'''


def footer(c):
    svc = "".join(f'<li><a href="services.html#{s[0]}">{c.pick(s[1])}</a></li>' for s in C.SERVICES[:6])
    return f'''</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="{c.P}assets/img/logo-light.png" alt="{c.t("brand_alt")}" width="162" height="54" loading="lazy">
      <p>{c.t("footer_blurb")}</p>
      <div class="socials">
        <a data-social="facebook" aria-label="{c.t("social_fb")}" href="#">{ic("facebook")}</a>
        <a data-social="instagram" aria-label="{c.t("social_ig")}" href="#">{ic("instagram")}</a>
        <a data-social="tiktok" aria-label="{c.t("social_tt")}" href="#">{ic("tiktok")}</a>
        <a data-wa aria-label="{c.t("wa")}" href="#">{ic("whatsapp")}</a>
      </div>
    </div>
    <div><h4>{c.t("f_services")}</h4><ul>{svc}<li><a href="services.html">{c.t("all_services")}</a></li></ul></div>
    <div><h4>{c.t("f_company")}</h4><ul>
      <li><a href="how-it-works.html">{c.t("nav_how")}</a></li>
      <li><a href="how-it-works.html#guarantee">{c.t("guarantee_link")}</a></li>
      <li><a href="business.html">{c.t("nav_business")}</a></li>
      <li><a href="join.html">{c.t("nav_join")}</a></li>
      <li><a href="how-it-works.html#faq">{c.t("faq_link")}</a></li>
    </ul></div>
    <div><h4>{c.t("f_contact")}</h4><ul>
      <li><a href="contact.html">{ic("pin")}<span>{c.t("tb_location")}</span></a></li>
      <li><a data-wa href="#">{ic("whatsapp")}<span data-wa-label>{c.t("wa")}</span></a></li>
      <li><a href="contact.html">{ic("phone")}<span data-contact="phone">{c.t("phone_soon")}</span></a></li>
      <li><a href="contact.html">{ic("clock")}<span data-contact="workingHours">{c.t("hours_soon")}</span></a></li>
    </ul></div>
  </div>
  <div class="container footer-bottom">
    <span>© <span data-year>2026</span> San3a. {c.t("rights")}</span>
    <span>{c.t("made_in")}</span>
  </div>
</footer>
<a class="fab-wa" aria-label="{c.t("fab")}">{ic("whatsapp")}</a>
<script src="{c.P}assets/js/config.js"></script>
<script src="{c.P}assets/js/main.js" defer></script>
<script>document.querySelectorAll("[data-year]").forEach(function(e){{e.textContent=new Date().getFullYear()}});</script>
</body>
</html>
'''


def write(c, title, desc, body):
    html = head(c, title, desc) + topbar(c) + header(c) + body + footer(c)
    out = OUT / c.fname if c.lang == "ar" else OUT / c.lang / c.fname
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


# ------------------------------------------------------------------ shared blocks

def crumbs(c, here):
    return f'<nav class="crumbs" aria-label="breadcrumb"><a href="index.html">{c.t("nav_home")}</a><span aria-hidden="true">/</span><span aria-current="page">{here}</span></nav>'


def cta_band(c):
    return f'''
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="cta-band">
      <div><h2>{c.t("cta_h2")}</h2><p>{c.t("cta_p")}</p></div>
      <div class="actions">
        <a class="btn btn-brass" href="request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("cta")}</span></a>
        <a class="btn btn-on-band" data-wa href="#">{ic("whatsapp")}<span data-wa-label>{c.t("cta_wa")}</span></a>
      </div>
    </div>
  </div>
</section>'''


STEP_KEYS = [("clipboard", "st1_h", "st1_p"), ("users", "st2_h", "st2_p"), ("tag", "st3_h", "st3_p"), ("shield", "st4_h", "st4_p")]


def pipeline(c, items, cls="pipeline"):
    lis = "".join(
        f'<li class="stage" style="--d:{i * 0.85:.2f}s"><span class="valve">{ic(icn)}</span>'
        f'<span class="num">{i + 1:02d}</span><h3>{c.t(h)}</h3><p>{c.t(p)}</p></li>' for i, (icn, h, p) in enumerate(items))
    return f'<ol class="{cls}" data-inview>{lis}</ol>'


def faq(c, items):
    return '<div class="faq">' + "".join(
        f'<details><summary><span>{c.pick(q)}</span><span class="plus" aria-hidden="true">{ic("plus")}</span></summary><p>{c.pick(a)}</p></details>'
        for q, a in items) + '</div>'


def checks(c, keys, icon="check"):
    return '<ul class="checks">' + "".join(f'<li>{ic(icon)}<span>{c.t(k)}</span></li>' for k in keys) + '</ul>'


def guarantee_panel(c, h_key, p_key, btn):
    return f'''<div class="guarantee" data-inview>
      <div class="gear">{TL.gear_svg()}<div class="gear-num"><b data-count-to="15">15</b><span>{c.t("g_days")}</span></div></div>
      <div><h2>{c.t(h_key)}</h2><p>{c.t(p_key)}</p></div>
      {btn}
    </div>'''


# ------------------------------------------------------------------ pages

def page_index(c):
    names = [c.pick(s[1]) for s in C.SERVICES]
    tape_items = "".join(f'<span class="tape-item">{n}{TL.SCREW}</span>' for n in names * 2)
    pegs = ""
    for i, (key, nm, sh, chips, flag) in enumerate(C.SERVICES):
        fl = f'<span class="flag">{c.t(flag)}</span>' if flag == "tag_summer" else ""
        pegs += (f'<a class="peg" href="services.html#{key}">{TL.peg_svg(key)}'
                 f'<div class="plate">{fl}<h3>{c.pick(nm)}</h3><p>{c.pick(sh)}</p></div></a>')
    tk_steps = "".join(f'<li style="--d:{0.35 + i * 0.5:.2f}s">{TL.TICK}<span>{c.t(k)}</span></li>' for i, k in enumerate(["tk_s1", "tk_s2", "tk_s3", "tk_s4", "tk_s5"]))
    body = f'''
<section class="hero blueprint">
  <div class="container hero-grid">
    <div class="hero-copy">
      <h1>{c.t("hero_h1")}</h1>
      <p class="lead">{c.t("hero_lead")}</p>
      <div class="hero-actions">
        <a class="btn btn-brass" href="request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("cta")}</span></a>
        <a class="btn btn-line" href="services.html"><span>{c.t("see_services")}</span></a>
      </div>
      <p class="hero-area">{ic("pin")}<span>{c.t("hero_area")}</span></p>
    </div>
    <div class="hero-visual">
      <div class="photo-frame">
        <img src="{c.P}assets/img/hero.webp" alt="{c.t("hero_alt")}" width="880" height="1100" fetchpriority="high">
        <div class="roller-track" aria-hidden="true"><div class="roller"></div></div>
      </div>
      <div class="nut-badge" data-loop>{TL.nut_badge_svg()}<div><strong>{c.t("badge_t")}</strong><small>{c.t("badge_s")}</small></div></div>
    </div>
  </div>
</section>

<div class="tape-wrap">
  <div class="tape-band" data-loop>
    <div class="tape-viewport" aria-hidden="true"><div class="tape-track">{tape_items}{tape_items}</div></div>
    <button class="tape-pause" type="button" aria-pressed="false" aria-label="{c.t("tape_pause")}">{ic("pause", "icon i-pause")}{ic("play", "icon i-play")}</button>
  </div>
</div>

<section class="section-tight">
  <div class="container">
    <div class="specs" role="list" aria-label="{c.t("specs_label")}">
      <div class="spec" role="listitem"><b>{c.t("spec1_b")}</b><p>{c.t("spec1_p")}</p></div>
      <div class="spec" role="listitem"><b>{c.t("spec2_b")}</b><p>{c.t("spec2_p")}</p></div>
      <div class="spec" role="listitem"><b>{c.t("spec3_b")}</b><p>{c.t("spec3_p")}</p></div>
      <div class="spec" role="listitem"><b>{c.t("spec4_b")}</b><p>{c.t("spec4_p")}</p></div>
    </div>
  </div>
</section>

<section class="section pegboard" id="services">
  <div class="container">
    <div class="sign"><h2>{c.t("svc_h2")}</h2><p>{c.t("svc_lead")}</p></div>
    <div class="peg-grid" data-inview data-pegs>{pegs}</div>
  </div>
</section>

<section class="section process blueprint">
  <div class="container">
    <div class="section-head"><h2>{c.t("proc_h2")}</h2><p>{c.t("proc_lead")}</p></div>
    {pipeline(c, STEP_KEYS)}
    <div class="actions">
      <a class="btn btn-brass" href="request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("start_request")}</span></a>
      <a class="btn btn-on-band" href="how-it-works.html"><span>{c.t("full_details")}</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div>
      <h2>{c.t("price_h2")}</h2>
      <p class="muted" style="font-size:1.12rem">{c.t("price_p")}</p>
      {checks(c, ["price_b1", "price_b2"])}
    </div>
    <div class="ticket" data-inview>
      <div class="ticket-head"><span class="ticket-title">{c.t("tk_title")}</span><span class="ticket-meta"><span class="ticket-id">SN-24K7Q</span><span class="ticket-sample">{c.t("tk_sample")}</span></span></div>
      <p class="ticket-job">{c.t("tk_job")}</p>
      <ol class="ticket-steps">{tk_steps}</ol>
      <dl class="ticket-lines">
        <div><dt>{c.t("tk_labor")}</dt><dd>{c.t("tk_labor_v")}</dd></div>
        <div><dt>{c.t("tk_mat")}</dt><dd>{c.t("tk_mat_v")}</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" id="guarantee">
  <div class="container">
    {guarantee_panel(c, "g_h2", "g_p", f'<a class="btn btn-brass" href="how-it-works.html#guarantee"><span>{c.t("g_terms")}</span></a>')}
  </div>
</section>

<section class="section" style="padding-top:clamp(1rem,3vw,2rem)">
  <div class="container">
    <div class="section-head"><h2>{c.t("aud_h2")}</h2></div>
    <div class="cols3">
      <div class="col">{ic("home", "big-ic")}<h3>{c.t("aud1_h")}</h3><p>{c.t("aud1_p")}</p></div>
      <div class="col">{ic("key", "big-ic")}<h3>{c.t("aud2_h")}</h3><p>{c.t("aud2_p")}</p></div>
      <div class="col">{ic("bed", "big-ic")}<h3>{c.t("aud3_h")}</h3><p>{c.t("aud3_p")}</p></div>
    </div>
    <div class="actions"><a class="btn btn-line" href="business.html"><span>{c.t("aud_link")}</span></a></div>
  </div>
</section>

<section class="section" style="background:var(--bg-2)">
  <div class="container split reverse">
    <div class="media"><img src="{c.P}assets/img/toolbelt.webp" alt="{c.t("belt_alt")}" width="1000" height="1000" loading="lazy"></div>
    <div>
      <h2>{c.t("tech_h2")}</h2>
      <p class="muted" style="font-size:1.12rem">{c.t("tech_p")}</p>
      {checks(c, ["tech_b1", "tech_b2", "tech_b3"])}
      <div class="actions"><a class="btn btn-solid" href="join.html">{ic("users")}<span>{c.t("tech_btn")}</span></a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><h2>{c.t("faq_h2")}</h2></div>
    {faq(c, C.FAQ[:4])}
    <p style="margin-top:1.5rem"><a href="how-it-works.html#faq">{c.t("faq_all")}</a></p>
  </div>
</section>
{cta_band(c)}
'''
    write(c, c.t("home_title"), c.t("home_desc"), body)


def page_services(c):
    rows = ""
    for key, nm, sh, chips, flag in C.SERVICES:
        fl = f'<span class="flag-inline">{c.t(flag)}</span>' if flag else ""
        chip_html = "".join(f"<li>{x}</li>" for x in c.pick(chips))
        if key == "b2b":
            btn = f'<a class="btn btn-solid btn-sm" href="business.html"><span>{c.t("get_quote")}</span></a>'
        else:
            btn = f'<a class="btn btn-brass btn-sm" href="request.html#svc-{key}"><span>{c.t("req_this")}</span></a>'
        rows += (f'<article class="svc" id="{key}"><div class="svc-tool">{TL.small_tool_svg(key)}</div>'
                 f'<div><h2>{c.pick(nm)}{fl}</h2><p>{c.pick(sh)}</p></div>'
                 f'<ul class="chips" aria-label="{c.t("examples")}">{chip_html}</ul>{btn}</article>')
    body = f'''
<section class="page-head blueprint">
  <div class="container">
    {crumbs(c, c.t("svcpage_h1"))}
    <h1>{c.t("svcpage_h1")}</h1>
    <p class="lead">{c.t("svcpage_lead")}</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="svc-rows">{rows}</div>
    <div class="notice">{ic("info")}<span>{c.t("svc_notice")}</span></div>
  </div>
</section>
{cta_band(c)}
'''
    write(c, f'{c.t("svcpage_h1")} | San3a', c.t("svcpage_lead"), body)


def page_how(c):
    cover = [("check-circle", "gc1_h", "gc1_p"), ("receipt", "gc2_h", "gc2_p"), ("x", "gc3_h", "gc3_p"), ("message", "gc4_h", "gc4_p")]
    cols = "".join(f'<div class="col">{ic(i, "big-ic")}<h3>{c.t(h)}</h3><p>{c.t(p)}</p></div>' for i, h, p in cover)
    body = f'''
<section class="page-head blueprint">
  <div class="container">
    {crumbs(c, c.t("how_h1"))}
    <h1>{c.t("how_h1")}</h1>
    <p class="lead">{c.t("how_lead")}</p>
  </div>
</section>
<section class="section process blueprint">
  <div class="container">
    <div class="section-head"><h2>{c.t("how_steps_h2")}</h2></div>
    {pipeline(c, STEP_KEYS)}
  </div>
</section>
<section class="section" id="pricing">
  <div class="container split">
    <div>
      <h2>{c.t("pol_h2")}</h2>
      <p class="muted" style="font-size:1.12rem">{c.t("pol_p")}</p>
      {checks(c, ["pol_1", "pol_2", "pol_3", "pol_4"])}
    </div>
    <div class="media tall"><img src="{c.P}assets/img/toolbag.webp" alt="{c.t("bag_alt")}" width="1000" height="1250" loading="lazy"></div>
  </div>
</section>
<section class="section" id="guarantee" style="padding-top:0">
  <div class="container">
    {guarantee_panel(c, "gp_h2", "gp_p", f'<a class="btn btn-brass" href="request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("cta")}</span></a>')}
    <div class="cols4" style="margin-top:2.5rem">{cols}</div>
  </div>
</section>
<section class="section" id="support" style="background:var(--bg-2)">
  <div class="container split reverse">
    <div class="media"><img src="{c.P}assets/img/tools.webp" alt="{c.t("tools_alt")}" width="332" height="342" loading="lazy"></div>
    <div>
      <h2>{c.t("sup_h2")}</h2>
      <p class="muted" style="font-size:1.12rem">{c.t("sup_p")}</p>
      {checks(c, ["sup_1", "sup_2", "sup_3"])}
    </div>
  </div>
</section>
<section class="section" id="faq">
  <div class="container">
    <div class="section-head"><h2>{c.t("faq_h2_full")}</h2></div>
    {faq(c, C.FAQ)}
  </div>
</section>
{cta_band(c)}
'''
    write(c, f'{c.t("how_h1")} | San3a', c.t("how_lead"), body)


def page_request(c):
    choices = "".join(
        f'<label class="choice"><input type="radio" name="service" value="{k}" data-label="{c.pick(nm)}"><span>{ic(SVC_ICON[k])}{c.pick(nm)}</span></label>'
        for k, nm, *_ in C.SERVICES if k != "b2b")
    areas = "".join(f"<option>{c.pick(a)}</option>" for a in C.AREAS)
    body = f'''
<section class="page-head blueprint" style="padding-bottom:1.5rem">
  <div class="container">
    {crumbs(c, c.t("req_h1"))}
    <h1>{c.t("req_h1")}</h1>
    <p class="lead">{c.t("req_lead")}</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container form-shell">
    <div class="card">
      <ol class="progress" aria-label="{c.t("pr_label")}">
        <li class="active" aria-current="step">1 <span>{c.t("pr1")}</span></li>
        <li>2 <span>{c.t("pr2")}</span></li>
        <li>3 <span>{c.t("pr3")}</span></li>
      </ol>
      <form id="requestForm" novalidate>
        <div class="form-step active">
          <h2>{c.t("s1_h")}</h2>
          <p class="hint">{c.t("s1_hint")}</p>
          <div class="field" data-required="radio">
            <span class="label" id="svcLbl">{c.t("f_service")}</span>
            <div class="choice-grid" role="radiogroup" aria-labelledby="svcLbl">{choices}</div>
            <span class="error-msg">{c.t("e_service")}</span>
          </div>
          <div class="field" data-required="min15">
            <label for="description">{c.t("f_desc")}</label>
            <textarea class="input" id="description" name="description" maxlength="1000" placeholder="{c.t("ph_desc")}" aria-describedby="descHelp"></textarea>
            <span class="help" id="descHelp">{c.t("h_desc")}</span>
            <span class="error-msg">{c.t("e_desc")}</span>
          </div>
          <div class="field">
            <span class="label">{c.t("f_photos")} <span class="opt">{c.t("o_photos")}</span></span>
            <label class="upload" for="photos">{ic("camera")}<strong>{c.t("up_strong")}</strong><small>{c.t("up_small")}</small></label>
            <input class="sr-only" type="file" id="photos" accept="image/*" multiple>
            <span class="error-msg" id="photoError" role="alert"></span>
            <div class="thumbs"></div>
            <span class="help" id="photoCount" aria-live="polite"></span>
          </div>
          <div class="field" data-required="radio">
            <span class="label" id="urgLbl">{c.t("f_urg")}</span>
            <div class="choice-grid c3" role="radiogroup" aria-labelledby="urgLbl">
              <label class="choice"><input type="radio" name="urgency" value="urgent" data-label="{c.t("u1")}"><span>{ic("zap")}{c.t("u1")}</span></label>
              <label class="choice"><input type="radio" name="urgency" value="soon" data-label="{c.t("u2")}" checked><span>{ic("clock")}{c.t("u2")}</span></label>
              <label class="choice"><input type="radio" name="urgency" value="flexible" data-label="{c.t("u3")}"><span>{ic("calendar")}{c.t("u3")}</span></label>
            </div>
            <span class="error-msg">{c.t("e_urg")}</span>
          </div>
          <div class="form-nav"><button type="button" class="btn btn-solid btn-next" data-next><span>{c.t("next")}</span></button></div>
        </div>

        <div class="form-step">
          <h2>{c.t("s2_h")}</h2>
          <p class="hint">{c.t("s2_hint")}</p>
          <div class="field-row">
            <div class="field" data-required="text"><label for="name">{c.t("f_name")}</label><input class="input" id="name" name="name" autocomplete="name" placeholder="{c.t("ph_name")}"><span class="error-msg">{c.t("e_name")}</span></div>
            <div class="field" data-required="phone"><label for="phone">{c.t("f_phone")}</label><input class="input" id="phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="{c.t("ph_phone")}"><span class="error-msg">{c.t("e_phone")}</span></div>
          </div>
          <div class="field" data-required="text">
            <label for="area">{c.t("f_area")}</label>
            <select class="input" id="area" name="area"><option value="">{c.t("o_area")}</option>{areas}</select>
            <span class="error-msg">{c.t("e_area")}</span>
          </div>
          <div class="field" data-required="text">
            <label for="address">{c.t("f_addr")}</label>
            <input class="input" id="address" name="address" autocomplete="street-address" placeholder="{c.t("ph_addr")}">
            <span class="error-msg">{c.t("e_addr")}</span>
            <div><button type="button" class="inline-btn" id="useLocation">{ic("pin")}{c.t("loc_btn")}</button><span class="loc-status" id="locStatus" aria-live="polite"></span></div>
            <input type="hidden" id="locationUrl" name="location_url">
          </div>
          <div class="field">
            <span class="label" id="timeLbl">{c.t("f_time")} <span class="opt">{c.t("optional")}</span></span>
            <div class="choice-grid c3" role="radiogroup" aria-labelledby="timeLbl">
              <label class="choice"><input type="radio" name="timeslot" value="morning" data-label="{c.t("t1")}"><span>{c.t("t1")}</span></label>
              <label class="choice"><input type="radio" name="timeslot" value="afternoon" data-label="{c.t("t2")}"><span>{c.t("t2")}</span></label>
              <label class="choice"><input type="radio" name="timeslot" value="evening" data-label="{c.t("t3")}"><span>{c.t("t3")}</span></label>
            </div>
          </div>
          <div class="form-nav">
            <button type="button" class="btn btn-line" data-prev><span>{c.t("back")}</span></button>
            <button type="button" class="btn btn-solid btn-next" data-next><span>{c.t("review_btn")}</span></button>
          </div>
        </div>

        <div class="form-step">
          <h2>{c.t("s3_h")}</h2>
          <p class="hint">{c.t("s3_hint")}</p>
          <dl class="review" id="reviewList"></dl>
          <div class="notice">{ic("tag")}<span>{c.t("s3_notice")}</span></div>
          <p class="error-msg" id="submitError" role="alert"></p>
          <div class="form-nav">
            <button type="button" class="btn btn-line" data-prev><span>{c.t("edit")}</span></button>
            <button type="submit" class="btn btn-brass btn-next">{ic("check")}<span>{c.t("send_req")}</span></button>
          </div>
          <p class="consent">{c.t("consent")}</p>
        </div>
      </form>

      <div id="requestSuccess" class="success" hidden>
        {TL.done_mark_svg()}
        <h2>{c.t("ok_h")}</h2>
        <p class="muted" style="margin:0">{c.t("ok_num")}</p>
        <div class="order-id" id="orderId">SN-000000</div>
        <ul class="checks next-steps">
          <li>{ic("check")}<span>{c.t("ok_1")}</span></li>
          <li>{ic("check")}<span>{c.t("ok_2")}</span></li>
          <li>{ic("check")}<span>{c.t("ok_3")}</span></li>
        </ul>
        <div class="actions">
          <a class="btn btn-brass" id="successWa" href="#">{ic("whatsapp")}<span data-wa-label>{c.t("ok_wa")}</span></a>
          <a class="btn btn-line" href="index.html"><span>{c.t("back_home")}</span></a>
        </div>
        <div class="notice" id="demoNote" hidden>{ic("info")}<span>{c.t("demo_req")}</span></div>
      </div>
    </div>

    <aside class="card aside-card">
      <h3>{c.t("why_h")}</h3>
      <ul class="checks">
        <li>{ic("shield")}<span>{c.t("why_1")}</span></li>
        <li>{ic("tag")}<span>{c.t("why_2")}</span></li>
        <li>{ic("users")}<span>{c.t("why_3")}</span></li>
        <li>{ic("headset")}<span>{c.t("why_4")}</span></li>
      </ul>
      <hr>
      <p class="muted" style="font-size:.95rem;margin-bottom:.75rem">{c.t("prefer_wa")}</p>
      <a class="btn btn-line btn-block" data-wa href="#">{ic("whatsapp")}<span data-wa-label>{c.t("req_wa")}</span></a>
    </aside>
  </div>
</section>
'''
    write(c, f'{c.t("req_h1")} | San3a', c.t("req_lead"), body)


def simple_success(c, sid, h, p, note="demo_short"):
    return (f'<div id="{sid}" class="success" hidden>{TL.done_mark_svg()}<h2>{c.t(h)}</h2><p class="muted">{c.t(p)}</p>'
            f'<div class="notice" data-demo-note hidden>{ic("info")}<span>{c.t(note)}</span></div></div>')


def page_business(c):
    inc = [("calendar", "bi1_h", "bi1_p"), ("zap", "bi2_h", "bi2_p"), ("camera", "bi3_h", "bi3_p"), ("receipt", "bi4_h", "bi4_p")]
    inc_cols = "".join(f'<div class="col">{ic(i, "big-ic")}<h3>{c.t(h)}</h3><p>{c.t(p)}</p></div>' for i, h, p in inc)
    body = f'''
<section class="page-head blueprint">
  <div class="container split">
    <div>
      {crumbs(c, c.t("nav_business"))}
      <h1>{c.t("biz_h1")}</h1>
      <p class="lead">{c.t("biz_lead")}</p>
      <div class="actions">
        <a class="btn btn-brass" href="#b2b-form">{ic("clipboard")}<span>{c.t("get_quote")}</span></a>
        <a class="btn btn-line" data-wa data-wa-text="{c.t("biz_wa_text")}" href="#">{ic("whatsapp")}<span data-wa-label>{c.t("cta_wa")}</span></a>
      </div>
    </div>
    <div class="media"><img src="{c.P}assets/img/electric.webp" alt="{c.t("elec_alt")}" width="1000" height="1000"></div>
  </div>
</section>
<section class="section" style="background:var(--bg-2)">
  <div class="container">
    <div class="section-head"><h2>{c.t("biz_who_h2")}</h2></div>
    <div class="cols3">
      <div class="col">{ic("key", "big-ic")}<h3>{c.t("aud2_h")}</h3><p>{c.t("bw1_p")}</p></div>
      <div class="col">{ic("bed", "big-ic")}<h3>{c.t("aud3_h")}</h3><p>{c.t("bw2_p")}</p></div>
      <div class="col">{ic("building", "big-ic")}<h3>{c.t("bw3_h")}</h3><p>{c.t("bw3_p")}</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><h2>{c.t("biz_inc_h2")}</h2></div>
    <div class="cols4">{inc_cols}</div>
  </div>
</section>
<section class="section" id="b2b-form" style="padding-top:0">
  <div class="container form-shell">
    <div class="card">
      <form class="simple-form" data-form="b2b_inquiry" data-success="b2bSuccess" novalidate>
        <h2>{c.t("get_quote")}</h2>
        <p class="muted">{c.t("bf_p")}</p>
        <div class="field-row">
          <div class="field" data-required="text"><label for="b-name">{c.t("bf_contact")}</label><input class="input" id="b-name" name="contact_name" autocomplete="name"><span class="error-msg">{c.t("e_name")}</span></div>
          <div class="field" data-required="text"><label for="b-company">{c.t("bf_company")}</label><input class="input" id="b-company" name="company" autocomplete="organization"><span class="error-msg">{c.t("e_company")}</span></div>
        </div>
        <div class="field-row">
          <div class="field" data-required="text"><label for="b-type">{c.t("bf_type")}</label>
            <select class="input" id="b-type" name="business_type"><option value="">{c.t("choose")}</option><option>{c.t("bt1")}</option><option>{c.t("bt2")}</option><option>{c.t("bt3")}</option><option>{c.t("bt4")}</option></select>
            <span class="error-msg">{c.t("e_type")}</span></div>
          <div class="field"><label for="b-units">{c.t("bf_units")} <span class="opt">{c.t("approx")}</span></label><input class="input" id="b-units" name="units" inputmode="numeric" placeholder="{c.t("ph_units")}"></div>
        </div>
        <div class="field" data-required="phone"><label for="b-phone">{c.t("f_phone")}</label><input class="input" id="b-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="{c.t("ph_phone")}"><span class="error-msg">{c.t("e_phone")}</span></div>
        <div class="field"><label for="b-needs">{c.t("bf_needs")} <span class="opt">{c.t("optional")}</span></label><textarea class="input" id="b-needs" name="needs" placeholder="{c.t("ph_needs")}"></textarea></div>
        <p class="error-msg submit-error" role="alert"></p>
        <button class="btn btn-brass" type="submit">{ic("check")}<span>{c.t("send")}</span></button>
      </form>
      {simple_success(c, "b2bSuccess", "bok_h", "bok_p")}
    </div>
    <aside class="card aside-card">
      <h3>{c.t("biz_why_h")}</h3>
      <ul class="checks">
        <li>{ic("headset")}<span>{c.t("bwy_1")}</span></li>
        <li>{ic("users")}<span>{c.t("bwy_2")}</span></li>
        <li>{ic("shield")}<span>{c.t("bwy_3")}</span></li>
        <li>{ic("receipt")}<span>{c.t("bwy_4")}</span></li>
      </ul>
    </aside>
  </div>
</section>
'''
    write(c, f'{c.t("nav_business")} | San3a', c.t("biz_lead"), body)


def page_join(c):
    ben = [("camera", "jb1_h", "jb1_p"), ("route", "jb2_h", "jb2_p"), ("calendar", "jb3_h", "jb3_p"), ("star", "jb4_h", "jb4_p")]
    ben_cols = "".join(f'<div class="col">{ic(i, "big-ic")}<h3>{c.t(h)}</h3><p>{c.t(p)}</p></div>' for i, h, p in ben)
    reqs = '<ul class="checks">' + "".join(f'<li>{ic(i)}<span>{c.t(k)}</span></li>' for i, k in
                                           [("id", "jr_1"), ("wrench", "jr_2"), ("clock", "jr_3"), ("tag", "jr_4"), ("shield", "jr_5")]) + '</ul>'
    specs = "".join(f'<label class="choice"><input type="checkbox" name="specialties" value="{k}"><span>{ic(SVC_ICON[k])}{c.pick(nm)}</span></label>'
                    for k, nm, *_ in C.SERVICES if k != "b2b")
    areas = "".join(f"<option>{c.pick(a)}</option>" for a in C.AREAS)
    body = f'''
<section class="page-head blueprint">
  <div class="container split">
    <div>
      {crumbs(c, c.t("nav_join"))}
      <h1>{c.t("join_h1")}</h1>
      <p class="lead">{c.t("join_lead")}</p>
      <div class="actions"><a class="btn btn-brass" href="#join-form">{ic("users")}<span>{c.t("join_now")}</span></a></div>
    </div>
    <div class="media tall"><img src="{c.P}assets/img/toolbag.webp" alt="{c.t("bag_alt")}" width="1000" height="1250"></div>
  </div>
</section>
<section class="section" style="background:var(--bg-2)">
  <div class="container">
    <div class="section-head"><h2>{c.t("jb_h2")}</h2></div>
    <div class="cols4">{ben_cols}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><h2>{c.t("jr_h2")}</h2></div>
    {reqs}
  </div>
</section>
<section class="section process blueprint">
  <div class="container">
    <div class="section-head"><h2>{c.t("js_h2")}</h2></div>
    {pipeline(c, [("clipboard", "js1_h", "js1_p"), ("phone", "js2_h", "js2_p"), ("wrench", "js3_h", "js3_p")], "pipeline three")}
  </div>
</section>
<section class="section" id="join-form">
  <div class="container" style="max-width:860px">
    <div class="card">
      <form class="simple-form" data-form="technician_signup" data-success="joinSuccess" novalidate>
        <h2>{c.t("jf_h2")}</h2>
        <p class="muted">{c.t("jf_p")}</p>
        <div class="field-row">
          <div class="field" data-required="text"><label for="j-name">{c.t("jf_name")}</label><input class="input" id="j-name" name="name" autocomplete="name"><span class="error-msg">{c.t("e_name")}</span></div>
          <div class="field" data-required="phone"><label for="j-phone">{c.t("f_phone")}</label><input class="input" id="j-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="{c.t("ph_phone")}"><span class="error-msg">{c.t("e_phone")}</span></div>
        </div>
        <div class="field" data-required="checkbox">
          <span class="label" id="specLbl">{c.t("jf_spec")} <span class="opt">{c.t("o_spec")}</span></span>
          <div class="choice-grid" role="group" aria-labelledby="specLbl">{specs}</div>
          <span class="error-msg">{c.t("e_spec")}</span>
        </div>
        <div class="field-row">
          <div class="field" data-required="text"><label for="j-years">{c.t("jf_years")}</label>
            <select class="input" id="j-years" name="experience"><option value="">{c.t("choose")}</option><option>{c.t("y1")}</option><option>{c.t("y2")}</option><option>{c.t("y3")}</option><option>{c.t("y4")}</option></select>
            <span class="error-msg">{c.t("e_years")}</span></div>
          <div class="field" data-required="text"><label for="j-area">{c.t("jf_area")}</label>
            <select class="input" id="j-area" name="area"><option value="">{c.t("choose")}</option><option>{c.t("all_hurghada")}</option>{areas}</select>
            <span class="error-msg">{c.t("e_area")}</span></div>
        </div>
        <div class="field">
          <span class="label" id="toolsLbl">{c.t("jf_tools")}</span>
          <div class="choice-grid c3" role="radiogroup" aria-labelledby="toolsLbl">
            <label class="choice"><input type="radio" name="has_tools" value="yes" checked><span>{c.t("tools_y")}</span></label>
            <label class="choice"><input type="radio" name="has_tools" value="partial"><span>{c.t("tools_p")}</span></label>
            <label class="choice"><input type="radio" name="has_tools" value="no"><span>{c.t("tools_n")}</span></label>
          </div>
        </div>
        <div class="field"><label for="j-notes">{c.t("jf_notes")} <span class="opt">{c.t("optional")}</span></label><textarea class="input" id="j-notes" name="notes" placeholder="{c.t("ph_notes")}"></textarea></div>
        <p class="error-msg submit-error" role="alert"></p>
        <button class="btn btn-brass" type="submit">{ic("check")}<span>{c.t("jf_send")}</span></button>
      </form>
      {simple_success(c, "joinSuccess", "jok_h", "jok_p")}
    </div>
  </div>
</section>
'''
    write(c, f'{c.t("nav_join")} | San3a', c.t("join_lead"), body)


def page_contact(c):
    soon = f'<span class="soon">{c.t("soon")}</span>'
    body = f'''
<section class="page-head blueprint">
  <div class="container">
    {crumbs(c, c.t("ct_h1"))}
    <h1>{c.t("ct_h1")}</h1>
    <p class="lead">{c.t("ct_lead", req="request.html")}</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container form-shell">
    <ul class="contact-list">
      <li><span class="ic">{ic("whatsapp")}</span><div><h3>{c.t("wa")}</h3><p><a data-wa href="#"><span data-wa-label>{c.t("wa")}</span></a></p></div></li>
      <li><span class="ic">{ic("phone")}</span><div><h3>{c.t("c_phone")}</h3><p><a><span data-contact="phone">—</span></a>{soon}</p></div></li>
      <li><span class="ic">{ic("mail")}</span><div><h3>{c.t("c_email")}</h3><p><a><span data-contact="email">—</span></a>{soon}</p></div></li>
      <li><span class="ic">{ic("clock")}</span><div><h3>{c.t("c_hours")}</h3><p><span data-contact="workingHours">—</span>{soon}</p></div></li>
      <li><span class="ic">{ic("pin")}</span><div><h3>{c.t("c_area")}</h3><p>{c.t("c_area_v")}</p></div></li>
      <li><span class="ic">{ic("users")}</span><div><h3>{c.t("c_follow")}</h3>
        <div class="socials" style="margin-top:.35rem">
          <a data-social="facebook" aria-label="{c.t("social_fb")}" href="#">{ic("facebook")}</a>
          <a data-social="instagram" aria-label="{c.t("social_ig")}" href="#">{ic("instagram")}</a>
          <a data-social="tiktok" aria-label="{c.t("social_tt")}" href="#">{ic("tiktok")}</a>
        </div></div></li>
    </ul>
    <div class="card">
      <form class="simple-form" data-form="contact_message" data-success="contactSuccess" novalidate>
        <h2>{c.t("cf_h2")}</h2>
        <div class="field" data-required="text"><label for="c-name">{c.t("f_name")}</label><input class="input" id="c-name" name="name" autocomplete="name"><span class="error-msg">{c.t("e_name")}</span></div>
        <div class="field" data-required="phone"><label for="c-phone">{c.t("f_phone")}</label><input class="input" id="c-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="{c.t("ph_phone")}"><span class="error-msg">{c.t("e_phone")}</span></div>
        <div class="field" data-required="text"><label for="c-msg">{c.t("cf_msg")}</label><textarea class="input" id="c-msg" name="message"></textarea><span class="error-msg">{c.t("e_msg")}</span></div>
        <p class="error-msg submit-error" role="alert"></p>
        <button class="btn btn-solid btn-block" type="submit">{ic("message")}<span>{c.t("cf_send")}</span></button>
      </form>
      {simple_success(c, "contactSuccess", "cok_h", "cok_p")}
    </div>
  </div>
</section>
'''
    write(c, f'{c.t("ct_h1")} | San3a', c.t("ct_lead", req="request.html").split("<a")[0].strip(), body)


def page_404():
    c = Ctx("ar", "404.html")
    c.P = "/"   # root-absolute so the page keeps its styles at any missing URL depth
    others = "".join(f'<a class="btn btn-line btn-sm" href="/{l}/index.html" lang="{l}">{C.LANG_META[l]["name"]}</a>' for l in C.LANGS[1:])
    body = f'''
<section class="section blueprint">
  <div class="container" style="max-width:720px;text-align:center">
    <svg viewBox="0 0 120 210" width="80" height="140" aria-hidden="true" style="margin:0 auto 1rem">{TL.TOOLS["heaters"]()}</svg>
    <h1>{c.t("nf_h1")}</h1>
    <p class="muted">{c.t("nf_p")}</p>
    <p class="muted" lang="en" dir="ltr">{C.T["nf_p"][1]}</p>
    <div class="actions" style="justify-content:center">
      <a class="btn btn-solid" href="/index.html">{ic("home")}<span>{c.t("nav_home")}</span></a>
      <a class="btn btn-brass" href="/request.html">{ic("wrench", "icon icon-turn")}<span>{c.t("cta")}</span></a>
    </div>
    <div class="actions" style="justify-content:center">{others}</div>
  </div>
</section>
'''
    write(c, c.t("nf_title"), c.t("nf_p"), body)


BUILDERS = {"index.html": page_index, "services.html": page_services, "how-it-works.html": page_how, "request.html": page_request,
            "business.html": page_business, "join.html": page_join, "contact.html": page_contact}

if __name__ == "__main__":
    for lang in C.LANGS:
        for fname, fn in BUILDERS.items():
            fn(Ctx(lang, fname))
    page_404()
    print("built", sum(1 for _ in OUT.rglob("*.html")), "pages")
