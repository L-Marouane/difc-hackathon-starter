# Databricks notebook source
# MAGIC %md
# MAGIC # Falak data generator (shared code)
# MAGIC Do not run this notebook directly. `00_Setup_Data` and `02_New_Data_Drop` call it with `%run`.
# MAGIC
# MAGIC Falak is a fictional Dubai startup: SaaS invoicing and payment links for SMEs across the GCC.
# MAGIC The generator simulates every customer month by month (signups, plan changes, churn, invoices,
# MAGIC product usage, support tickets, marketing spend) and writes raw files the way real source systems would.

# COMMAND ----------

import json
import os

import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2024-01-01")
DATA_END = pd.Timestamp("2026-10-31 23:59:59")   # batch 1 cut-off
DROP_END = pd.Timestamp("2026-11-04 23:59:59")   # batch 2 (new data drop) cut-off
SIM_END = pd.Timestamp("2027-01-31")             # simulate beyond the cut-off so "future churners" leave signals today
N_CUSTOMERS = 4000

COUNTRIES = {
    # country: (weight, cities, currency, utc offset)
    "United Arab Emirates": (0.55, {"Dubai": 0.6, "Abu Dhabi": 0.25, "Sharjah": 0.15}, "AED", "+04:00"),
    "Saudi Arabia": (0.28, {"Riyadh": 0.55, "Jeddah": 0.3, "Dammam": 0.15}, "SAR", "+03:00"),
    "Qatar": (0.06, {"Doha": 1.0}, "USD", "+03:00"),
    "Bahrain": (0.04, {"Manama": 1.0}, "USD", "+03:00"),
    "Oman": (0.04, {"Muscat": 1.0}, "USD", "+04:00"),
    "Kuwait": (0.03, {"Kuwait City": 1.0}, "USD", "+03:00"),
}
COUNTRY_VARIANTS = {
    "United Arab Emirates": ["United Arab Emirates", "UAE", "U.A.E.", "AE", "uae"],
    "Saudi Arabia": ["Saudi Arabia", "KSA", "SA", "Kingdom of Saudi Arabia"],
    "Qatar": ["Qatar", "QA"],
    "Bahrain": ["Bahrain", "BH"],
    "Oman": ["Oman", "OM"],
    "Kuwait": ["Kuwait", "KW"],
}
KSA_LAUNCH = pd.Timestamp("2024-09-01")

INDUSTRIES = {"Retail": 0.2, "Food & Beverage": 0.16, "Professional Services": 0.18, "Logistics": 0.1,
              "Healthcare": 0.08, "Construction": 0.1, "E-commerce": 0.12, "Education": 0.06}
SIZES = {"1-10": 0.45, "11-50": 0.35, "51-200": 0.15, "201+": 0.05}
SEAT_RANGE = {"1-10": (1, 4), "11-50": (3, 12), "51-200": (8, 35), "201+": (20, 80)}
CHANNELS = {"Paid Social": 0.30, "Google Ads": 0.22, "Organic": 0.18, "Referral": 0.12, "Partner Bank": 0.10, "Events": 0.08}
MARKETING_CHANNEL_CODE = {"Paid Social": "paid_social", "Google Ads": "google_ads", "Organic": "seo_content",
                          "Referral": "referral_program", "Partner Bank": "bank_partnership", "Events": "events"}
CAC_TARGET_AED = {"Paid Social": 5600, "Google Ads": 4400, "Referral": 1500, "Partner Bank": 6000, "Events": 7500}
LEADS_PER_SIGNUP = {"Paid Social": 12.0, "Google Ads": 4.0, "Organic": 3.0, "Referral": 1.6, "Partner Bank": 1.8, "Events": 5.0}

PLAN_BY_SIZE = {"1-10": [0.75, 0.23, 0.02], "11-50": [0.35, 0.55, 0.10], "51-200": [0.10, 0.50, 0.40], "201+": [0.0, 0.30, 0.70]}
PLANS = ["Starter", "Growth", "Scale"]
PLAN_PRICE = {  # base price, included seats, extra seat price, per currency
    "AED": {"Starter": (149, 2, 39), "Growth": (449, 5, 35), "Scale": (1499, 15, 29)},
    "SAR": {"Starter": (149, 2, 39), "Growth": (449, 5, 35), "Scale": (1499, 15, 29)},
    "USD": {"Starter": (39, 2, 10), "Growth": (119, 5, 9), "Scale": (399, 15, 8)},
}

CHURN_BASE = 0.03
CHURN_CHANNEL = {"Paid Social": 2.3, "Google Ads": 1.25, "Organic": 1.0, "Referral": 0.8, "Events": 0.85, "Partner Bank": 0.6}
CHURN_SIZE = {"1-10": 1.3, "11-50": 1.0, "51-200": 0.75, "201+": 0.6}
CHURN_PLAN = {"Starter": 1.2, "Growth": 1.0, "Scale": 0.75}
ACTIVATION_P = {"Partner Bank": 0.68, "Referral": 0.58, "Events": 0.52, "Organic": 0.46, "Google Ads": 0.36, "Paid Social": 0.2}
INTEGRATIONS = ["Xero", "QuickBooks", "Zoho Books", "Odoo", "Shopify"]

# KSA card-payment gateway incident: failed payment links for a subset of KSA card customers
INCIDENT_START, INCIDENT_END = pd.Timestamp("2026-06-08"), pd.Timestamp("2026-07-27")
INCIDENT_CHURN_MONTHS = {"2026-08", "2026-09"}

