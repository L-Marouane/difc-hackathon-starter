"""Slide + notebook builder for the DGE workshop.

Every visual block below is lifted from the html-slide-notebook-generator Card-Template-Catalog
(same classes, palette, 14pt floor). A Slide collects blocks and only emits the CSS it uses.
A Notebook collects cells and writes a Databricks source file (.py with # MAGIC prefixes).
"""
import html as _html
import json
import re

ACCENT = {"blue": "#4299E0", "green": "#00A972", "coral": "#FF5F46", "amber": "#FFAB00", "red": "#98102A", "teal": "#1B5162"}
TINT = {"blue": "rgba(66,153,224,0.10)", "green": "rgba(0,169,114,0.10)", "coral": "rgba(255,95,70,0.10)",
        "amber": "rgba(255,171,0,0.12)", "red": "rgba(152,16,42,0.10)", "teal": "rgba(27,81,98,0.10)"}

CSS = {
    "base": """
.cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
.cw * { box-sizing: border-box; }
.mh { text-align: left; }
.mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
.mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
.mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
""",
    "banner": """
.ds-banner { display: flex; align-items: center; gap: 20px; width: 100%; border-radius: 10px; padding: 24px 28px; background: var(--bnr-bg); border-left: 8px solid var(--bnr-accent); box-shadow: 0 2px 10px rgba(27,49,57,0.08); }
.ds-banner-icon { width: 60px; height: 60px; border-radius: 50%; flex-shrink: 0; background: var(--bnr-accent); color: var(--bnr-icon-fg); font-size: 26pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; }
.ds-banner-title { font-size: 22pt; font-weight: 700; color: var(--bnr-title); line-height: 1.2; margin-bottom: 4px; }
.ds-banner-tagline { font-size: 15pt; color: var(--bnr-tagline); line-height: 1.4; }
.ds-banner.info { --bnr-bg: #1B5162; --bnr-accent: #4299E0; --bnr-icon-fg: #FFFFFF; --bnr-title: #FFFFFF; --bnr-tagline: #F9F7F4; }
.ds-banner.caution { --bnr-bg: rgba(255,171,0,0.12); --bnr-accent: #FFAB00; --bnr-icon-fg: #0b2026; --bnr-title: #0b2026; --bnr-tagline: #5E7077; }
.ds-banner.danger { --bnr-bg: rgba(255,95,70,0.10); --bnr-accent: #FF5F46; --bnr-icon-fg: #FFFFFF; --bnr-title: #98102A; --bnr-tagline: #5E7077; }
""",
    "cards": """
.ds-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
.ds-row > * { flex: 1; min-width: 230px; }
.ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
.blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;} .teal{--accent:#1B5162;}
.ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
.ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
.ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
.ds-card li { margin-bottom: 10px; }
.ds-card li:last-child { margin-bottom: 0; }
.ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
.ds-card-sub { font-size: 14pt; font-weight: 600; color: #1B5162; margin: 0 0 12px; line-height: 1.4; }
.ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
.ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; line-height: 1.4; }
.tc { text-align: center; }
""",
    "fact": """
.fc-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
.fc-row > .fc-card { flex: 1; min-width: 300px; }
.fc-card { background: #F9F7F4; border-radius: 10px; padding: 20px; border-top: 8px solid var(--accent); box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
.fc-title { font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 12px; }
.fc-intro { font-size: 14pt; line-height: 1.55; color: #0b2026; margin-bottom: 14px; }
.fc-item { display: grid; grid-template-columns: 210px 1fr; gap: 20px; padding: 12px 0; border-bottom: 1px solid #EEEDE9; align-items: start; }
.fc-item:first-child { padding-top: 4px; }
.fc-item:last-child { border-bottom: none; padding-bottom: 4px; }
.fc-key { font-size: 14pt; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; line-height: 1.3; color: var(--accent); }
.fc-val { font-size: 14pt; color: #0b2026; line-height: 1.55; }
.fc-val ul { margin: 0; padding-left: 18px; }
.fc-val li { margin-bottom: 6px; }
.fc-example { margin-top: 14px; border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; padding: 14px 16px; font-size: 14pt; line-height: 1.55; background: var(--tint); }
.fc-example strong:first-child { text-transform: uppercase; font-size: 14pt; letter-spacing: 1.5px; display: block; margin-bottom: 6px; }
""",
    "callout": """
.ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
.ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
.ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
.ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
.ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
.ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
.ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
.ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
.ds-callout.row { display: flex; align-items: center; gap: 16px; }
.ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ds-callout.caution .ds-callout-icon { color: #0b2026; }
.ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
""",
    "band": """
.ds-band-solid { background: #1B5162; color: #fff; border-radius: 10px; padding: 22px 28px; text-align: center; border-top: 6px solid var(--accent, #FF5F46); box-shadow: 0 2px 10px rgba(27,49,57,0.12); }
.ds-band-lead { font-size: 17pt; font-weight: 700; color: #fff; line-height: 1.3; margin-bottom: 8px; }
.ds-band-sub { font-size: 14pt; color: #F9F7F4; font-weight: 600; line-height: 1.4; }
.ds-band-bordered { background: #F8F9FC; border: 3px solid #1B5162; border-radius: 8px; padding: 16px 24px; text-align: center; font-size: 16pt; color: #0b2026; line-height: 1.5; }
""",
    "flow": """
.flow-grid { display: grid; gap: 0; align-items: stretch; }
.flow-step { background: #F9F7F4; border: 3px solid var(--accent, #4299E0); border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0; }
.flow-num { font-size: 26pt; font-weight: 800; color: var(--accent, #4299E0); line-height: 1; margin-bottom: 8px; }
.flow-label { font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35; }
.flow-sub { font-size: 14pt; color: #5E7077; line-height: 1.35; margin-top: 6px; font-weight: 400; }
.flow-arrow { display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1; padding: 0 6px; }
.flow-step.dim { background: #EEEDE9; border-color: #C2C2C2; box-shadow: none; opacity: 0.7; }
.flow-step.dim .flow-num { color: #90A5B1; }
.flow-step.dim .flow-label, .flow-step.dim .flow-sub { color: #5A6F77; }
.flow-arrow.dim { color: #C2C2C2; }
""",
    "steps": """
.ds-steps { display: flex; flex-direction: column; gap: 20px; }
.ds-step { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; border-top: 6px solid var(--accent, #4299E0); }
.ds-step.blue { --accent:#4299E0; --tint:rgba(66,153,224,0.10); }
.ds-step.green { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
.ds-step.amber { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
.ds-step.coral { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
.ds-step.red { --accent:#98102A; --tint:rgba(152,16,42,0.10); }
.ds-step.teal { --accent:#1B5162; --tint:rgba(27,81,98,0.10); }
.ds-step-head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.ds-step-num { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 18pt; font-weight: 800; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ds-step-title { font-size: 18pt; font-weight: 700; color: #0b2026; }
.ds-step-text { font-size: 14pt; color: #0b2026; line-height: 1.6; }
.ds-step-text ul { margin: 0; padding-left: 20px; }
.ds-step-text li { margin-bottom: 8px; }
.ds-example { margin-top: 12px; padding: 10px 12px; border-radius: 8px; font-size: 14pt; line-height: 1.5; background: var(--tint); border-left: 4px solid var(--accent); }
.ds-example ul { margin: 4px 0 0; padding-left: 18px; }
.ds-example li { margin-bottom: 4px; }
""",
    "table": """
.ds-table { width: 100%; border-collapse: collapse; font-size: 14pt; background: #F9F7F4; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
.ds-table th { text-align: left; background: #1B5162; color: #FFFFFF; font-weight: 700; padding: 10px 12px; }
.ds-table td { padding: 9px 12px; border-bottom: 1px solid #EEEDE9; vertical-align: top; line-height: 1.45; }
.ds-table tr:nth-child(even) td { background: #FFFFFF; }
.ds-table td.k { font-weight: 700; white-space: nowrap; }
.ds-table td.mono, .ds-table span.mono { font-family: Menlo, Consolas, monospace; font-size: 14pt; }
""",
    "pills": """
.ds-pill-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.ds-pill { background: #FFFFFF; border: 1px solid #EEEDE9; border-radius: 8px; padding: 14px 10px; text-align: center; font-size: 14pt; font-weight: 700; color: #0b2026; line-height: 1.3; }
.ds-grid-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin: 0 0 14px; }
.np-pills { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.np-pill { border-radius: 14px; padding: 4px 12px; font-size: 14pt; color: #0b2026; background: var(--tint, rgba(66,153,224,0.10)); border: 1px solid var(--accent, #4299E0); }
""",
    "dodont": """
.dd-head { font-size: 20pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
""",
}


