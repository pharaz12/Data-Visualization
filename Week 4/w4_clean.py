"""
w4_clean.py -- the Part D cleaning pipeline for sessions_hourly.csv, written as
one small function per fault so a notebook can run them one at a time and
print what each one did.  Every function returns (result, log_entry); the log
entries are what Part E quotes (rule, count, before -> after).

The six faults, in the order the notebook meets them:
    1. mixed timestamp formats  (ISO text vs dd/mm/yyyy text)
    2. rows are not in time order
    3. inconsistent device labels  (Mobile / mobile / MOBILE ...)
    4. sentinel value  sessions == -1
    5. duplicated hours  (the same hour logged twice)
    6. whole days never recorded  (+ a partial final month)
"""
from __future__ import annotations
import numpy as np
import pandas as pd

ISO_RE = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
DMY_RE = r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$"


def parse_timestamps(df: pd.DataFrame):
    """Parse each format with its OWN explicit format string.

    The slash format is dd/mm/yyyy, not mm/dd/yyyy: in the slash rows the
    first field reaches 31 and the second never exceeds 12.  An mm/dd reading
    is impossible for those rows, and format='mixed' would silently apply it
    to every row where both fields are <= 12 -- moving them to the wrong day.
    """
    iso = df.ts.str.match(ISO_RE)
    dmy = df.ts.str.match(DMY_RE)
    assert (iso | dmy).all(), "a third timestamp format is present"
    out = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    out[iso] = pd.to_datetime(df.ts[iso], format="%Y-%m-%d %H:%M:%S")
    out[dmy] = pd.to_datetime(df.ts[dmy], format="%d/%m/%Y %H:%M")
    slash = df.ts[dmy]
    log = {
        "fault": "mixed timestamp formats",
        "rule": "parse ISO rows as %Y-%m-%d %H:%M:%S and slash rows as "
                "%d/%m/%Y %H:%M (first field reaches 31, second never "
                "exceeds 12 => day-first)",
        "n_iso": int(iso.sum()), "n_slash": int(dmy.sum()),
        "slash_first_field_max": int(slash.str[:2].astype(int).max()),
        "slash_second_field_max": int(slash.str[3:5].astype(int).max()),
        "rows_removed": 0,
    }
    return out, log


def mixed_parse_damage(df: pd.DataFrame, correct: pd.Series) -> dict:
    """What format='mixed' would have done -- for the write-up."""
    bad = pd.to_datetime(df.ts, format="mixed")
    wrong = int((bad != correct).sum())
    return {
        "mixed_min": str(bad.min()), "mixed_max": str(bad.max()),
        "correct_min": str(correct.min()), "correct_max": str(correct.max()),
        "rows_on_wrong_date": wrong,
        "span_days_mixed": int((bad.max() - bad.min()).days),
        "span_days_correct": int((correct.max() - correct.min()).days),
    }


def sort_by_time(df: pd.DataFrame):
    was_sorted = bool(df.index.is_monotonic_increasing)
    out = df.sort_index()
    return out, {"fault": "rows not in time order", "rule": "sort_index()",
                 "already_sorted": was_sorted, "rows_removed": 0}


def normalise_device(df: pd.DataFrame):
    before = df.device.value_counts().to_dict()
    out = df.copy()
    out["device"] = out.device.str.strip().str.title()
    return out, {"fault": "inconsistent device labels",
                 "rule": "strip + title-case",
                 "before": before, "after": out.device.value_counts().to_dict(),
                 "rows_removed": 0}


def drop_duplicate_hours(df: pd.DataFrame):
    """Drop repeated timestamps, but only after proving they are copies."""
    dup_mask = df.index.duplicated(keep=False)
    grp = df[dup_mask].groupby(level=0)[["sessions", "orders", "revenue_pkr",
                                         "device"]].nunique()
    all_identical = bool((grp.max(axis=1) == 1).all())
    n_dup_rows = int(df.index.duplicated().sum())
    out = df[~df.index.duplicated(keep="first")]
    return out, {"fault": "duplicated hours",
                 "rule": "keep first row per timestamp (verified: every "
                         "duplicate pair is value-identical)",
                 "n_timestamps_duplicated": int(grp.shape[0]),
                 "all_pairs_identical": all_identical,
                 "rows_removed": n_dup_rows}