ACCOUNT_MANAGERS = {
    "United Arab Emirates": ["Layla Mansour", "Karim Aziz", "Sara Al Hashimi", "Yousef Nasser"],
    "Saudi Arabia": ["Faisal Al Otaibi", "Noura Al Qahtani", "Hana Qureshi"],
    "OTHER": ["Rami Khoury", "Dina Saleh"],
}
NAME_A = ["Al Noor", "Rimal", "Sahra", "Marina", "Golden Palm", "Desert Rose", "Blue Dhow", "Falcon", "Oasis", "Najma",
          "Zaitoun", "Bayt", "Sanad", "Qamar", "Wadi", "Lulu Bay", "Saffron", "Corniche", "Atlas", "Majlis", "Medina",
          "Jumeirah", "Hijaz", "Dunes", "Pearl", "Cedar", "Amber", "Silk Route", "Sidra", "Areej", "Tamr", "Noon Star"]
NAME_B = {"Retail": ["Trading", "Stores", "Boutique", "General Trading"], "Food & Beverage": ["Cafe", "Kitchen", "Catering", "Bakery"],
          "Professional Services": ["Consulting", "Advisory", "Legal", "Partners"], "Logistics": ["Logistics", "Freight", "Couriers", "Cargo"],
          "Healthcare": ["Clinic", "Medical Centre", "Dental", "Pharmacy"], "Construction": ["Contracting", "Builders", "Interiors", "Engineering"],
          "E-commerce": ["Online", "Marketplace", "Shop", "Direct"], "Education": ["Academy", "Learning", "Tutors", "Training Institute"]}
NAME_SUFFIX = ["LLC", "FZ-LLC", "FZE", "Co.", "Est.", "", "", "L.L.C"]

HERO_ID = "C-01842"


def _pick(rng, d, n=None):
    keys = list(d.keys())
    p = np.array(list(d.values()), dtype=float)
    return rng.choice(keys, size=n, p=p / p.sum())


def _month_start(ts):
    return pd.Timestamp(year=ts.year, month=ts.month, day=1)


def _fmt_ts(ts, offset):
    return ts.strftime("%Y-%m-%dT%H:%M:%S") + offset

# COMMAND ----------