def esc(s):
    return _html.escape(s, quote=False)


class Slide:
    """One %md-sandbox cell built from catalog blocks."""

    def __init__(self, notes=None):
        self.parts, self.css, self.notes, self.tail = [], ["base"], notes, []

    def _use(self, *keys):
        for k in keys:
            if k not in self.css:
                self.css.append(k)
        return self

    def raw(self, html, *css):
        self._use(*css)
        self.parts.append(html)
        return self

    # ---------------------------------------------------------------- headers
    def banner(self, title, tagline, icon=None, variant="info"):
        self._use("banner")
        ic = f'<div class="ds-banner-icon">{icon}</div>' if icon else ""
        self.parts.append(f'<div class="ds-banner {variant}">{ic}<div><div class="ds-banner-title">{title}</div>'
                          f'<div class="ds-banner-tagline">{tagline}</div></div></div>')
        return self

    def header(self, title, sub=None, eyebrow=None):
        e = f'<div class="mh-eyebrow">{eyebrow}</div>' if eyebrow else ""
        s = f'<div class="mh-sub">{sub}</div>' if sub else ""
        self.parts.append(f'<div class="mh">{e}<div class="mh-title">{title}</div>{s}</div>')
        return self

    # ---------------------------------------------------------------- cards
    def cards(self, items, kind="list"):
        """items: list of dicts. kind: list | pillar | labeled | text | stat."""
        self._use("cards")
        out = []
        for it in items:
            a = it.get("accent", "blue")
            if kind == "stat":
                out.append(f'<div class="ds-card {a} tc"><div class="ds-stat">{it["stat"]}</div><div class="ds-stat-label">{it["label"]}</div></div>')
                continue
            body = ""
            if it.get("label"):
                body += f'<div class="ds-card-label">{it["label"]}</div>'
            if it.get("title"):
                body += f'<div class="ds-card-title">{it["title"]}</div>'
            if it.get("sub"):
                body += f'<div class="ds-card-sub">{it["sub"]}</div>'
            if it.get("text"):
                cls = "ds-card-para" if kind in ("labeled",) else "ds-card-text"
                body += f'<div class="{cls}">{it["text"]}</div>'
            if it.get("items"):
                body += "<ul>" + "".join(f"<li>{x}</li>" for x in it["items"]) + "</ul>"
            if it.get("pills"):
                self._use("pills")
                body += '<div class="np-pills" style="--accent:%s; --tint:%s;">' % (ACCENT[a], TINT[a]) + "".join(
                    f'<span class="np-pill">{p}</span>' for p in it["pills"]) + "</div>"
            tc = " tc" if kind == "text" else ""
            out.append(f'<div class="ds-card {a}{tc}">{body}</div>')
        self.parts.append('<div class="ds-row">' + "".join(out) + "</div>")
        return self

    def do_dont(self, do, dont, do_title="&check; DO", dont_title="&times; DON'T"):
        self._use("cards", "dodont")
        self.parts.append('<div class="ds-row">'
                          f'<div class="ds-card green"><div class="dd-head">{do_title}</div><ul>' + "".join(f"<li>{x}</li>" for x in do) + "</ul></div>"
                          f'<div class="ds-card coral"><div class="dd-head">{dont_title}</div><ul>' + "".join(f"<li>{x}</li>" for x in dont) + "</ul></div></div>")
        return self

    def facts(self, cards):
        """cards: list of {title, accent, intro?, rows:[(key, val)], example?}"""
        self._use("fact")
        out = []
        for c in cards:
            a = c.get("accent", "blue")
            rows = "".join(f'<div class="fc-item"><div class="fc-key">{k}</div><div class="fc-val">{v}</div></div>' for k, v in c["rows"])
            intro = f'<div class="fc-intro">{c["intro"]}</div>' if c.get("intro") else ""
            ex = f'<div class="fc-example"><strong>{c.get("example_label", "Example")}</strong>{c["example"]}</div>' if c.get("example") else ""
            title = f'<div class="fc-title">{c["title"]}</div>' if c.get("title") else ""
            out.append(f'<div class="fc-card" style="--accent:{ACCENT[a]}; --tint:{TINT[a]};">{title}{intro}<div>{rows}</div>{ex}</div>')
        self.parts.append('<div class="fc-row">' + "".join(out) + "</div>")
        return self

    def table(self, headers, rows, key_col=True, mono_cols=()):
        self._use("table")
        th = "".join(f"<th>{h}</th>" for h in headers)
        body = ""
        for r in rows:
            tds = ""
            for i, v in enumerate(r):
                cls = []
                if key_col and i == 0:
                    cls.append("k")
                if i in mono_cols:
                    cls.append("mono")
                c = f' class="{" ".join(cls)}"' if cls else ""
                tds += f"<td{c}>{v}</td>"
            body += f"<tr>{tds}</tr>"
        self.parts.append(f'<table class="ds-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>')
        return self

    def pill_grid(self, title, pills, accent="blue", cols=4):
        self._use("cards", "pills")
        ps = "".join(f'<div class="ds-pill">{p}</div>' for p in pills)
        self.parts.append(f'<div class="ds-card {accent}"><div class="ds-grid-title">{title}</div>'
                          f'<div class="ds-pill-grid" style="grid-template-columns: repeat({cols}, 1fr);">{ps}</div></div>')
        return self

    # ---------------------------------------------------------------- callouts and bands
    def callout(self, text=None, eyebrow=None, title=None, items=None, kind="info", icon=None):
        self._use("callout")
        inner = ""
        if eyebrow:
            inner += f'<div class="ds-eyebrow">{eyebrow}</div>'
        if title:
            inner += f'<div class="ds-callout-title">{title}</div>'
        if text:
            inner += f"<div>{text}</div>"
        if items:
            inner += "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
        if icon:
            self.parts.append(f'<div class="ds-callout {kind} row"><div class="ds-callout-icon">{icon}</div><div>{inner}</div></div>')
        else:
            self.parts.append(f'<div class="ds-callout {kind}">{inner}</div>')
        return self

    def band(self, lead, sub=None, accent="coral"):
        self._use("band")
        s = f'<div class="ds-band-sub">{sub}</div>' if sub else ""
        self.parts.append(f'<div class="ds-band-solid" style="--accent:{ACCENT[accent]};"><div class="ds-band-lead">{lead}</div>{s}</div>')
        return self

    def band_bordered(self, text):
        self._use("band")
        self.parts.append(f'<div class="ds-band-bordered">{text}</div>')
        return self

    # ---------------------------------------------------------------- sequences
    def flow(self, steps, dim_from=None):
        """steps: list of (label, sub, accent). Horizontal numbered flow with arrows."""
        self._use("flow")
        cols, out = [], []
        for i, st in enumerate(steps):
            label, sub, a = (st + (None, None))[:3] if isinstance(st, tuple) else (st, None, None)
            a = a or list(ACCENT)[i % 5]
            dim = " dim" if dim_from is not None and i >= dim_from else ""
            if i:
                out.append(f'<div class="flow-arrow{dim}">&rarr;</div>')
                cols.append("auto")
            s = f'<div class="flow-sub">{sub}</div>' if sub else ""
            num = st[3] if isinstance(st, tuple) and len(st) > 3 else str(i + 1)
            out.append(f'<div class="flow-step{dim}" style="--accent:{ACCENT[a]};"><div class="flow-num">{num}</div><div class="flow-label">{label}</div>{s}</div>')
            cols.append("1fr")
        self.parts.append(f'<div class="flow-grid" style="grid-template-columns: {" ".join(cols)};">' + "".join(out) + "</div>")
        return self

    def journey(self, current):
        """Where-are-we strip: Foundations, Ingest, Transform, Activate. current = stage name."""
        self._use("flow")
        stages = [("Foundations", "Strategy, platform, medallion", "teal"), ("Ingest", "Lakeflow Connect, Auto Loader", "blue"),
                  ("Transform", "SDP, Lakeflow Designer", "green"), ("Activate", "Metric views, dashboards, Genie", "coral")]
        cols, out = [], []
        for i, (name, sub, a) in enumerate(stages):
            dim = "" if name == current else " dim"
            if i:
                out.append('<div class="flow-arrow">&rarr;</div>')
                cols.append("auto")
            out.append(f'<div class="flow-step{dim}" style="--accent:{ACCENT[a]}; padding: 10px 10px;"><div class="flow-label">{name}</div><div class="flow-sub">{sub}</div></div>')
            cols.append("1fr")
        self.parts.append(f'<div class="flow-grid" style="grid-template-columns: {" ".join(cols)};">' + "".join(out) + "</div>")
        return self

    def next_up(self, title, path):
        """Closing band pointing to the next notebook."""
        return self.band(f"Next: {title}", f"Open <code style=\"background: rgba(255,255,255,0.15); color: #FFFFFF;\">{path}</code>", accent="coral")

    def steps(self, items):
        """items: list of {title, items:[...], example?, accent?}"""
        self._use("steps")
        out = []
        for i, it in enumerate(items, start=1):
            a = it.get("accent", ["blue", "green", "amber", "coral", "teal"][(i - 1) % 5])
            ul = "<ul>" + "".join(f"<li>{x}</li>" for x in it.get("items", [])) + "</ul>" if it.get("items") else ""
            txt = f'<div>{it["text"]}</div>' if it.get("text") else ""
            ex = f'<div class="ds-example">{it["example"]}</div>' if it.get("example") else ""
            num = it.get("num", str(i))
            out.append(f'<div class="ds-step {a}"><div class="ds-step-head"><div class="ds-step-num">{num}</div>'
                       f'<div class="ds-step-title">{it["title"]}</div></div><div class="ds-step-text">{txt}{ul}{ex}</div></div>')
        self.parts.append('<div class="ds-steps">' + "".join(out) + "</div>")
        return self

    # ---------------------------------------------------------------- copy blocks (catalog section E)
    def copy_prompt(self, text, label="Prompt to Copy"):
        self.tail.append(
            '<div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;">'
            '<div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;">'
            f'<span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">{label}</span>'
            '<button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement(\'textarea\'); ta.value=pre.innerText; ta.style.position=\'fixed\'; ta.style.opacity=\'0\'; document.body.appendChild(ta); ta.select(); document.execCommand(\'copy\'); document.body.removeChild(ta); var b=this; b.innerText=\'\\u2713 Copied!\'; setTimeout(function(){b.innerText=\'Copy\';},2000);" '
            'style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div>'
            f'<pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">{esc(text)}</pre>'
            "</div>")
        return self

    def copy_code(self, code, lang="sql", label=None):
        lab = (f'<div style="font-size: 14pt; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #1B5162; margin-top: 8px;">{label}</div>'
               if label else "")
        self.tail.append(f'<div style="max-width: 1100px; margin: 0 auto; font-family: sans-serif; color: #0b2026;">{lab}'
                         f'<div class="code-block" data-language="{lang}">\n{esc(code)}\n</div></div>')
        self._prism = getattr(self, "_prism", set()) | {lang}
        return self

    # ---------------------------------------------------------------- render
    def render(self):
        css = "".join(CSS[k] for k in self.css)
        out = f'<div class="cw">\n<style>{css}</style>\n' + "\n".join(self.parts) + "\n</div>"
        if self.tail:
            out += "\n" + "\n".join(self.tail)
        if getattr(self, "_prism", None):
            langs = "".join(f'<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-{l}.min.js"></script>'
                            for l in sorted(self._prism) if l in ("sql", "python", "yaml", "bash", "json"))
            out += PRISM_HEAD + langs + PRISM_SCRIPT
        if self.notes:
            notes = re.sub(r"(?ims)^### Talking points?\s*\n.*?(?=^### |\Z)", "", self.notes).strip()
            if notes:
                out += "\n\n##### EXPAND FOR ADDITIONAL NOTES\n\n<details>\n\n" + notes + "\n\n</details>"
        return out