def sentinel_to_nan(df: pd.DataFrame):
    """sessions == -1 is a collector 'no reading' code, not a count."""
    mask = df.sessions == -1
    out = df.copy()
    out["sessions_missing"] = mask
    out.loc[mask, "sessions"] = np.nan
    return out, {"fault": "sentinel -1 in sessions",
                 "rule": "sessions == -1 -> NaN (flagged in sessions_missing)",
                 "n_sentinel": int(mask.sum()),
                 "other_columns_touched": False,
                 "rows_removed": 0}


def impute_sentinel_hours(df: pd.DataFrame):
    """Fill the -1 hours with the median of the same hour-of-week, and FLAG it.

    Leaving them NaN would void ~200 of 516 daily totals (a day with one bad
    hour has no sum).  Filling them keeps the daily total honest to a few
    percent; the flag column keeps the fill visible.
    """
    out = df.copy()
    how = out.index.dayofweek * 24 + out.index.hour
    med = out.groupby(how).sessions.transform("median")
    mask = out.sessions.isna()
    out["sessions_imputed"] = mask
    out.loc[mask, "sessions"] = med[mask].round()
    return out, {"fault": "sentinel hours (fill)",
                 "rule": "median of same day-of-week x hour; flagged in "
                         "sessions_imputed",
                 "n_filled": int(mask.sum()),
                 "sessions_filled_total": float(out.loc[mask, "sessions"].sum())}


def to_daily(df: pd.DataFrame):
    """Count gaps on the HOURLY index first, then resample flows with sum().

    min_count=24 makes a day with fewer than 24 hourly rows NaN instead of a
    silent short total or a silent 0.
    """
    full = pd.date_range(df.index.min(), df.index.max(), freq="h")
    missing_hours = full.difference(df.index)
    hourly = df.reindex(full)
    daily = pd.DataFrame({
        "sessions": hourly.sessions.resample("D").sum(min_count=24),
        "orders": hourly.orders.resample("D").sum(min_count=24),
        "revenue_pkr": hourly.revenue_pkr.resample("D").sum(min_count=24),
    })
    gap_days = daily.index[daily.sessions.isna()]
    return daily, hourly, {
        "fault": "days never recorded",
        "rule": "reindex to a complete hourly calendar, count gaps there, "
                "then resample('D').sum(min_count=24); gap days stay NaN "
                "(line breaks, not zeros)",
        "n_missing_hours": int(len(missing_hours)),
        "n_gap_days": int(len(gap_days)),
        "gap_days": [str(d.date()) for d in gap_days],
        "rows_removed": 0,
    }


def partial_tail(daily: pd.DataFrame):
    last = daily.index.max()
    month_start = last.replace(day=1)
    days_in_month = (month_start + pd.offsets.MonthEnd(0)).day
    n = int((daily.index >= month_start).sum())
    return {"fault": "partial final month",
            "tail_month": str(month_start.date())[:7],
            "days_present": n, "days_in_month": int(days_in_month),
            "rule": "kept on the daily chart, shaded and labelled partial; "
                    "never compared as a monthly total",
            "tail_start": str(month_start.date())}


def run_all(path="data/sessions_hourly.csv"):
    """The whole pipeline, for notebooks that only need the answer."""
    raw = pd.read_csv(path)
    logs = []
    ts, l1 = parse_timestamps(raw); logs.append(l1)
    df = raw.drop(columns="ts").set_index(pd.DatetimeIndex(ts, name="ts"))
    df, l2 = sort_by_time(df); logs.append(l2)
    df, l3 = normalise_device(df); logs.append(l3)
    df, l4 = drop_duplicate_hours(df); logs.append(l4)
    df, l5 = sentinel_to_nan(df); logs.append(l5)
    df, l5b = impute_sentinel_hours(df); logs.append(l5b)
    daily, hourly, l6 = to_daily(df); logs.append(l6)
    logs.append(partial_tail(daily))
    return dict(raw=raw, hourly_clean=df, hourly_full=hourly, daily=daily,
                logs=logs)