def simulate(seed=SEED):
    """Simulate Falak's whole world up to SIM_END. Returns a dict of DataFrames with an 'event time' column
    so each batch can slice what had happened by its cut-off."""
    rng = np.random.default_rng(seed)

    # ---------------- customers ----------------
    months = pd.date_range(START, _month_start(DROP_END), freq="MS")
    month_w = np.array([1 + 0.07 * i for i in range(len(months))])
    month_w[-1] *= DROP_END.day / 30  # the drop month only has a few days
    signup_month = rng.choice(months, size=N_CUSTOMERS, p=month_w / month_w.sum())
    customers = []
    used_names = set()
    for i in range(N_CUSTOMERS):
        sm = pd.Timestamp(signup_month[i])
        days_in_month = DROP_END.day if sm == _month_start(DROP_END) else (sm + pd.offsets.MonthEnd(0)).day
        signup = sm + pd.Timedelta(days=int(rng.integers(0, days_in_month)), hours=int(rng.integers(8, 20)),
                                   minutes=int(rng.integers(0, 60)))
        cw = {k: v[0] for k, v in COUNTRIES.items()}
        if signup < KSA_LAUNCH:
            cw["Saudi Arabia"] = 0.0
        else:
            cw["Saudi Arabia"] = 0.36  # KSA becomes the growth market after launch
        country = _pick(rng, cw)
        city = _pick(rng, COUNTRIES[country][1])
        industry = _pick(rng, INDUSTRIES)
        size = _pick(rng, SIZES)
        chw = dict(CHANNELS)
        if signup >= pd.Timestamp("2025-06-01"):  # growth push: paid social budget doubled
            chw["Paid Social"] = 0.42
        channel = _pick(rng, chw)
        for _ in range(20):
            name = f"{rng.choice(NAME_A)} {rng.choice(NAME_B[industry])} {rng.choice(NAME_SUFFIX)}".strip()
            if name not in used_names:
                break
            name = f"{name} {int(rng.integers(2, 99))}"
        used_names.add(name)
        am_pool = ACCOUNT_MANAGERS.get(country, ACCOUNT_MANAGERS["OTHER"])
        customers.append(dict(customer_id=f"C-{i + 1:05d}", company_name=name, industry=industry, country=country,
                              city=city, company_size=size, acquisition_channel=channel, signup_ts=signup,
                              account_manager=str(rng.choice(am_pool)), currency=COUNTRIES[country][2],
                              utc_offset=COUNTRIES[country][3], is_test=False))
    cust = pd.DataFrame(customers)

    # hero account: big, healthy KSA logistics customer hit by the payment incident, now quietly at risk
    h = cust.index[cust.customer_id == HERO_ID][0]
    cust.loc[h, ["company_name", "industry", "country", "city", "company_size", "acquisition_channel", "signup_ts",
                 "account_manager", "currency", "utc_offset"]] = [
        "Rimal Logistics Co.", "Logistics", "Saudi Arabia", "Riyadh", "201+", "Partner Bank",
        pd.Timestamp("2025-02-11 10:24:00"), "Faisal Al Otaibi", "SAR", "+03:00"]

    # activation = connected an accounting/e-commerce integration within 14 days of signup
    act_p = cust.acquisition_channel.map(ACTIVATION_P) + cust.company_size.map({"1-10": -0.05, "11-50": 0, "51-200": 0.08, "201+": 0.12})
    cust["activated"] = rng.random(len(cust)) < act_p.clip(0.05, 0.95)
    cust.loc[h, "activated"] = True
    cust["integration_day"] = np.where(cust.activated, rng.integers(0, 14, len(cust)),
                                       np.where(rng.random(len(cust)) < 0.3, rng.integers(20, 120, len(cust)), -1))
    cust["integration"] = rng.choice(INTEGRATIONS, size=len(cust), p=[0.3, 0.2, 0.2, 0.15, 0.15])
    cust["billing_cycle"] = np.where(rng.random(len(cust)) < 0.2, "annual", "monthly")
    cust.loc[h, "billing_cycle"] = "monthly"
    cust["payment_method"] = rng.choice(["card", "bank_transfer", "direct_debit"], size=len(cust), p=[0.6, 0.25, 0.15])
    cust.loc[h, "payment_method"] = "card"
    cust["incident_affected"] = (cust.country == "Saudi Arabia") & (cust.payment_method == "card") & (rng.random(len(cust)) < 0.5)
    cust.loc[h, "incident_affected"] = True

    # ---------------- subscription lifecycle (monthly simulation) ----------------
    sub_events, spans = [], []  # spans = active periods per customer
    for r in cust.itertuples():
        size_lo, size_hi = SEAT_RANGE[r.company_size]
        seats = int(rng.integers(size_lo, size_hi + 1))
        plan = rng.choice(PLANS, p=PLAN_BY_SIZE[r.company_size])
        if r.customer_id == HERO_ID:
            plan, seats = "Scale", 140
        cur = r.currency

        def mrr(plan_, seats_):
            base, incl, extra = PLAN_PRICE[cur][plan_]
            v = base + max(0, seats_ - incl) * extra
            return round(v * (0.85 if r.billing_cycle == "annual" else 1.0), 2)

        def emit(ts, etype, plan_, seats_):
            sub_events.append(dict(customer_id=r.customer_id, effective_ts=ts, event_type=etype, plan=plan_, seats=seats_,
                                   mrr=mrr(plan_, seats_) if etype != "churn" else 0.0, currency=cur,
                                   billing_cycle=r.billing_cycle))

        emit(r.signup_ts, "new", plan, seats)
        active, span_start, age = True, r.signup_ts, 0
        m = _month_start(r.signup_ts) + pd.offsets.MonthBegin(1)
        churn_dates = []
        while m <= SIM_END:
            age += 1
            ym = m.strftime("%Y-%m")
            if active:
                hz = CHURN_BASE * CHURN_CHANNEL[r.acquisition_channel] * CHURN_SIZE[r.company_size] * CHURN_PLAN[plan]
                hz *= 0.4 if r.activated else 1.45
                hz *= 1.4 if age <= 3 else (0.8 if age > 12 else 1.0)
                if r.incident_affected and ym in INCIDENT_CHURN_MONTHS:
                    hz *= 5.0
                if r.billing_cycle == "annual":
                    hz = (1 - (1 - hz) ** 12) * 0.6 if age % 12 == 0 else 0.0
                if r.customer_id == HERO_ID:
                    hz = 1.0 if ym == "2026-12" else 0.0  # planned: leaves in December unless someone acts
                if rng.random() < hz:
                    ts = m + pd.Timedelta(days=int(rng.integers(0, 27)), hours=int(rng.integers(8, 20)))
                    emit(ts, "churn", plan, seats)
                    churn_dates.append(ts)
                    spans.append((r.customer_id, span_start, ts))
                    active = False
                else:
                    u = rng.random()
                    up_p = 0.012 * (2.0 if r.activated else 1.0) * (1.5 if r.acquisition_channel == "Partner Bank" else 1.0)
                    down_p = 0.006 * (2.5 if r.incident_affected and ym in {"2026-07", "2026-08", "2026-09"} else 1.0)
                    ts = m + pd.Timedelta(days=int(rng.integers(0, 27)), hours=int(rng.integers(8, 20)))
                    if r.customer_id == HERO_ID:
                        pass
                    elif u < up_p and plan != "Scale":
                        plan = PLANS[PLANS.index(plan) + 1]
                        emit(ts, "upgrade", plan, seats)
                    elif u < up_p + down_p and plan != "Starter":
                        plan = PLANS[PLANS.index(plan) - 1]
                        emit(ts, "downgrade", plan, seats)
                    elif u < up_p + down_p + 0.03 * (1.5 if r.activated else 1.0):
                        seats = seats + int(rng.integers(1, 5))
                        emit(ts, "seat_change", plan, seats)
                    elif u < up_p + down_p + 0.03 * (1.5 if r.activated else 1.0) + 0.008 and seats > 1:
                        seats = max(1, seats - int(rng.integers(1, 3)))
                        emit(ts, "seat_change", plan, seats)
            else:
                if rng.random() < 0.025 and r.customer_id != HERO_ID:  # win-back
                    ts = m + pd.Timedelta(days=int(rng.integers(0, 27)), hours=int(rng.integers(8, 20)))
                    emit(ts, "reactivation", plan, seats)
                    active, span_start = True, ts
            m = m + pd.offsets.MonthBegin(1)
        if active:
            spans.append((r.customer_id, span_start, SIM_END))
        cust.loc[cust.customer_id == r.customer_id, "first_churn_ts"] = churn_dates[0] if churn_dates else pd.NaT

    subs = pd.DataFrame(sub_events).sort_values("effective_ts").reset_index(drop=True)
    spans = pd.DataFrame(spans, columns=["customer_id", "span_start", "span_end"])
    # next churn after any timestamp (for usage decay and failed payments before churn)
    churns = subs[subs.event_type == "churn"][["customer_id", "effective_ts"]]
    churn_map = churns.groupby("customer_id").effective_ts.apply(lambda s: np.sort(s.values)).to_dict()

    def days_to_next_churn(cid, ts_arr):
        c = churn_map.get(cid)
        out = np.full(len(ts_arr), 9999.0)
        if c is None:
            return out
        idx = np.searchsorted(c, ts_arr)
        ok = idx < len(c)
        out[ok] = (c[idx[ok]] - ts_arr[ok]) / np.timedelta64(1, "D")
        return out

    cust_i = cust.set_index("customer_id")

    # state lookup: plan/mrr/seats in force at a timestamp
    subs_by_c = {cid: g for cid, g in subs.groupby("customer_id")}

    def state_at(cid, ts_arr):
        g = subs_by_c[cid]
        idx = np.searchsorted(g.effective_ts.values, ts_arr, side="right") - 1
        idx = np.clip(idx, 0, len(g) - 1)
        return g.plan.values[idx], g.mrr.values[idx], g.seats.values[idx]

    # ---------------- invoices ----------------
    inv = []
    for s in spans.itertuples():
        c = cust_i.loc[s.customer_id]
        step = 12 if c.billing_cycle == "annual" else 1
        anchor_day = min(c.signup_ts.day, 28)
        d = pd.Timestamp(year=s.span_start.year, month=s.span_start.month, day=anchor_day)
        if d < s.span_start.normalize():
            d = d + pd.DateOffset(months=0)
        dates = []
        while d < s.span_end and d <= SIM_END:
            if d >= s.span_start.normalize():
                dates.append(d)
            d = d + pd.DateOffset(months=step)
        if not dates:
            continue
        dates = pd.DatetimeIndex(dates)
        plans_, mrrs, _ = state_at(s.customer_id, dates.values)
        dtc = days_to_next_churn(s.customer_id, dates.values)
        for dt_, p_, m_, dc in zip(dates, plans_, mrrs, dtc):
            p_fail = 0.025
            if dc < 75:
                p_fail = 0.32
            if c.incident_affected and INCIDENT_START <= dt_ <= INCIDENT_END:
                p_fail = 0.55
            if s.customer_id == HERO_ID and pd.Timestamp("2026-06-01") <= dt_ <= pd.Timestamp("2026-09-30"):
                p_fail = 1.0 if dt_.month in (6, 7, 9, 10) else 0.0
            amount = m_ * (12 if c.billing_cycle == "annual" else 1)
            u = rng.random()
            if u < p_fail:
                recovered = rng.random() < 0.45 and s.customer_id != HERO_ID
                status = "paid" if recovered else "failed"
                attempts = int(rng.integers(2, 4))
                paid = dt_ + pd.Timedelta(days=int(rng.integers(3, 12))) if recovered else pd.NaT
            elif c.payment_method == "bank_transfer" and rng.random() < 0.15:
                status, attempts = "overdue", 1
                paid = dt_ + pd.Timedelta(days=int(rng.integers(20, 50)))
            elif rng.random() < 0.004:
                status, attempts, paid = "refunded", 1, dt_ + pd.Timedelta(days=1)
            else:
                status, attempts, paid = "paid", 1, dt_ + pd.Timedelta(hours=int(rng.integers(0, 72)))
            inv.append(dict(customer_id=s.customer_id, issue_ts=dt_ + pd.Timedelta(hours=6), plan=p_, amount=round(amount, 2),
                            currency=c.currency, status=status, attempts=attempts, paid_ts=paid,
                            payment_method=c.payment_method))
    inv = pd.DataFrame(inv).sort_values("issue_ts").reset_index(drop=True)
    inv["invoice_id"] = [f"INV-{i + 100001}" for i in range(len(inv))]

    # ---------------- product usage events ----------------
    base_rate = {"1-10": 1.8, "11-50": 4.0, "51-200": 8.0, "201+": 16.0}
    plan_f = {"Starter": 0.8, "Growth": 1.0, "Scale": 1.3}
    mix_names = np.array(["login", "invoice_created", "payment_link_sent", "payment_received", "report_exported",
                          "integration_sync", "team_member_invited"])
    mix_p = np.array([0.33, 0.25, 0.15, 0.13, 0.06, 0.06, 0.02])
    ev_parts = []
    for s in spans.itertuples():
        c = cust_i.loc[s.customer_id]
        end = min(s.span_end, DROP_END)
        if end <= s.span_start:
            continue
        weeks = pd.date_range(s.span_start.normalize(), end, freq="7D")
        if len(weeks) == 0:
            continue
        wv = weeks.values
        plans_, _, seats_ = state_at(s.customer_id, wv)
        dtc = days_to_next_churn(s.customer_id, wv)
        rate = base_rate[c.company_size] * np.vectorize(plan_f.get)(plans_) * (1.6 if c.activated else 0.8)
        decay = np.where(dtc < 70, np.clip(dtc / 70, 0.08, 1) ** 1.3, 1.0)
        rate = rate * decay
        age_w = (wv - wv[0]) / np.timedelta64(7, "D")
        rate = rate * np.where(age_w < 2, 1.5, 1.0)
        if s.customer_id == HERO_ID:  # usage falls off a cliff after the incident
            rate = rate * np.select([wv >= np.datetime64("2026-10-01"), wv >= np.datetime64("2026-09-01"), wv >= np.datetime64("2026-08-01")],
                                    [0.2, 0.45, 0.6], 1.0)
        counts = rng.poisson(rate)
        wk = np.repeat(wv, counts)
        seat_rep = np.repeat(seats_, counts)
        offs = rng.random(len(wk)) * 7 * 24 * 3600
        ts = wk + (offs * 1e9).astype("timedelta64[ns]")
        keep = (ts >= np.datetime64(s.span_start)) & (ts < np.datetime64(end))
        ts, seat_rep = ts[keep], seat_rep[keep]
        n = len(ts)
        if n == 0:
            continue
        names = rng.choice(mix_names, size=n, p=mix_p)
        if c.incident_affected:
            inc = (ts >= np.datetime64(INCIDENT_START)) & (ts <= np.datetime64(INCIDENT_END)) & (names == "payment_link_sent")
            names = np.where(inc & (rng.random(n) < 0.6), "payment_link_failed", names)
        user_n = (rng.random(n) * np.maximum(seat_rep, 1)).astype(int) + 1
        ev_parts.append(pd.DataFrame(dict(customer_id=s.customer_id, ts=ts, event_name=names, user_n=user_n)))
        if c.integration_day >= 0 and s.span_start == c.signup_ts:
            its = c.signup_ts + pd.Timedelta(days=int(c.integration_day), hours=int(rng.integers(1, 8)))
            if its < end:
                ev_parts.append(pd.DataFrame(dict(customer_id=[s.customer_id], ts=[its], event_name=["integration_connected"], user_n=[1])))
    ev = pd.concat(ev_parts, ignore_index=True).sort_values("ts").reset_index(drop=True)

    # ---------------- support tickets ----------------
    tk = []
    for s in spans.itertuples():
        c = cust_i.loc[s.customer_id]
        end = min(s.span_end, DROP_END)
        ms = pd.date_range(_month_start(s.span_start), end, freq="MS")
        if len(ms) == 0:
            continue
        dtc = days_to_next_churn(s.customer_id, ms.values)
        _, _, seats_ = state_at(s.customer_id, ms.values)
        for mi, (m, dc, st) in enumerate(zip(ms, dtc, seats_)):
            lam = 0.06 * (1 + st / 30)
            topics = {"how_to": 1.0, "integration_sync": 0.9 if c.activated else 0.3, "billing_question": 0.7,
                      "feature_request": 0.6, "e_invoicing": 0.4, "payment_failure": 0.3}
            if mi < 2:
                lam += 0.12
                topics["onboarding"] = 3.0
            if c.country == "United Arab Emirates" and pd.Timestamp("2026-03-01") <= m <= pd.Timestamp("2026-09-30"):
                topics["e_invoicing"] = 2.5  # UAE e-invoicing mandate approaching
                lam += 0.04
            if c.country == "Saudi Arabia":
                topics["e_invoicing"] = 1.0  # ZATCA phase 2
            if dc < 60:
                lam *= 2.5
                topics["cancellation"] = 1.5
                topics["billing_question"] = 1.5
            if c.incident_affected and pd.Timestamp("2026-06-01") <= m <= pd.Timestamp("2026-08-01"):
                lam += 0.7
                topics["payment_failure"] = 8.0
            k = rng.poisson(lam)
            if s.customer_id == HERO_ID:
                k = {"2026-06": 1, "2026-07": 2, "2026-08": 1, "2026-09": 1, "2026-10": 1}.get(m.strftime("%Y-%m"), 0)
            for j in range(k):
                ts = m + pd.Timedelta(seconds=int(rng.integers(0, 27 * 86400)))
                if ts < s.span_start or ts > end:
                    continue
                topic = _pick(rng, topics)
                if s.customer_id == HERO_ID:
                    topic = "cancellation" if m.strftime("%Y-%m") == "2026-10" else "payment_failure"
                    ts = m + pd.Timedelta(days=4 + 9 * j, hours=10)
                tk.append(dict(customer_id=s.customer_id, created_ts=ts, topic=topic))
    tk = pd.DataFrame(tk).sort_values("created_ts").reset_index(drop=True)
    tk["ticket_id"] = [f"T-{i + 200001}" for i in range(len(tk))]

    return dict(customers=cust, subs=subs, invoices=inv, events=ev, tickets=tk, rng=rng)