PRISM_HEAD = ('\n<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />'
              '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>')
PRISM_SCRIPT = """
<script>
(function() {
    document.querySelectorAll('.code-block').forEach(function(block) {
        if (block.getAttribute('data-processed')) return;
        block.setAttribute('data-processed', 'true');
        var lang = block.getAttribute('data-language') || 'sql';
        var code = block.textContent.trim();
        var id = 'code-' + Math.random().toString(36).substr(2, 9);
        block.innerHTML =
            '<div style="position:relative;margin:12px 0;">' +
                '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:6px 14px;font-size:14pt;background:#FF5F46;color:#FFFFFF;border:none;border-radius:6px;cursor:pointer;z-index:10;font-weight:700;">Copy</button>' +
                '<pre style="background:#F9F7F4;border-radius:8px;padding:16px;padding-top:44px;overflow-x:auto;margin:0;border:1px solid #EEEDE9;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Menlo,Consolas,monospace;font-size:14pt;"></code></pre>' +
            '</div>';
        var codeEl = document.getElementById(id);
        codeEl.textContent = code;
        Prism.highlightElement(codeEl);
        block.querySelector('.copy-btn').onclick = function() {
            var t = document.createElement('textarea');
            t.value = code;
            document.body.appendChild(t);
            t.select();
            document.execCommand('copy');
            document.body.removeChild(t);
            this.textContent = '\\u2713 Copied!';
            setTimeout(function(){ this.textContent = 'Copy'; }.bind(this), 2000);
        };
    });
})();
</script>"""