# ================================================================ catalogue
def clean_catalogue(path="data/revenue_catalogue.csv"):
    """Make revenue_catalogue.csv a TREE, then roll it up to sub-category.

    Two faults:
      * one SKU (SKU-0127) is listed under two parents -> a child with two
        parents is not a tree; its double-count inflates Wearables by ~0.9pp.
        Rule: keep the row whose sku_name prefix matches the sub-category that
        prefix belongs to everywhere else.
      * seven SKUs have NEGATIVE net revenue (returns exceed sales). Area
        cannot be negative, so the leaf SKUs are never drawn individually.
        They are netted inside their sub-category (every sub-category total
        stays positive) and reported.
    Returns (catalogue_clean, subcategory_table, logs).
    """
    c = pd.read_csv(path)
    logs = []
    c["prefix"] = c.sku_name.str.split("-").str[0]
    home = c.groupby("prefix").subcategory.agg(lambda x: x.value_counts().index[0])

    dup_skus = c.sku[c.sku.duplicated(keep=False)].unique().tolist()
    before_dups = c[c.sku.isin(dup_skus)][["sku", "category", "subcategory", "net_revenue_pkr_m"]]
    keep = ~c.sku.duplicated(keep=False) | (c.subcategory == c.prefix.map(home))
    removed = c[~keep]
    cc = c[keep].drop(columns="prefix").reset_index(drop=True)
    assert cc.sku.is_unique
    logs.append({"fault": "SKU with two parents (not a tree)",
                 "rule": "keep the row whose sku_name prefix matches its sub-category's home; drop the other copy",
                 "skus": dup_skus, "rows_removed": int(len(removed)),
                 "removed_parent": removed.subcategory.tolist(),
                 "kept_parent": cc[cc.sku.isin(dup_skus)].subcategory.tolist(),
                 "net_revenue_removed_pkr_m": float(removed.net_revenue_pkr_m.sum())})

    neg = cc[cc.net_revenue_pkr_m < 0]
    logs.append({"fault": "negative net revenue",
                 "rule": "never drawn as area; netted inside sub-category totals (all totals > 0) and reported",
                 "n_negative_skus": int(len(neg)),
                 "sum_negative_pkr_m": float(neg.net_revenue_pkr_m.sum()),
                 "rows_removed": 0,
                 "by_subcategory": neg.groupby("subcategory").net_revenue_pkr_m.agg(["count", "sum"]).round(4).to_dict("index")})

    # tree check: every sub-category has exactly one parent
    assert cc.groupby("subcategory").category.nunique().max() == 1
    sub = (cc.groupby(["category", "subcategory"], as_index=False)
             .agg(net_revenue_pkr_m=("net_revenue_pkr_m", "sum"), n_skus=("sku", "count")))
    assert (sub.net_revenue_pkr_m > 0).all(), "a sub-category total is negative - cannot be drawn as area"
    total = float(sub.net_revenue_pkr_m.sum())
    sub["share_pct"] = sub.net_revenue_pkr_m / total * 100
    cat = cc.groupby("category").net_revenue_pkr_m.sum()
    assert abs(cat.sum() - total) < 1e-9          # children sum to the parent
    logs.append({"fault": "levels rolled up",
                 "rule": "344 SKUs summed to 8 sub-categories; depth cut at sub-category; "
                         "no 'Other' bucket needed (smallest sub-category is 2.4% of the total)",
                 "n_skus_in": int(len(cc)), "n_subcategories": int(len(sub)),
                 "other_bucket": {"n_categories": 0, "value_pkr_m": 0.0},
                 "total_net_pkr_m": total, "rows_removed": 0})
    return cc, sub, logs