# COMMAND ----------

TEMPLATES = {
    "onboarding": [
        ("How do I import my customers from Excel?", "Hi, we just signed up for {company}. We have around {n} customers in an Excel sheet. Is there a way to import them in one go instead of typing them one by one?"),
        ("Help setting up our first invoice template", "We are new to Falak. How do I add our logo, TRN number and bank details to the invoice template?"),
        ("Adding my team", "I want to invite {n} colleagues from the finance team. Where do I set their permissions so they cannot delete invoices?"),
        ("كيف أضيف شعار الشركة على الفاتورة؟", "مرحبا، اشتركنا اليوم ونريد إضافة شعار الشركة والرقم الضريبي على الفواتير. كيف نفعل ذلك؟"),
    ],
    "how_to": [
        ("Recurring invoices", "Can I set up a recurring monthly invoice for a retainer client? I could not find the option."),
        ("Partial payments", "A client paid {amount} {currency} out of a larger invoice. How do I record a partial payment?"),
        ("Exporting VAT report", "Where can I export the VAT summary for last quarter for my accountant?"),
        ("Credit note", "How do I issue a credit note against invoice {inv}?"),
    ],
    "integration_sync": [
        ("{integration} sync duplicated invoices", "Since yesterday every invoice we create in Falak appears twice in {integration}. Our accountant is not happy. Please check."),
        ("{integration} connection keeps dropping", "The {integration} integration disconnects every few days and we have to reconnect it manually."),
        ("Payments not showing in {integration}", "Payments received through Falak links are not reconciled in {integration}. We have {n} unmatched payments this month."),
    ],
    "billing_question": [
        ("Charged twice this month", "We see two charges of {amount} {currency} on our card for the Falak subscription this month. Please refund one."),
        ("Question about extra seats", "Why did our bill go up? We did not add any users as far as I know."),
        ("Need a tax invoice for our subscription", "Our finance team needs a proper tax invoice for the Falak subscription with our TRN."),
        ("Can we switch to annual billing?", "We would like to move to annual billing if there is a discount."),
    ],
    "feature_request": [
        ("Arabic invoice template", "Many of our clients prefer bilingual Arabic and English invoices. Is that on the roadmap?"),
        ("WhatsApp payment reminders", "It would be great if payment reminders could go out on WhatsApp, our clients ignore emails."),
        ("Multi-currency on one account", "We bill clients in AED and USD. Can one account handle both currencies?"),
        ("طلب ميزة: تذكير الدفع عبر واتساب", "نتمنى إضافة إرسال تذكير الدفع للعملاء عبر واتساب بدلا من البريد الإلكتروني."),
    ],
    "e_invoicing": [
        ("Is Falak ready for UAE e-invoicing?", "Our auditor told us e-invoicing becomes mandatory soon in the UAE. Will Falak support the Peppol format and when?"),
        ("ZATCA phase 2 integration", "We received a ZATCA notification for phase 2 integration. Does Falak generate the compliant XML and QR code?"),
        ("E-invoice rejected", "One of our e-invoices was rejected by the tax portal with a validation error on the buyer TRN field."),
        ("الربط مع منصة فاتورة", "هل يدعم فلك المرحلة الثانية من الفوترة الإلكترونية والربط مع هيئة الزكاة والضريبة؟"),
    ],
    "payment_failure": [
        ("Payment link not working", "Our clients click the payment link and get an error after entering card details. This is the third complaint this week. We are losing money."),
        ("Customer card declined on payment link", "Several of our customers report their cards are declined on the Falak payment page but the same cards work elsewhere. Invoice {inv}."),
        ("Payments stuck in processing", "We have {n} payments showing processing for more than 3 days. Our clients say the money left their account."),
        ("رابط الدفع لا يعمل", "عملاؤنا لا يستطيعون الدفع عبر الرابط، تظهر رسالة خطأ بعد إدخال بيانات البطاقة. نحتاج حلا عاجلا."),
    ],
    "cancellation": [
        ("How do I cancel our subscription?", "Please let me know how to cancel. We are moving our invoicing to another tool."),
        ("Evaluating alternatives", "To be transparent, after the payment problems this summer management asked us to evaluate other providers. Can someone from your team call me?"),
        ("Downgrade or cancel", "We are not using Falak as much as we planned. What are our options to downgrade or cancel before the next renewal?"),
        ("إلغاء الاشتراك", "نرغب في إلغاء الاشتراك بنهاية الشهر. ما هي الإجراءات؟"),
    ],
}
AGENT_CATEGORY = {  # what support agents tag by hand, inconsistently
    "onboarding": ["Onboarding", "onboarding", "Setup"], "how_to": ["How-to", "Question", "how to"],
    "integration_sync": ["Integrations", "integration", "Xero/QB"], "billing_question": ["Billing", "billing ", "Invoice"],
    "feature_request": ["Feature Request", "feature", "Product"], "e_invoicing": ["Compliance", "e-invoice", "Tax"],
    "payment_failure": ["Payments", "payment issue", "Billing"], "cancellation": ["Churn Risk", "cancel", "Billing"],
}
PRIORITY = {"payment_failure": [0.05, 0.2, 0.45, 0.3], "cancellation": [0.1, 0.4, 0.4, 0.1], "integration_sync": [0.1, 0.45, 0.4, 0.05],
            "e_invoicing": [0.15, 0.5, 0.3, 0.05]}