def quiz(questions, intro="This knowledge check is **ungraded**. Select an answer and click **Check** to see feedback."):
    """Catalog block K: knowledge-check-quiz. questions: list of (q, [opts], ans_idx, feedback)."""
    qz = json.dumps([{"q": q, "opts": o, "ans": a, "fb": f} for q, o, a, f in questions])
    key = "\n\n".join(f"**{i}. {q}**\n\n- Expected answer: **{o[a]}**\n- Why: {f}" for i, (q, o, a, f) in enumerate(questions, start=1))
    return (intro + "\n\n" + QUIZ_TEMPLATE.replace("__QZ__", qz)
            + "\n\n##### EXPAND FOR THE ANSWERS\n\n<details>\n\n" + key + "\n\n</details>")


QUIZ_TEMPLATE = """<style>
.qz-shell{display:flex;border:1px solid #DCE0E2;border-radius:12px;overflow:hidden;min-height:380px;font-family:sans-serif;max-width:1100px}
.qz-nav{flex:0 0 200px;background:#F8F9FC;border-right:1px solid #DCE0E2;padding:12px 0;display:flex;flex-direction:column;justify-content:space-between}
.qz-nav-list{display:flex;flex-direction:column;gap:2px}
.qz-nav-item{padding:10px 16px;font-size:14pt;font-weight:500;color:#5E7077;cursor:pointer;user-select:none;display:flex;align-items:center;gap:10px;transition:background .12s,color .12s}
.qz-nav-item:hover{background:#EEEDE9;color:#0b2026}
.qz-nav-item.active{background:#F8F9FC;color:#0b2026;border-right:3px solid #4299E0}
.qz-dot{width:10px;height:10px;border-radius:50%;border:2px solid #C2C2C2;flex-shrink:0;transition:background .2s,border-color .2s}
.qz-dot.answered{border-color:#4299E0;background:#4299E0}
.qz-dot.correct{border-color:#00A972;background:#00A972}
.qz-dot.wrong{border-color:#FF5F46;background:#FF5F46}
.qz-nav-footer{padding:10px 16px}
.qz-grade-btn{width:100%;padding:10px;border:none;border-radius:8px;font-size:14pt;font-weight:600;cursor:pointer;background:#4299E0;color:#fff;transition:opacity .12s}
.qz-grade-btn:hover{opacity:.85}
.qz-grade-btn:disabled{opacity:.35;cursor:default}
.qz-main{flex:1;padding:24px 28px;display:flex;flex-direction:column;justify-content:center}
.qz-q{font-size:14pt;font-weight:500;color:#0b2026;margin-bottom:16px;line-height:1.5}
.qz-q code{background:#EEEDE9;padding:1px 5px;border-radius:4px;font-size:14pt}
.qz-opts{display:flex;flex-direction:column;gap:10px}
.qz-opt{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:8px;border:1px solid #DCE0E2;background:#fff;cursor:pointer;font-size:14pt;color:#0b2026;transition:background .12s,border-color .12s;user-select:none}
.qz-opt:hover{background:#EEEDE9;border-color:#C2C2C2}
.qz-opt.selected{border-color:#4299E0;background:#F8F9FC;color:#0b2026;font-weight:500}
.qz-opt.right{border-color:#00A972;background:rgba(0,169,114,0.10);color:#00A972;font-weight:500}
.qz-opt.wrong-pick{border-color:#FF5F46;background:rgba(255,95,70,0.10);color:#FF5F46}
.qz-opt.locked{pointer-events:none}
.qz-radio{width:18px;height:18px;border-radius:50%;border:2px solid #C2C2C2;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:border-color .15s,background .15s}
.qz-opt.selected .qz-radio{border-color:#4299E0;background:#4299E0}
.qz-opt.right .qz-radio{border-color:#00A972;background:#00A972}
.qz-opt.wrong-pick .qz-radio{border-color:#FF5F46;background:#FF5F46}
.qz-radio::after{content:'';width:8px;height:8px;border-radius:50%;background:#fff;display:none}
.qz-opt.selected .qz-radio::after,.qz-opt.right .qz-radio::after,.qz-opt.wrong-pick .qz-radio::after{display:block}
.qz-fb{margin-top:14px;padding:12px 16px;border-radius:8px;font-size:14pt;line-height:1.5;display:none}
.qz-fb.show{display:block}
.qz-fb.ok{background:rgba(0,169,114,0.10);color:#00A972}
.qz-fb.no{background:rgba(255,95,70,0.10);color:#98102A}
</style>

<div class="qz-shell">
  <div class="qz-nav">
    <div class="qz-nav-list" id="qz-nav"></div>
    <div class="qz-nav-footer"></div>
  </div>
  <div class="qz-main" id="qz-main"></div>
</div>

<script>
var QZ=__QZ__;
var qzPick=new Array(QZ.length).fill(-1), qzCur=0, qzChecked=new Array(QZ.length).fill(false);
function qzBuildNav(){
  var nav=document.getElementById('qz-nav'); nav.innerHTML='';
  QZ.forEach(function(q,i){
    var item=document.createElement('div');
    item.className='qz-nav-item'+(i===qzCur?' active':'');
    var dotClass='qz-dot';
    if(qzChecked[i]){dotClass='qz-dot '+(qzPick[i]===q.ans?'correct':'wrong');}
    else if(qzPick[i]>=0){dotClass='qz-dot answered';}
    item.innerHTML='<div class="'+dotClass+'"></div>Question '+(i+1);
    item.onclick=function(){qzCur=i;qzBuildNav();qzShowQ();};
    nav.appendChild(item);
  });
}
function qzShowQ(){
  var q=QZ[qzCur], main=document.getElementById('qz-main');
  var html='<div class="qz-q">'+(qzCur+1)+'. '+q.q+'</div><div class="qz-opts">';
  q.opts.forEach(function(o,oi){
    var cls='qz-opt';
    if(qzChecked[qzCur]){
      cls+=' locked';
      if(oi===q.ans) cls+=' right';
      else if(oi===qzPick[qzCur]) cls+=' wrong-pick';
    } else if(oi===qzPick[qzCur]) cls+=' selected';
    html+='<div class="'+cls+'" onclick="qzSelect('+oi+')"><div class="qz-radio"></div><div>'+o+'</div></div>';
  });
  html+='</div>';
  if(qzChecked[qzCur]){
    var ok=qzPick[qzCur]===q.ans;
    html+='<div class="qz-fb show '+(ok?'ok':'no')+'">'+(ok?'&#10003; Correct. ':'&#10007; Incorrect. ')+q.fb+'</div>';
  } else {
    html+='<button class="qz-grade-btn" style="margin-top:14px;width:auto;padding:10px 24px" '+(qzPick[qzCur]<0?'disabled':'')+' onclick="qzCheck()">Check</button>';
  }
  main.innerHTML=html;
}
function qzSelect(oi){ if(qzChecked[qzCur]) return; qzPick[qzCur]=oi; qzBuildNav(); qzShowQ(); }
function qzCheck(){ qzChecked[qzCur]=true; qzBuildNav(); qzShowQ(); }
qzBuildNav(); qzShowQ();
</script>"""


class Notebook:
    def __init__(self, language="python"):
        self.cells, self.language = [], language

    def slide(self, s):
        self.cells.append(("md-sandbox", s.render() if isinstance(s, Slide) else s))
        return self

    def md(self, text):
        self.cells.append(("md", text))
        return self

    def sandbox(self, text):
        self.cells.append(("md-sandbox", text))
        return self

    def py(self, code):
        self.cells.append(("python", code.strip("\n")))
        return self

    def sql(self, code):
        self.cells.append(("sql", code.strip("\n")))
        return self

    def run(self, path):
        self.cells.append(("run", path))
        return self

    def source(self):
        out = ["# Databricks notebook source"]
        for i, (kind, body) in enumerate(self.cells):
            if i:
                out.append("\n# COMMAND ----------\n")
            if kind == "python":
                out.append(body)
            else:
                header = {"md": "%md", "md-sandbox": "%md-sandbox", "sql": "%sql", "run": f"%run {body}"}[kind]
                lines = [header] + ([] if kind == "run" else body.split("\n"))
                out.append("\n".join(("# MAGIC " + l) if l else "# MAGIC" for l in lines))
        return "\n".join(out) + "\n"

    def write(self, path):
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(self.source())
        return path