def render_tickets(world, rng):
    cust_i = world["customers"].set_index("customer_id")
    rows = []
    for t in world["tickets"].itertuples():
        c = cust_i.loc[t.customer_id]
        variants = TEMPLATES[t.topic]
        arabic_p = 0.25 if c.country == "Saudi Arabia" else 0.08
        ar = [v for v in variants if not v[0].isascii()]
        en = [v for v in variants if v[0].isascii()]
        subj, body = (ar[0] if ar and rng.random() < arabic_p else en[int(rng.integers(0, len(en)))])
        if t.customer_id == HERO_ID:
            subj, body = ({"cancellation": TEMPLATES["cancellation"][1]}.get(t.topic) or TEMPLATES["payment_failure"][int(rng.integers(0, 3))])
        fill = dict(company=c.company_name, n=int(rng.integers(3, 400)), amount=int(rng.integers(150, 9000)), currency=c.currency,
                    inv=f"INV-{int(rng.integers(100001, 160000))}", integration=c.integration)
        subj, body = subj.format(**fill), body.format(**fill)
        prio = rng.choice(["low", "medium", "high", "urgent"], p=PRIORITY.get(t.topic, [0.35, 0.45, 0.17, 0.03]))
        resolve_h = float(rng.lognormal(2.6 if t.topic == "payment_failure" else 2.0, 0.9))
        if t.topic == "payment_failure" and INCIDENT_START <= t.created_ts <= INCIDENT_END:
            resolve_h *= 4  # support overwhelmed during the incident
        resolved = t.created_ts + pd.Timedelta(hours=resolve_h)
        if resolved > DROP_END - pd.Timedelta(days=1) and rng.random() < 0.7:
            status, resolved = rng.choice(["open", "pending"]), pd.NaT
        else:
            status = rng.choice(["resolved", "closed", "Resolved"])
        csat_mu = {"payment_failure": 2.1, "cancellation": 2.4, "integration_sync": 3.2}.get(t.topic, 4.1)
        csat = int(np.clip(round(rng.normal(csat_mu, 0.9)), 1, 5)) if (rng.random() < 0.45 and status != "open") else None
        rows.append(dict(ticket_id=t.ticket_id, customer_id=t.customer_id, created_ts=t.created_ts, channel=rng.choice(["email", "whatsapp", "in_app_chat"], p=[0.45, 0.35, 0.2]),
                         priority=prio, subject=subj, description=body, status=status, resolved_ts=resolved,
                         first_response_minutes=int(rng.lognormal(3.4 if t.created_ts.hour < 18 else 5.2, 0.7)),
                         csat_score=csat, agent_category=(rng.choice(AGENT_CATEGORY[t.topic]) if rng.random() < 0.4 else None)))
    return pd.DataFrame(rows)

# COMMAND ----------

def _iso(ts, offset="+04:00"):
    return None if pd.isna(ts) else _fmt_ts(pd.Timestamp(ts), offset)


def _messy_date(ts, rng):
    u = rng.random()
    if u < 0.7:
        return ts.strftime("%Y-%m-%d")
    if u < 0.9:
        return ts.strftime("%d/%m/%Y")
    return ts.strftime("%b %d, %Y")


def _write_jsonl(records, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps({k: v for k, v in r.items() if v is not None}, ensure_ascii=False, default=str) + "\n")


def _clean(v):
    if v is None:
        return None
    if isinstance(v, float) and np.isnan(v):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    return v


def write_batch(world, root, batch=1):
    """Write raw source files for a batch. batch 1 = history up to 2026-10-31, batch 2 = 1-4 Nov 2026 drop."""
    rng = np.random.default_rng(SEED + batch)
    lo = START - pd.Timedelta(days=1) if batch == 1 else DATA_END
    hi = DATA_END if batch == 1 else DROP_END
    tag = "2026-10-31" if batch == 1 else "2026-11-04"
    cust = world["customers"]
    off = cust.set_index("customer_id").utc_offset.to_dict()
    stats = {}

    # ---- CRM export (CSV): full snapshot in batch 1, only new + changed accounts in batch 2
    c = cust[(cust.signup_ts > lo) & (cust.signup_ts <= hi)].copy()
    if batch == 2:
        changed = cust[cust.signup_ts <= lo].sample(40, random_state=batch).copy()
        changed["account_manager"] = [rng.choice(ACCOUNT_MANAGERS.get(x, ACCOUNT_MANAGERS["OTHER"])) for x in changed.country]
        c = pd.concat([c, changed])
    out = pd.DataFrame({
        "customer_id": c.customer_id,
        "company_name": [n + (" " if rng.random() < 0.05 else "") for n in c.company_name],
        "industry": [None if rng.random() < 0.03 else x for x in c.industry],
        "country": [rng.choice(COUNTRY_VARIANTS[x]) for x in c.country],
        "city": c.city,
        "company_size": c.company_size,
        "acquisition_channel": c.acquisition_channel,
        "signup_date": [_messy_date(t, rng) for t in c.signup_ts],
        "account_manager": c.account_manager,
        "contact_email": [f"finance@{n.lower().split(' ')[0].replace('.', '')}{i}.ae" for i, n in zip(c.customer_id.str[-5:], c.company_name)],
        "last_modified": [(t + pd.Timedelta(days=int(rng.integers(0, 60)))).strftime("%Y-%m-%d %H:%M:%S") if batch == 1 else "2026-11-04 07:00:00" for t in c.signup_ts],
    })
    if batch == 1:
        dups = out.sample(frac=0.03, random_state=7).copy()  # re-exported rows with an older timestamp
        dups["last_modified"] = "2024-01-01 00:00:00"
        dups["account_manager"] = "Unassigned"
        tests = pd.DataFrame({"customer_id": [f"C-9{i:04d}" for i in range(12)], "company_name": [f"TEST ACCOUNT {i} - QA do not use" for i in range(12)],
                              "industry": "Retail", "country": "UAE", "city": "Dubai", "company_size": "1-10", "acquisition_channel": "Organic",
                              "signup_date": "2024-02-01", "account_manager": "QA Team", "contact_email": [f"qa{i}@falak.io" for i in range(12)],
                              "last_modified": "2024-02-01 00:00:00"})
        out = pd.concat([out, dups, tests]).sample(frac=1, random_state=3)
    p = f"{root}/crm/customers_export_{tag}.csv"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    out.to_csv(p, index=False)
    stats["crm/customers"] = len(out)

    # ---- billing: subscription events (JSON lines, nested plan object), one file per month
    s = world["subs"]
    s = s[(s.effective_ts > lo) & (s.effective_ts <= hi)]
    if batch == 1:
        tests = [dict(event_id=f"SE-T{i}", customer_id=f"C-9{i:04d}", event_type="new", effective_at="2024-02-01T09:00:00+04:00",
                      billing_cycle="monthly", plan={"name": "Scale", "seats": 99, "mrr": 0.0, "currency": "AED"}) for i in range(12)]
    else:
        tests = []
    n_sub = 0
    for ym, g in s.groupby(s.effective_ts.dt.strftime("%Y_%m")):
        recs = [dict(event_id=f"SE-{i:07d}", customer_id=r.customer_id, event_type=r.event_type,
                     effective_at=_iso(r.effective_ts, off[r.customer_id]), billing_cycle=r.billing_cycle,
                     plan={"name": r.plan, "seats": int(r.seats), "mrr": float(r.mrr), "currency": r.currency})
                for i, r in zip(g.index, g.itertuples())]
        if tests and ym == "2024_02":
            recs += tests
        _write_jsonl(recs, f"{root}/billing/subscription_events/subscription_events_{ym}.json")
        n_sub += len(recs)
    stats["billing/subscription_events"] = n_sub

    # ---- billing: invoices (JSON lines, status casing and amount type drift)
    iv = world["invoices"]
    iv = iv[(iv.issue_ts > lo) & (iv.issue_ts <= hi)]
    n_inv = 0
    for ym, g in iv.groupby(iv.issue_ts.dt.strftime("%Y_%m")):
        recs = []
        for r in g.itertuples():
            paid = r.paid_ts if (not pd.isna(r.paid_ts) and r.paid_ts <= hi) else None
            status = r.status
            if status in ("paid", "overdue") and paid is None:
                status = "overdue" if r.payment_method == "bank_transfer" else "pending"
            status = rng.choice([status, status.upper(), status.capitalize()], p=[0.8, 0.1, 0.1])
            amount = f"{r.amount:.2f}" if rng.random() < 0.05 else float(r.amount)
            recs.append(dict(invoice_id=r.invoice_id, customer_id=r.customer_id, issued_at=_iso(r.issue_ts, off[r.customer_id]),
                             due_date=(r.issue_ts + pd.Timedelta(days=14)).strftime("%Y-%m-%d"), plan=r.plan, amount=amount,
                             currency=r.currency, status=status, payment_attempts=int(r.attempts),
                             paid_at=_iso(paid, off[r.customer_id]) if paid is not None else None, payment_method=r.payment_method))
        _write_jsonl(recs, f"{root}/billing/invoices/invoices_{ym}.json")
        n_inv += len(recs)
    stats["billing/invoices"] = n_inv

    # ---- product events (JSON lines, nested context, mixed timestamp formats, ~1% duplicates)
    ev = world["events"]
    sel = (ev.ts > lo) & (ev.ts <= hi)
    if batch == 2:  # late-arriving October events show up in the new drop
        late = (ev.ts > DATA_END - pd.Timedelta(days=3)) & (ev.ts <= DATA_END)
        late_idx = ev[late].sample(frac=0.04, random_state=11).index
        sel = sel | ev.index.isin(late_idx)
    ev = ev[sel]
    ver_of = lambda t: f"3.{min(9, (t.year - 2024) * 4 + t.quarter)}.{t.month % 4}"
    n_ev = 0
    for ym, g in ev.groupby(ev.ts.dt.strftime("%Y_%m")):
        n = len(g)
        plat = rng.choice(["web", "ios", "android"], size=n, p=[0.6, 0.25, 0.15])
        loc = rng.random(n)
        naive = rng.random(n) < 0.04
        dup = rng.random(n) < 0.01
        integ = cust.set_index("customer_id").integration
        recs = []
        for k, r in enumerate(g.itertuples()):
            t = pd.Timestamp(r.ts)
            props = None
            if r.event_name in ("invoice_created", "payment_received"):
                props = {"amount": round(float(rng.lognormal(7.3, 0.9)), 2)}
            elif r.event_name == "integration_connected":
                props = {"integration": integ[r.customer_id]}
            elif r.event_name == "payment_link_failed":
                props = {"error_code": rng.choice(["GATEWAY_TIMEOUT", "3DS_FAILED", "ACQUIRER_DECLINED"], p=[0.5, 0.3, 0.2])}
            elif r.event_name == "report_exported":
                props = {"report": rng.choice(["vat_summary", "aging", "cash_flow", "sales_by_client"])}
            rec = dict(event_id=f"EV-{r.Index:08d}", event_ts=t.strftime("%Y-%m-%d %H:%M:%S") if naive[k] else _iso(t, off[r.customer_id]),
                       customer_id=r.customer_id, user_id=f"U{r.customer_id[2:]}-{r.user_n:02d}", event_name=r.event_name,
                       context={"platform": str(plat[k]), "app_version": ver_of(t), "locale": "ar" if loc[k] < (0.25 if off[r.customer_id] == "+03:00" else 0.1) else "en"},
                       properties=props)
            recs.append(rec)
            if dup[k]:
                recs.append(rec)
        suffix = "" if batch == 1 else "_drop_2026-11-04"
        _write_jsonl(recs, f"{root}/product_events/events_{ym}{suffix}.json")
        n_ev += len(recs)
    stats["product_events"] = n_ev

    # ---- support tickets (JSON lines with free text, English and Arabic)
    tk = world["tickets_rendered"]
    tk = tk[(tk.created_ts > lo) & (tk.created_ts <= hi)]
    n_tk = 0
    for ym, g in tk.groupby(tk.created_ts.dt.strftime("%Y_%m")):
        recs = []
        for r in g.itertuples():
            rr = r.resolved_ts if (not pd.isna(r.resolved_ts) and r.resolved_ts <= hi) else None
            st = r.status if rr is not None or r.status in ("open", "pending") else "open"
            recs.append(dict(ticket_id=r.ticket_id, customer_id=r.customer_id, created_at=_iso(r.created_ts, off[r.customer_id]),
                             channel=r.channel, priority=r.priority, subject=r.subject, description=r.description, status=st,
                             resolved_at=_iso(rr, off[r.customer_id]) if rr is not None else None,
                             first_response_minutes=r.first_response_minutes, csat_score=_clean(r.csat_score), agent_category=r.agent_category))
        _write_jsonl(recs, f"{root}/support/tickets/tickets_{ym}.json")
        n_tk += len(recs)
    stats["support/tickets"] = n_tk

    # ---- marketing spend (CSV, channel codes differ from CRM labels) + FX rates
    if batch == 1:
        cu = cust[(cust.signup_ts <= DATA_END) & (~cust.is_test)]
        sign = cu.groupby([cu.signup_ts.dt.to_period("M"), "acquisition_channel"]).size().rename("signups").reset_index()
        rows = []
        for r in sign.itertuples():
            ch = r.acquisition_channel
            if ch == "Organic":
                spend = 32000 + rng.normal(0, 2500)  # content team + SEO tooling
            else:
                spend = r.signups * CAC_TARGET_AED[ch] * rng.lognormal(0, 0.12)
            clicks = int(spend / rng.uniform(2.5, 6)) if ch in ("Paid Social", "Google Ads") else None
            rows.append(dict(month=r.signup_ts.strftime("%Y-%m"), channel=MARKETING_CHANNEL_CODE[ch], spend_aed=round(spend, 2),
                             impressions=clicks * int(rng.integers(40, 90)) if clicks else None, clicks=clicks,
                             leads=int(r.signups * LEADS_PER_SIGNUP[ch] * rng.uniform(0.85, 1.15))))
        mk = pd.DataFrame(rows).sort_values(["month", "channel"])
        os.makedirs(f"{root}/marketing", exist_ok=True)
        mk.to_csv(f"{root}/marketing/marketing_spend_monthly.csv", index=False)
        stats["marketing/spend"] = len(mk)
        fx = [dict(month=m.strftime("%Y-%m"), currency=cur, rate_to_aed=rate)
              for m in pd.date_range(START, DROP_END, freq="MS")
              for cur, rate in [("AED", 1.0), ("SAR", round(0.9793 + float(rng.normal(0, 0.0004)), 4)), ("USD", 3.6725)]]
        os.makedirs(f"{root}/reference", exist_ok=True)
        pd.DataFrame(fx).to_csv(f"{root}/reference/fx_rates_monthly.csv", index=False)
        stats["reference/fx_rates"] = len(fx)
    return stats


def build_world(seed=SEED):
    world = simulate(seed)
    world["tickets_rendered"] = render_tickets(world, world["rng"])
    return world
