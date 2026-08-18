from __future__ import annotations

import base64
import html
import random
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="UD Financial Accounting Hoops Challenge", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stMain"] {
            overflow: hidden;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: none;
            padding: 60px 0 0;
        }

        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
            gap: 0;
        }

        iframe[data-testid="stIFrame"][title="st.iframe"] {
            position: fixed;
            z-index: 0;
            top: 60px;
            right: 0;
            bottom: 0;
            left: 0;
            display: block;
            width: 100vw;
            height: calc(100vh - 60px) !important;
            height: calc(100dvh - 60px) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_DIR = Path(__file__).resolve().parent

# These URLs and field identifiers belong to the public Google Form and the
# published Leaderboard tab. They are integration identifiers, not secrets.
GOOGLE_FORM_ACTION = (
    "https://docs.google.com/forms/u/0/d/e/"
    "1FAIpQLSdwoJyyhevlW6Qn5zEaogxb_MsStiK0CZASV9uK0z8KoCuaIA/formResponse"
)
LEADERBOARD_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQtNnYVM9mU7X63VhPlng78CqwawCLIXHqIREAZawATyZEhsEWs_6TI_b8KK4hRC_zeiKwxaL1R72bg/"
    "pub?gid=4392995&single=true&output=csv"
)
FORM_FIELD_IDS = {
    "first_name": "entry.919779357",
    "last_initial": "entry.1329702632",
    "section_number": "entry.1468180747",
    "score": "entry.827728069",
    "attempt_id": "entry.1076422944",
    "completion_time": "entry.1244525519",
}


def asset_data_uri(filename: str, mime_type: str) -> str:
    """Return a deployment-safe data URI for a bundled asset."""
    encoded = base64.b64encode((APP_DIR / filename).read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def png_data_uri(filename: str) -> str:
    return asset_data_uri(filename, "image/png")


HOOP_IMAGE_URI = png_data_uri("UD Hoop.png")
BASKETBALL_IMAGE_URI = png_data_uri("UD Basketball.png")
SUCCESS_SOUND_URI = asset_data_uri("assets/basketball-through-net.wav", "audio/wav")
MISS_SOUND_URI = asset_data_uri("assets/basketball-hard-hit.wav", "audio/wav")
BUZZER_SOUND_URI = asset_data_uri("assets/basketball-buzzer.wav", "audio/wav")

# Card data is randomized on each Streamlit rerun.
card_data = [
    {"target": "Cash Account", "text": "Currency and coins on hand plus balances in checking and savings accounts."},
    {"target": "Sales Revenue", "text": "Amounts earned from selling products to customers."},
    {"target": "Accounts Payable", "text": "Amounts owed to suppliers for purchases made on credit."},
    {"target": "Service Revenue", "text": "Amounts earned from performing services for customers."},
    {"target": "Equipment", "text": "Machinery, computers, tools, and vehicles owned and used in operations."},
    {"target": "Retained Earnings", "text": "Cumulative profits kept in the business rather than paid as dividends."},
    {"target": "Inventory", "text": "Products a company owns and holds for resale to customers."},
    {"target": "Accounts Receivable", "text": "Amounts customers owe for products or services sold on credit."},
    {"target": "Utilities Expense", "text": "Cost of electricity, internet, water, and sewage used in operations."},
    {"target": "Land & Buildings", "text": "Land & physical stores used in a retailer's operations"},
    {"target": "Intangible Assets", "text": "Patents, Trademarks, & Copyrights"},
    {"target": "Land Investments", "text": "Land not used in operations and held for future use or appreciation."},
    {"target": "Unearned Revenue", "text": "Amounts received before goods are delivered or services are performed."},
    {"target": "Cost of Goods Sold", "text": "Cost of inventory sold to customers."},
    {"target": "Interest Expense", "text": "Cost of borrowing through loans, mortgages, or bonds."},
    {"target": "Common Stock", "text": "Amounts invested by stockholders in exchange for ownership shares."},
    {"target": "Supplies", "text": "Goods on hand for future use in operations, not for resale."},
    {"target": "Supplies Expense", "text": "Office and cleaning supplies used in current period operations."},
    {"target": "NET INCOME (LOSS)", "text": "Total Revenue less Total Expenses for an accounting period"},
    {"target": "Stock Investments", "text": "Long-term investments in another corporation's stock."},
    {"target": "Cost of Goods Sold", "text": "A merchandiser's cost to buy merchandise it later sold."},
    {"target": "Mortgage Payable", "text": "Amount due on a 20-year mortgage to finance purchase of a building"},
    {"target": "Advertising Expense", "text": "Cost of designing marketing materials and promoting the business or its products."},
    {"target": "Prepaid Expense", "text": "Rent paid in advance for occupancy in a future period."},
    {"target": "Salaries and Wages Payable", "text": "Salaries and wages owed for work already performed."},
    {"target": "Salaries & Wages Expense", "text": "Cost of employee labor used during the period."},
    {"target": "Long-Term Notes Payable", "text": "Amount owed beyond one year under a written promissory note."},
]

bucket_sections = [
    (
        "ASSETS",
        "assets",
        [
            "Cash Account",
            "Accounts Receivable",
            "Inventory",
            "Supplies",
            "Prepaid Expense",
            "Stock Investments",
            "Land Investments",
            "Equipment",
            "Land & Buildings",
            "Intangible Assets",
        ],
    ),
    (
        "LIABILITIES",
        "liabilities",
        [
            "Accounts Payable",
            "Salaries and Wages Payable",
            "Unearned Revenue",
            "Long-Term Notes Payable",
            "Mortgage Payable",
            "Bonds Payable",
        ],
    ),
    ("STOCKHOLDER'S EQUITY", "equity", ["Retained Earnings", "Common Stock"]),
    ("REVENUE", "revenue", ["Service Revenue", "Sales Revenue", "Interest Income"]),
    (
        "EXPENSES",
        "expenses",
        [
            "Cost of Goods Sold",
            "Supplies Expense",
            "Rent Expense",
            "Salaries & Wages Expense",
            "Advertising Expense",
            "Insurance Expense",
            "Interest Expense",
            "Income Tax Expense",
            "Utilities Expense",
        ],
    ),
    ("NET INCOME (LOSS)", "net-income", ["NET INCOME (LOSS)"]),
]


def card_text_class(text: str) -> str:
    if len(text) > 115:
        return "card-text card-text--compact"
    if len(text) > 90:
        return "card-text card-text--dense"
    return "card-text"


shuffled_cards = card_data.copy()
random.shuffle(shuffled_cards)

cards_html = "".join(
    (
        f'<div class="card" draggable="true" data-target="{html.escape(card["target"], quote=True)}" '
        f'id="card-{index}" role="button" tabindex="0" '
        f'aria-label="{html.escape(card["text"], quote=True)}">'
        '<img class="card-art" alt="" aria-hidden="true">'
        f'<span class="{card_text_class(card["text"])}">{html.escape(card["text"])}</span>'
        "</div>"
    )
    for index, card in enumerate(shuffled_cards)
)

sections_html = "".join(
    (
        f'<section class="section {section_class}">'
        f'<h2 class="section-header">{html.escape(title)}</h2>'
        '<div class="bucket-grid">'
        + "".join(
            (
                f'<div class="bucket" data-type="{html.escape(bucket, quote=True)}" '
                f'aria-label="{html.escape(bucket, quote=True)} hoop" role="button" tabindex="0">'
                '<img class="bucket-art" alt="" aria-hidden="true">'
                f'<span class="bucket-label">{html.escape(bucket)}</span>'
                "</div>"
            )
            for bucket in buckets
        )
        + "</div></section>"
    )
    for title, section_class, buckets in bucket_sections
)

game_template = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mobile-drag-drop@2.3.0-rc.2/default.css">
<script src="https://cdn.jsdelivr.net/npm/mobile-drag-drop@2.3.0-rc.2/index.min.js"></script>

<style>
    :root {
        --ud-red: #ce1141;
        --ud-blue: #002d72;
        --ud-light-blue: #d9e9f6;
        --ink: #132238;
    }

    * { box-sizing: border-box; }

    html, body {
        margin: 0;
        width: 100%;
        height: 100%;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--ink);
        background: #f5f7fb;
        overflow: hidden;
    }

    #main-container {
        height: 100vh;
        overflow-y: auto;
        overscroll-behavior: contain;
        -webkit-overflow-scrolling: touch;
    }

    #header-container {
        position: sticky;
        top: 0;
        z-index: 1000;
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        min-height: 68px;
        padding: 10px 20px;
        color: white;
        background: linear-gradient(135deg, var(--ud-blue), #001b44);
        border-bottom: 4px solid var(--ud-red);
        box-shadow: 0 6px 18px rgba(0, 25, 63, 0.22);
    }

    #header-title {
        grid-column: 2;
        margin: 0;
        font-size: clamp(20px, 2.25vw, 30px);
        line-height: 1.1;
        text-align: center;
        letter-spacing: 0.02em;
    }

    #header-status {
        grid-column: 3;
        justify-self: end;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    #score-board {
        min-width: 112px;
        padding: 8px 12px;
        font-size: clamp(15px, 1.45vw, 20px);
        font-weight: 800;
        text-align: center;
        color: white;
        background: rgba(206, 17, 65, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.55);
        border-radius: 999px;
    }

    #shot-clock-panel {
        display: grid;
        width: 76px;
        min-height: 54px;
        place-items: center;
        padding: 4px 7px 5px;
        color: #ff392e;
        background: #07090c;
        border: 2px solid #d7dce3;
        border-radius: 7px;
        box-shadow: inset 0 0 0 2px #242830, 0 3px 8px rgba(0, 0, 0, 0.32);
    }

    #shot-clock-label {
        font-size: 8px;
        font-weight: 900;
        line-height: 1;
        letter-spacing: 0.1em;
        color: #f7f7f7;
    }

    #shot-clock {
        min-width: 2ch;
        font-family: "Courier New", ui-monospace, monospace;
        font-size: 30px;
        font-weight: 900;
        line-height: 0.95;
        text-align: center;
        text-shadow: 0 0 5px rgba(255, 40, 30, 0.9);
        font-variant-numeric: tabular-nums;
    }

    #shot-clock-panel.expiring {
        border-color: #ffb21c;
        animation: clock-pulse 620ms ease-in-out infinite alternate;
    }

    #shot-clock-panel.violation {
        animation: clock-violation 420ms ease-in-out;
    }

    #shot-clock-panel.warmup {
        color: #ffd447;
        border-color: #ffd447;
        box-shadow: inset 0 0 0 2px #242830, 0 0 10px rgba(255, 212, 71, 0.45);
    }

    #player-controls {
        grid-column: 1;
        display: flex;
        min-width: 0;
        align-items: center;
        gap: 10px;
    }

    button {
        font: inherit;
    }

    .action-button {
        min-height: 40px;
        padding: 9px 15px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 850;
        color: white;
        background: var(--ud-blue);
        border: 2px solid var(--ud-blue);
        border-radius: 999px;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    .action-button:hover,
    .action-button:focus-visible {
        outline: none;
        transform: translateY(-1px);
        box-shadow: 0 5px 12px rgba(0, 25, 63, 0.2);
    }

    .action-button--header {
        flex: 0 0 auto;
        min-height: 38px;
        padding: 8px 13px;
        color: white;
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.68);
    }

    .action-button--header:hover,
    .action-button--header:focus-visible {
        background: rgba(255, 255, 255, 0.22);
        box-shadow: 0 5px 12px rgba(0, 0, 0, 0.22);
    }

    .action-button--secondary {
        color: var(--ud-blue);
        background: white;
    }

    .action-button:disabled {
        cursor: wait;
        opacity: 0.62;
        transform: none;
        box-shadow: none;
    }

    .layout-container {
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(330px, 0.85fr);
        gap: 18px;
        align-items: start;
        width: 100%;
        padding: 18px;
    }

    #game-board {
        display: flex;
        min-width: 0;
        flex-direction: column;
        gap: 18px;
        padding-bottom: 24px;
    }

    .section {
        padding: 14px;
        border: 2px solid rgba(0, 45, 114, 0.18);
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 25, 63, 0.07);
    }

    .section-header {
        margin: 0 0 10px;
        font-size: 15px;
        font-weight: 900;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--ud-blue);
    }

    .bucket-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
        gap: 12px;
    }

    .assets { background: #eaf5ff; }
    .liabilities { background: #fff0f3; }
    .equity { background: #f6efff; }
    .revenue { background: #fff6e9; }
    .expenses { background: #edf9f1; }
    .net-income { background: #fffce5; }

    .bucket {
        position: relative;
        width: 100%;
        max-width: 190px;
        aspect-ratio: 1;
        justify-self: center;
        border: 0;
        border-radius: 18%;
        filter: drop-shadow(0 7px 7px rgba(0, 25, 63, 0.18));
        transition: transform 160ms ease, filter 160ms ease;
    }

    .bucket-art,
    .card-art {
        position: absolute;
        z-index: 0;
        inset: 0;
        display: block;
        width: 100%;
        height: 100%;
        object-fit: contain;
        pointer-events: none;
        user-select: none;
    }

    .bucket-label {
        position: absolute;
        z-index: 3;
        top: 35%;
        left: 13%;
        right: 13%;
        display: flex;
        min-height: 22%;
        align-items: center;
        justify-content: center;
        padding: 5px 7px;
        overflow-wrap: anywhere;
        font-size: clamp(8px, 0.78vw, 11px);
        font-weight: 900;
        line-height: 1.04;
        text-align: center;
        color: white;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.75);
        background: rgba(0, 28, 70, 0.76);
        border: 1px solid rgba(255, 255, 255, 0.72);
        border-radius: 8px;
        backdrop-filter: blur(2px);
    }

    .bucket.drag-over {
        z-index: 5;
        transform: translateY(-4px) scale(1.055);
        filter: drop-shadow(0 0 13px rgba(206, 17, 65, 0.95));
    }

    .bucket:focus-visible {
        outline: 3px solid var(--ud-red);
        outline-offset: 2px;
    }

    .bucket.matched {
        filter: drop-shadow(0 0 12px rgba(12, 145, 72, 0.68));
    }

    #card-pool {
        position: sticky;
        top: 86px;
        display: grid;
        grid-template-columns: repeat(2, minmax(145px, 1fr));
        gap: 10px;
        max-height: calc(100vh - 104px);
        padding: 14px;
        overflow-y: auto;
        background: white;
        border: 2px solid rgba(0, 45, 114, 0.14);
        border-radius: 16px;
        box-shadow: 0 10px 28px rgba(0, 25, 63, 0.11);
    }

    .card {
        position: relative;
        display: flex;
        width: 100%;
        max-width: 190px;
        aspect-ratio: 1;
        align-items: center;
        justify-content: center;
        justify-self: center;
        padding: 0;
        cursor: grab;
        overflow: hidden;
        user-select: none;
        touch-action: none;
        background-color: transparent;
        border: 0;
        border-radius: 50%;
        filter: drop-shadow(0 6px 6px rgba(82, 27, 4, 0.28));
        transition: transform 120ms ease, filter 120ms ease, opacity 120ms ease;
    }

    .card:hover,
    .card:focus-visible {
        z-index: 2;
        outline: none;
        transform: translateY(-3px) scale(1.025);
        filter: drop-shadow(0 9px 9px rgba(82, 27, 4, 0.36));
    }

    .card.selected {
        z-index: 3;
        transform: translateY(-3px) scale(1.035);
        filter: drop-shadow(0 0 12px rgba(206, 17, 65, 0.95));
    }

    .card:active { cursor: grabbing; }

    .card-text {
        position: relative;
        z-index: 1;
        display: flex;
        width: 72%;
        min-height: 48%;
        max-height: 64%;
        align-items: center;
        justify-content: center;
        padding: 8px 7px;
        overflow: hidden;
        overflow-wrap: anywhere;
        font-size: clamp(8.2px, 0.72vw, 10.5px);
        font-weight: 800;
        line-height: 1.07;
        text-align: center;
        color: #09172a;
        text-shadow: 0 1px 0 rgba(255, 255, 255, 0.7);
        background: rgba(255, 255, 255, 0.79);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 44%;
        box-shadow: 0 2px 8px rgba(47, 14, 0, 0.22);
        backdrop-filter: blur(2px);
    }

    .card-text--dense {
        font-size: clamp(7.5px, 0.66vw, 9.5px);
        line-height: 1.04;
    }

    .card-text--compact {
        width: 74%;
        font-size: clamp(6.9px, 0.59vw, 8.7px);
        line-height: 1.02;
    }

    .bucket .card {
        position: absolute;
        z-index: 4;
        top: 63%;
        left: 50%;
        width: 34%;
        cursor: default;
        pointer-events: none;
        transform: translate(-50%, -50%);
        animation: score-ball 460ms cubic-bezier(0.2, 0.9, 0.25, 1.2);
    }

    .bucket .card .card-text { display: none; }
    .bucket .card:nth-of-type(1) { left: 43%; }
    .bucket .card:nth-of-type(2) { left: 59%; top: 66%; }

    @keyframes score-ball {
        0% { opacity: 0.2; transform: translate(-50%, -125%) scale(1.5) rotate(-18deg); }
        72% { opacity: 1; transform: translate(-50%, -42%) scale(0.92) rotate(8deg); }
        100% { transform: translate(-50%, -50%) scale(1) rotate(0); }
    }

    @keyframes miss-shake {
        0%, 100% { transform: translateX(0) rotate(0); }
        20% { transform: translateX(-5px) rotate(-2deg); }
        40% { transform: translateX(5px) rotate(2deg); }
        60% { transform: translateX(-3px) rotate(-1deg); }
        80% { transform: translateX(3px) rotate(1deg); }
    }

    @keyframes clock-pulse {
        from { transform: scale(1); box-shadow: inset 0 0 0 2px #242830, 0 0 4px rgba(255, 178, 28, 0.35); }
        to { transform: scale(1.045); box-shadow: inset 0 0 0 2px #242830, 0 0 13px rgba(255, 178, 28, 0.9); }
    }

    @keyframes clock-violation {
        0%, 100% { transform: scale(1); }
        35% { transform: scale(1.13); background: #7b0000; }
        70% { transform: scale(0.96); }
    }

    .miss-animation { animation: miss-shake 360ms ease-in-out; }

    .modal-backdrop {
        position: fixed;
        z-index: 5000;
        inset: 0;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 18px;
        background: rgba(0, 18, 47, 0.76);
        backdrop-filter: blur(4px);
    }

    .modal-backdrop.is-open { display: flex; }

    .modal-card {
        width: min(680px, 100%);
        max-height: min(820px, calc(100vh - 36px));
        padding: 24px;
        overflow-y: auto;
        background: white;
        border: 3px solid var(--ud-red);
        border-radius: 20px;
        box-shadow: 0 24px 70px rgba(0, 15, 40, 0.4);
    }

    .modal-card--player { width: min(520px, 100%); }

    .modal-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 8px;
    }

    .modal-title {
        margin: 0;
        font-size: clamp(24px, 4vw, 34px);
        line-height: 1.08;
        color: var(--ud-blue);
    }

    .modal-copy {
        margin: 8px 0 18px;
        line-height: 1.45;
        color: #435269;
    }

    .close-button {
        width: 40px;
        height: 40px;
        flex: 0 0 auto;
        cursor: pointer;
        font-size: 25px;
        line-height: 1;
        color: var(--ud-blue);
        background: #edf3f9;
        border: 0;
        border-radius: 50%;
    }

    .player-form {
        display: grid;
        gap: 14px;
    }

    .field-row {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(130px, 0.45fr);
        gap: 14px;
    }

    .form-field {
        display: grid;
        gap: 6px;
    }

    .form-field label {
        font-size: 14px;
        font-weight: 850;
        color: var(--ud-blue);
    }

    .form-field input {
        width: 100%;
        min-height: 46px;
        padding: 10px 12px;
        font: inherit;
        color: var(--ink);
        background: white;
        border: 2px solid #bdc9d8;
        border-radius: 10px;
    }

    .form-field input:focus {
        outline: 3px solid rgba(206, 17, 65, 0.18);
        border-color: var(--ud-red);
    }

    .form-error {
        min-height: 21px;
        margin: 0;
        font-size: 14px;
        font-weight: 750;
        color: #a0002b;
    }

    .privacy-note {
        margin: 0;
        padding: 11px 13px;
        font-size: 12px;
        line-height: 1.4;
        color: #34455e;
        background: #eef5fb;
        border-radius: 10px;
    }

    .intro-guide {
        display: grid;
        gap: 10px;
        margin: 0 0 18px;
        padding: 14px;
        color: #233751;
        background: #f3f7fb;
        border: 1px solid #d7e1ec;
        border-radius: 12px;
    }

    .intro-guide h3 {
        margin: 0;
        font-size: 15px;
        color: var(--ud-blue);
    }

    .intro-guide ul {
        margin: 0;
        padding-left: 20px;
        line-height: 1.42;
    }

    .intro-score-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 8px;
    }

    .intro-score-item {
        padding: 8px 10px;
        font-size: 13px;
        line-height: 1.25;
        background: white;
        border: 1px solid #d9e2ed;
        border-radius: 9px;
    }

    .intro-score-item strong {
        display: block;
        font-size: 17px;
        color: var(--ud-red);
    }

    .intro-score-item--positive strong { color: #08783e; }

    #completion-score {
        display: none;
        margin: 12px 0 16px;
        padding: 14px;
        font-size: 22px;
        font-weight: 900;
        text-align: center;
        color: white;
        background: linear-gradient(135deg, var(--ud-blue), #001b44);
        border-radius: 12px;
    }

    #completion-score.is-visible { display: block; }

    #save-status,
    #leaderboard-status {
        margin: 9px 0;
        font-size: 14px;
        line-height: 1.4;
        color: #435269;
    }

    .leaderboard-table-wrap {
        max-height: 360px;
        margin-top: 12px;
        overflow: auto;
        border: 1px solid #d5deea;
        border-radius: 12px;
    }

    .leaderboard-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    .leaderboard-table th,
    .leaderboard-table td {
        padding: 10px 12px;
        text-align: left;
        border-bottom: 1px solid #e5ebf2;
    }

    .leaderboard-table th {
        position: sticky;
        top: 0;
        z-index: 1;
        color: white;
        background: var(--ud-blue);
    }

    .leaderboard-table th:first-child,
    .leaderboard-table td:first-child,
    .leaderboard-table th:last-child,
    .leaderboard-table td:last-child {
        text-align: center;
    }

    .leaderboard-table tr.current-player td {
        font-weight: 850;
        background: #fff4d6;
    }

    .leaderboard-actions {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 18px;
    }

    @media (max-width: 780px) {
        #header-container {
            grid-template-columns: 1fr auto;
            min-height: 62px;
            padding: 9px 12px;
        }

        #header-title {
            grid-column: 1 / 3;
            grid-row: 1;
            justify-self: center;
            text-align: center;
        }

        #header-status {
            grid-column: 2;
            grid-row: 2;
            gap: 6px;
        }

        #score-board {
            min-width: 91px;
            padding: 7px 9px;
            font-size: 14px;
        }

        #shot-clock-panel {
            width: 62px;
            min-height: 49px;
        }

        #shot-clock { font-size: 26px; }

        #player-controls {
            grid-column: 1;
            grid-row: 2;
            justify-content: flex-start;
        }

        .layout-container {
            display: block;
            padding: 10px;
        }

        #main-container {
            scroll-padding-bottom: calc(var(--card-pool-height, 42vh) + 220px);
        }

        #game-board {
            padding-bottom: calc(var(--card-pool-height, 42vh) + 220px);
        }

        .bucket-grid {
            grid-template-columns: repeat(2, minmax(125px, 1fr));
            gap: 8px;
        }

        .bucket { max-width: 175px; }

        .bucket-label {
            font-size: clamp(8px, 2.7vw, 11px);
        }

        #card-pool {
            position: fixed;
            z-index: 2000;
            top: auto;
            right: 0;
            bottom: 0;
            left: 0;
            grid-template-columns: repeat(2, minmax(130px, 1fr));
            max-height: 42vh;
            padding: 9px 12px 16px;
            border-right: 0;
            border-bottom: 0;
            border-left: 0;
            border-radius: 18px 18px 0 0;
            box-shadow: 0 -8px 24px rgba(0, 25, 63, 0.2);
        }

        .card { max-width: 165px; }

        .card-text {
            font-size: clamp(7.4px, 2.18vw, 9.5px);
        }

        .card-text--dense {
            font-size: clamp(6.9px, 1.98vw, 8.8px);
        }

        .card-text--compact {
            font-size: clamp(6.4px, 1.82vw, 8.1px);
        }

        .modal-card { padding: 18px; }

        .modal-backdrop { align-items: flex-start; }

        .field-row { grid-template-columns: 1fr; }

        .leaderboard-table th,
        .leaderboard-table td { padding: 9px 8px; }
    }
</style>
</head>
<body>
<div hidden aria-hidden="true">
    <img id="hoop-source" src="__HOOP_IMAGE_URI__" alt="">
    <img id="basketball-source" src="__BASKETBALL_IMAGE_URI__" alt="">
    <audio id="success-sound" preload="auto" src="__SUCCESS_SOUND_URI__"></audio>
    <audio id="miss-sound" preload="auto" src="__MISS_SOUND_URI__"></audio>
    <audio id="buzzer-sound" preload="auto" src="__BUZZER_SOUND_URI__"></audio>
</div>
<main id="main-container">
    <header id="header-container">
        <div id="player-controls">
            <button id="leaderboard-button" class="action-button action-button--header" type="button">Leaderboard</button>
        </div>
        <h1 id="header-title">UD Financial Accounting Hoops Challenge</h1>
        <div id="header-status">
            <div id="shot-clock-panel" role="timer" aria-label="Shot clock: 15 seconds">
                <span id="shot-clock-label">SHOT CLOCK</span>
                <span id="shot-clock">15</span>
            </div>
            <div id="score-board" aria-live="polite">Score: <span id="score">0</span></div>
        </div>
    </header>

    <div class="layout-container">
        <div id="game-board">__SECTIONS_HTML__</div>
        <aside id="card-pool" aria-label="Accounting definition basketballs">__CARDS_HTML__</aside>
    </div>
</main>

<div id="player-modal" class="modal-backdrop is-open" role="dialog" aria-modal="true" aria-labelledby="player-modal-title">
    <div class="modal-card modal-card--player">
        <h2 id="player-modal-title" class="modal-title">Welcome to the Challenge</h2>
        <p class="modal-copy">Enter the information that will identify your score on the class leaderboard.</p>
        <section class="intro-guide" aria-labelledby="intro-guide-title">
            <h3 id="intro-guide-title">How to play</h3>
            <ul>
                <li>Drag each basketball to its matching accounting hoop, or tap a basketball and then tap its hoop.</li>
                <li>After you enter your information, you will have a 20-second warm-up to browse the board before the game officially begins.</li>
                <li>You have 15 seconds for each answer. The shot clock resets after every submitted answer.</li>
            </ul>
            <h3>Scoring</h3>
            <div class="intro-score-grid">
                <div class="intro-score-item intro-score-item--positive"><strong>+10</strong>Correct answer</div>
                <div class="intro-score-item"><strong>&minus;2</strong>Incorrect answer or shot-clock violation</div>
            </div>
        </section>
        <form id="player-form" class="player-form" novalidate>
            <div class="field-row">
                <div class="form-field">
                    <label for="first-name">First Name</label>
                    <input id="first-name" name="first-name" type="text" maxlength="30" autocomplete="given-name" required>
                </div>
                <div class="form-field">
                    <label for="last-initial">Last Initial</label>
                    <input id="last-initial" name="last-initial" type="text" maxlength="1" autocomplete="off" required>
                </div>
            </div>
            <div class="form-field">
                <label for="section-number">Section Number</label>
                <input id="section-number" name="section-number" type="text" maxlength="20" autocomplete="off" required>
            </div>
            <p id="player-form-error" class="form-error" role="alert"></p>
            <p class="privacy-note">The leaderboard displays only your first name, last initial, section number, high score, and best completion time. Your email address is not collected.</p>
            <button class="action-button" type="submit">Begin Warm-Up</button>
        </form>
    </div>
</div>

<div id="leaderboard-modal" class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="leaderboard-modal-title">
    <div class="modal-card">
        <div class="modal-header">
            <div>
                <h2 id="leaderboard-modal-title" class="modal-title">Leaderboard</h2>
                <p id="leaderboard-modal-copy" class="modal-copy">Highest score for each student; fastest completion time breaks score ties.</p>
            </div>
            <button id="leaderboard-close-button" class="close-button" type="button" aria-label="Close leaderboard">&times;</button>
        </div>
        <div id="completion-score" aria-live="polite"></div>
        <p id="save-status" aria-live="polite"></p>
        <p id="leaderboard-status" aria-live="polite">Loading leaderboard...</p>
        <div class="leaderboard-table-wrap">
            <table class="leaderboard-table">
                <thead>
                    <tr>
                        <th scope="col">Rank</th>
                        <th scope="col">Student</th>
                        <th scope="col">Section</th>
                        <th scope="col">High Score</th>
                        <th scope="col">Best Time</th>
                    </tr>
                </thead>
                <tbody id="leaderboard-body"></tbody>
            </table>
        </div>
        <div class="leaderboard-actions">
            <button id="leaderboard-refresh-button" class="action-button action-button--secondary" type="button">Refresh</button>
            <button id="play-again-button" class="action-button" type="button" hidden>Play Again</button>
        </div>
    </div>
</div>

<script>
    MobileDragDrop.polyfill({
        holdToDrag: 150,
        dragImageTranslateOverride: MobileDragDrop.scrollBehaviourDragImageTranslateOverride
    });

    const GOOGLE_FORM_ACTION = '__GOOGLE_FORM_ACTION__';
    const LEADERBOARD_CSV_URL = '__LEADERBOARD_CSV_URL__';
    const FORM_FIELDS = Object.freeze({
        firstName: '__FORM_FIRST_NAME__',
        lastInitial: '__FORM_LAST_INITIAL__',
        sectionNumber: '__FORM_SECTION_NUMBER__',
        score: '__FORM_SCORE__',
        attemptId: '__FORM_ATTEMPT_ID__',
        completionTime: '__FORM_COMPLETION_TIME__'
    });
    const WARMUP_SECONDS = 20;
    const WARMUP_DURATION_MS = WARMUP_SECONDS * 1000;
    const SHOT_CLOCK_SECONDS = 15;
    const SHOT_CLOCK_DURATION_MS = SHOT_CLOCK_SECONDS * 1000;

    let score = 0;
    let matchedCount = 0;
    let draggedItem = null;
    let selectedItem = null;
    let audioContext = null;
    let playerInfo = null;
    let attemptComplete = false;
    let currentAttemptId = createAttemptId();
    let gameStartedAt = null;
    let completionTimeSeconds = null;
    let warmupActive = false;
    let warmupDeadline = null;
    let warmupInterval = null;
    let warmupDisplayValue = WARMUP_SECONDS;
    let shotClockDeadline = null;
    let shotClockInterval = null;
    let shotClockResetTimeout = null;
    let shotClockDisplayValue = SHOT_CLOCK_SECONDS;

    const cards = Array.from(document.querySelectorAll('.card'));
    const buckets = Array.from(document.querySelectorAll('.bucket'));
    const mainContainer = document.getElementById('main-container');
    const cardPool = document.getElementById('card-pool');
    const scoreDisplay = document.getElementById('score');
    const hoopImageSource = document.getElementById('hoop-source').src;
    const basketballImageSource = document.getElementById('basketball-source').src;
    const successSound = document.getElementById('success-sound');
    const missSound = document.getElementById('miss-sound');
    const buzzerSound = document.getElementById('buzzer-sound');
    const shotClockPanel = document.getElementById('shot-clock-panel');
    const shotClockLabel = document.getElementById('shot-clock-label');
    const shotClockDisplay = document.getElementById('shot-clock');
    const playerModal = document.getElementById('player-modal');
    const playerForm = document.getElementById('player-form');
    const playerFormError = document.getElementById('player-form-error');
    const firstNameInput = document.getElementById('first-name');
    const lastInitialInput = document.getElementById('last-initial');
    const sectionNumberInput = document.getElementById('section-number');
    const leaderboardButton = document.getElementById('leaderboard-button');
    const leaderboardModal = document.getElementById('leaderboard-modal');
    const leaderboardModalTitle = document.getElementById('leaderboard-modal-title');
    const leaderboardModalCopy = document.getElementById('leaderboard-modal-copy');
    const leaderboardCloseButton = document.getElementById('leaderboard-close-button');
    const leaderboardRefreshButton = document.getElementById('leaderboard-refresh-button');
    const leaderboardStatus = document.getElementById('leaderboard-status');
    const leaderboardBody = document.getElementById('leaderboard-body');
    const completionScore = document.getElementById('completion-score');
    const saveStatus = document.getElementById('save-status');
    const playAgainButton = document.getElementById('play-again-button');

    document.querySelectorAll('.bucket-art').forEach((image) => {
        image.src = hoopImageSource;
    });

    document.querySelectorAll('.card-art').forEach((image) => {
        image.src = basketballImageSource;
    });

    function createAttemptId() {
        if (window.crypto && typeof window.crypto.randomUUID === 'function') {
            return window.crypto.randomUUID();
        }
        return `${Date.now()}-${Math.random().toString(36).slice(2, 12)}`;
    }

    function normalizeFirstName(value) {
        return value
            .trim()
            .replace(/\s+/g, ' ')
            .toLocaleLowerCase()
            .replace(/(^|[\s'-])\p{L}/gu, (match) => match.toLocaleUpperCase());
    }

    function isValidFirstName(value) {
        return /^\p{L}[\p{L}' -]{0,29}$/u.test(value);
    }

    function isValidLastInitial(value) {
        return /^\p{L}$/u.test(value);
    }

    function updateScore(delta) {
        score = Math.max(0, score + delta);
        scoreDisplay.textContent = score;
    }

    function syncCardPoolSpace() {
        const isMobileLayout = window.matchMedia('(max-width: 780px)').matches;
        if (!isMobileLayout) {
            document.documentElement.style.removeProperty('--card-pool-height');
            return;
        }

        const cardPoolHeight = Math.ceil(cardPool.getBoundingClientRect().height);
        document.documentElement.style.setProperty('--card-pool-height', `${cardPoolHeight}px`);
    }

    function formatDuration(seconds) {
        if (!Number.isFinite(seconds) || seconds <= 0) return '—';
        const totalHundredths = Math.round(seconds * 100);
        const minutes = Math.floor(totalHundredths / 6000);
        const wholeSeconds = Math.floor(totalHundredths / 100) % 60;
        const hundredths = totalHundredths % 100;
        return `${minutes}:${String(wholeSeconds).padStart(2, '0')}.${String(hundredths).padStart(2, '0')}`;
    }

    function renderShotClock(value) {
        shotClockDisplayValue = value;
        shotClockLabel.textContent = 'SHOT CLOCK';
        shotClockDisplay.textContent = String(value);
        shotClockPanel.setAttribute('aria-label', `Shot clock: ${value} second${value === 1 ? '' : 's'}`);
        shotClockPanel.classList.remove('warmup');
        shotClockPanel.classList.toggle('expiring', value > 0 && value <= 3 && !attemptComplete);
    }

    function renderWarmup(value) {
        warmupDisplayValue = value;
        shotClockLabel.textContent = 'WARM UP';
        shotClockDisplay.textContent = String(value);
        shotClockPanel.setAttribute('aria-label', `Warm-up: ${value} second${value === 1 ? '' : 's'} remaining`);
        shotClockPanel.classList.add('warmup');
        shotClockPanel.classList.remove('expiring', 'violation');
    }

    function finishWarmup() {
        if (!warmupActive) return;
        warmupActive = false;
        warmupDeadline = null;
        if (warmupInterval !== null) {
            window.clearInterval(warmupInterval);
            warmupInterval = null;
        }
        startGameTimers();
    }

    function updateWarmup() {
        if (!warmupActive || warmupDeadline === null) return;
        const remainingMilliseconds = warmupDeadline - performance.now();
        if (remainingMilliseconds <= 0) {
            finishWarmup();
            return;
        }
        const nextDisplayValue = Math.ceil(remainingMilliseconds / 1000);
        if (nextDisplayValue !== warmupDisplayValue) renderWarmup(nextDisplayValue);
    }

    function startWarmup() {
        warmupActive = true;
        gameStartedAt = null;
        completionTimeSeconds = null;
        warmupDeadline = performance.now() + WARMUP_DURATION_MS;
        renderWarmup(WARMUP_SECONDS);
        if (warmupInterval !== null) window.clearInterval(warmupInterval);
        warmupInterval = window.setInterval(updateWarmup, 100);
    }

    function resetShotClock(now = performance.now()) {
        if (attemptComplete || gameStartedAt === null) return;
        if (shotClockResetTimeout !== null) {
            window.clearTimeout(shotClockResetTimeout);
            shotClockResetTimeout = null;
        }
        shotClockDeadline = now + SHOT_CLOCK_DURATION_MS;
        renderShotClock(SHOT_CLOCK_SECONDS);
    }

    function stopShotClock() {
        shotClockDeadline = null;
        if (shotClockInterval !== null) {
            window.clearInterval(shotClockInterval);
            shotClockInterval = null;
        }
        if (shotClockResetTimeout !== null) {
            window.clearTimeout(shotClockResetTimeout);
            shotClockResetTimeout = null;
        }
        shotClockPanel.classList.remove('expiring', 'violation');
    }

    function handleShotClockViolation() {
        if (attemptComplete || gameStartedAt === null || shotClockDeadline === null) return;
        shotClockDeadline = null;
        updateScore(-2);
        renderShotClock(0);
        shotClockPanel.classList.add('violation');
        playShotClockBuzzer();
        window.setTimeout(() => shotClockPanel.classList.remove('violation'), 430);
        shotClockResetTimeout = window.setTimeout(() => {
            shotClockResetTimeout = null;
            resetShotClock();
        }, 350);
    }

    function updateShotClock() {
        if (shotClockDeadline === null || attemptComplete) return;
        const remainingMilliseconds = shotClockDeadline - performance.now();
        if (remainingMilliseconds <= 0) {
            handleShotClockViolation();
            return;
        }
        const nextDisplayValue = Math.ceil(remainingMilliseconds / 1000);
        if (nextDisplayValue !== shotClockDisplayValue) renderShotClock(nextDisplayValue);
    }

    function startGameTimers() {
        gameStartedAt = performance.now();
        completionTimeSeconds = null;
        resetShotClock(gameStartedAt);
        if (shotClockInterval !== null) window.clearInterval(shotClockInterval);
        shotClockInterval = window.setInterval(updateShotClock, 100);
        primeBundledSound(buzzerSound);
    }

    function captureCompletionTime() {
        if (gameStartedAt === null || completionTimeSeconds !== null) return;
        completionTimeSeconds = Math.max(0.01, Math.round((performance.now() - gameStartedAt) / 10) / 100);
        stopShotClock();
    }

    function openLeaderboard({ completed = false } = {}) {
        leaderboardModalTitle.textContent = completed ? 'Challenge Complete!' : 'Leaderboard';
        leaderboardModalCopy.textContent = completed
            ? 'Your result is being added below. It may take a few seconds for the rankings to refresh.'
            : 'Highest score for each student; fastest completion time breaks score ties.';
        completionScore.classList.toggle('is-visible', completed);
        completionScore.textContent = completed
            ? `Final Score: ${score} • Time: ${formatDuration(completionTimeSeconds)}`
            : '';
        saveStatus.textContent = completed ? 'Saving your score...' : '';
        playAgainButton.hidden = !completed;
        leaderboardModal.classList.add('is-open');
        leaderboardCloseButton.focus();
        loadLeaderboard();
    }

    function closeLeaderboard() {
        leaderboardModal.classList.remove('is-open');
        leaderboardButton.focus({ preventScroll: true });
    }

    function parseCsv(csvText) {
        const rows = [];
        let row = [];
        let field = '';
        let inQuotes = false;

        for (let index = 0; index < csvText.length; index += 1) {
            const character = csvText[index];
            const nextCharacter = csvText[index + 1];

            if (character === '"' && inQuotes && nextCharacter === '"') {
                field += '"';
                index += 1;
            } else if (character === '"') {
                inQuotes = !inQuotes;
            } else if (character === ',' && !inQuotes) {
                row.push(field);
                field = '';
            } else if ((character === '\n' || character === '\r') && !inQuotes) {
                if (character === '\r' && nextCharacter === '\n') index += 1;
                row.push(field);
                if (row.some((value) => value.trim() !== '')) rows.push(row);
                row = [];
                field = '';
            } else {
                field += character;
            }
        }

        row.push(field);
        if (row.some((value) => value.trim() !== '')) rows.push(row);
        return rows;
    }

    function isCurrentPlayer(entry) {
        if (!playerInfo) return false;
        return entry.firstName.toLocaleLowerCase() === playerInfo.firstName.toLocaleLowerCase()
            && entry.lastInitial.toLocaleUpperCase() === playerInfo.lastInitial.toLocaleUpperCase()
            && entry.section === playerInfo.sectionNumber;
    }

    function renderLeaderboard(entries) {
        leaderboardBody.replaceChildren();

        entries.slice(0, 100).forEach((entry, index) => {
            const tableRow = document.createElement('tr');
            if (isCurrentPlayer(entry)) tableRow.classList.add('current-player');

            const rankCell = document.createElement('td');
            const studentCell = document.createElement('td');
            const sectionCell = document.createElement('td');
            const scoreCell = document.createElement('td');
            const timeCell = document.createElement('td');

            rankCell.textContent = String(index + 1);
            studentCell.textContent = `${entry.firstName} ${entry.lastInitial}.`;
            sectionCell.textContent = entry.section;
            scoreCell.textContent = String(entry.highScore);
            timeCell.textContent = formatDuration(entry.bestTime);

            tableRow.append(rankCell, studentCell, sectionCell, scoreCell, timeCell);
            leaderboardBody.appendChild(tableRow);
        });

        leaderboardStatus.textContent = entries.length
            ? `Showing ${Math.min(entries.length, 100)} of ${entries.length} students.`
            : 'No scores have been recorded yet. Be the first!';
    }

    async function loadLeaderboard() {
        leaderboardRefreshButton.disabled = true;
        leaderboardStatus.textContent = 'Loading leaderboard...';

        try {
            const separator = LEADERBOARD_CSV_URL.includes('?') ? '&' : '?';
            const response = await fetch(`${LEADERBOARD_CSV_URL}${separator}_=${Date.now()}`, {
                cache: 'no-store'
            });
            if (!response.ok) throw new Error(`Leaderboard request failed (${response.status})`);

            const rows = parseCsv(await response.text());
            const entries = rows.slice(1)
                .map((row) => ({
                    firstName: (row[0] || '').trim(),
                    lastInitial: (row[1] || '').trim().replace(/\.$/, ''),
                    section: (row[2] || '').trim(),
                    highScore: Number.parseInt((row[3] || '').trim(), 10),
                    bestTime: Number.parseFloat((row[4] || '').trim())
                }))
                .filter((entry) => entry.firstName && entry.lastInitial && entry.section && Number.isFinite(entry.highScore))
                .filter((entry) => !(entry.firstName === 'Test' && entry.lastInitial === 'S' && entry.section === '999'))
                .sort((left, right) => {
                    const scoreDifference = right.highScore - left.highScore;
                    if (scoreDifference !== 0) return scoreDifference;
                    const leftTime = Number.isFinite(left.bestTime) ? left.bestTime : Number.POSITIVE_INFINITY;
                    const rightTime = Number.isFinite(right.bestTime) ? right.bestTime : Number.POSITIVE_INFINITY;
                    if (leftTime !== rightTime) return leftTime - rightTime;
                    return left.firstName.localeCompare(right.firstName);
                });

            renderLeaderboard(entries);
        } catch (error) {
            leaderboardBody.replaceChildren();
            leaderboardStatus.textContent = 'The leaderboard could not be loaded. Check your connection and select Refresh.';
        } finally {
            leaderboardRefreshButton.disabled = false;
        }
    }

    async function submitScore() {
        if (!playerInfo || !Number.isFinite(completionTimeSeconds)) return false;

        const payload = new URLSearchParams();
        payload.append(FORM_FIELDS.firstName, playerInfo.firstName);
        payload.append(FORM_FIELDS.lastInitial, playerInfo.lastInitial);
        payload.append(FORM_FIELDS.sectionNumber, playerInfo.sectionNumber);
        payload.append(FORM_FIELDS.score, String(score));
        payload.append(FORM_FIELDS.attemptId, currentAttemptId);
        payload.append(FORM_FIELDS.completionTime, completionTimeSeconds.toFixed(2));

        try {
            await fetch(GOOGLE_FORM_ACTION, {
                method: 'POST',
                mode: 'no-cors',
                body: payload
            });
            return true;
        } catch (error) {
            return false;
        }
    }

    async function completeAttempt() {
        if (attemptComplete || matchedCount !== cards.length) return;
        attemptComplete = true;
        openLeaderboard({ completed: true });

        const saved = await submitScore();
        saveStatus.textContent = saved
            ? 'Score sent successfully. Refresh the leaderboard if it does not appear immediately.'
            : 'Your score could not be sent. Check your connection, then use Play Again to retry the challenge.';

        window.setTimeout(loadLeaderboard, 1800);
    }

    function getAudioContext() {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (!AudioContextClass) return null;
        if (!audioContext) audioContext = new AudioContextClass();
        if (audioContext.state === 'suspended') audioContext.resume();
        return audioContext;
    }

    function createNoise(ctx, duration) {
        const frameCount = Math.max(1, Math.floor(ctx.sampleRate * duration));
        const buffer = ctx.createBuffer(1, frameCount, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < frameCount; i += 1) {
            data[i] = Math.random() * 2 - 1;
        }
        return buffer;
    }

    function playBounce(ctx, startTime, startFrequency = 115, volume = 0.22) {
        const oscillator = ctx.createOscillator();
        const gain = ctx.createGain();
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(startFrequency, startTime);
        oscillator.frequency.exponentialRampToValueAtTime(48, startTime + 0.14);
        gain.gain.setValueAtTime(volume, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.16);
        oscillator.connect(gain).connect(ctx.destination);
        oscillator.start(startTime);
        oscillator.stop(startTime + 0.17);
    }

    function playSynthesizedThroughNetSound() {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;

        playBounce(ctx, now, 125, 0.17);

        const noise = ctx.createBufferSource();
        const bandpass = ctx.createBiquadFilter();
        const gain = ctx.createGain();
        noise.buffer = createNoise(ctx, 0.42);
        bandpass.type = 'bandpass';
        bandpass.frequency.setValueAtTime(2400, now + 0.035);
        bandpass.frequency.exponentialRampToValueAtTime(900, now + 0.42);
        bandpass.Q.value = 0.55;
        gain.gain.setValueAtTime(0.001, now);
        gain.gain.linearRampToValueAtTime(0.14, now + 0.045);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.42);
        noise.connect(bandpass).connect(gain).connect(ctx.destination);
        noise.start(now + 0.02);
        noise.stop(now + 0.44);

        [0.08, 0.14, 0.2].forEach((offset, index) => {
            const tick = ctx.createOscillator();
            const tickGain = ctx.createGain();
            tick.type = 'triangle';
            tick.frequency.value = 1650 - index * 260;
            tickGain.gain.setValueAtTime(0.045, now + offset);
            tickGain.gain.exponentialRampToValueAtTime(0.001, now + offset + 0.05);
            tick.connect(tickGain).connect(ctx.destination);
            tick.start(now + offset);
            tick.stop(now + offset + 0.055);
        });
    }

    function playSynthesizedRimReboundSound() {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;

        [720, 1040, 1480].forEach((frequency, index) => {
            const oscillator = ctx.createOscillator();
            const gain = ctx.createGain();
            oscillator.type = index === 0 ? 'triangle' : 'sine';
            oscillator.frequency.setValueAtTime(frequency, now);
            oscillator.frequency.exponentialRampToValueAtTime(frequency * 0.72, now + 0.22);
            gain.gain.setValueAtTime(index === 0 ? 0.16 : 0.08, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
            oscillator.connect(gain).connect(ctx.destination);
            oscillator.start(now);
            oscillator.stop(now + 0.25);
        });

        playBounce(ctx, now + 0.16, 105, 0.2);
        playBounce(ctx, now + 0.34, 82, 0.1);
    }

    function playSynthesizedShotClockBuzzer() {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;

        [0, 0.34, 0.68, 1.02].forEach((offset, index) => {
            const oscillator = ctx.createOscillator();
            const gain = ctx.createGain();
            const startTime = now + offset;
            oscillator.type = 'sawtooth';
            oscillator.frequency.setValueAtTime(index % 2 === 0 ? 190 : 170, startTime);
            gain.gain.setValueAtTime(0.16, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.26);
            oscillator.connect(gain).connect(ctx.destination);
            oscillator.start(startTime);
            oscillator.stop(startTime + 0.27);
        });
    }

    function primeBundledSound(sound) {
        if (!sound || typeof sound.play !== 'function') return;
        const wasMuted = sound.muted;
        sound.muted = true;
        try {
            const playRequest = sound.play();
            if (playRequest && typeof playRequest.then === 'function') {
                playRequest
                    .then(() => {
                        sound.pause();
                        sound.currentTime = 0;
                        sound.muted = wasMuted;
                    })
                    .catch(() => { sound.muted = wasMuted; });
            } else {
                sound.pause();
                sound.currentTime = 0;
                sound.muted = wasMuted;
            }
        } catch (error) {
            sound.muted = wasMuted;
        }
    }

    function playBundledSound(sound, fallback) {
        if (!sound || typeof sound.play !== 'function') {
            fallback();
            return;
        }

        try {
            sound.pause();
            sound.currentTime = 0;
            const playRequest = sound.play();
            if (playRequest && typeof playRequest.catch === 'function') {
                playRequest.catch(() => fallback());
            }
        } catch (error) {
            fallback();
        }
    }

    function playThroughNetSound() {
        playBundledSound(successSound, playSynthesizedThroughNetSound);
    }

    function playRimReboundSound() {
        playBundledSound(missSound, playSynthesizedRimReboundSound);
    }

    function playShotClockBuzzer() {
        playBundledSound(buzzerSound, playSynthesizedShotClockBuzzer);
        window.setTimeout(() => {
            if (!buzzerSound || buzzerSound.paused) return;
            buzzerSound.pause();
            buzzerSound.currentTime = 0;
        }, 1400);
    }

    function dragStart(event) {
        if (warmupActive || gameStartedAt === null || attemptComplete) {
            event.preventDefault();
            return;
        }
        draggedItem = this;
        selectCard(this);
        window.setTimeout(() => { this.style.opacity = '0.45'; }, 0);
    }

    function dragEnd() {
        if (draggedItem) draggedItem.style.opacity = '1';
        draggedItem = null;
    }

    function dragOver(event) {
        event.preventDefault();
    }

    function dragEnter(event) {
        event.preventDefault();
        this.classList.add('drag-over');
    }

    function dragLeave() {
        this.classList.remove('drag-over');
    }

    function selectCard(card) {
        if (warmupActive || gameStartedAt === null || attemptComplete) return;
        if (selectedItem && selectedItem !== card) {
            selectedItem.classList.remove('selected');
        }
        selectedItem = card;
        selectedItem.classList.add('selected');
    }

    function attemptMatch(card, bucket) {
        if (warmupActive || gameStartedAt === null || attemptComplete) return;
        if (!card || card.getAttribute('draggable') === 'false') return;

        const expectedTarget = card.dataset.target;
        const bucketType = bucket.dataset.type;
        resetShotClock();

        if (expectedTarget === bucketType) {
            bucket.appendChild(card);
            card.setAttribute('draggable', 'false');
            card.setAttribute('tabindex', '-1');
            card.style.opacity = '1';
            card.style.cursor = 'default';
            card.classList.remove('selected');
            bucket.classList.add('matched');
            selectedItem = null;
            updateScore(10);
            matchedCount += 1;
            playThroughNetSound();
            window.requestAnimationFrame(syncCardPoolSpace);
            if (matchedCount === cards.length) {
                captureCompletionTime();
                window.setTimeout(completeAttempt, 650);
            }
        } else {
            updateScore(-2);
            card.classList.add('miss-animation');
            bucket.classList.add('miss-animation');
            playRimReboundSound();
            window.setTimeout(() => {
                card.classList.remove('miss-animation');
                bucket.classList.remove('miss-animation');
            }, 380);
        }
    }

    function dragDrop(event) {
        event.preventDefault();
        this.classList.remove('drag-over');
        attemptMatch(draggedItem, this);
    }

    cards.forEach((card) => {
        card.addEventListener('dragstart', dragStart);
        card.addEventListener('dragend', dragEnd);
        card.addEventListener('click', () => selectCard(card));
        card.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                selectCard(card);
            }
        });
    });

    buckets.forEach((bucket) => {
        bucket.addEventListener('dragover', dragOver);
        bucket.addEventListener('dragenter', dragEnter);
        bucket.addEventListener('dragleave', dragLeave);
        bucket.addEventListener('drop', dragDrop);
        bucket.addEventListener('click', () => attemptMatch(selectedItem, bucket));
        bucket.addEventListener('keydown', (event) => {
            if ((event.key === 'Enter' || event.key === ' ') && selectedItem) {
                event.preventDefault();
                attemptMatch(selectedItem, bucket);
            }
        });
    });

    playerForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const firstName = normalizeFirstName(firstNameInput.value);
        const lastInitial = lastInitialInput.value.trim().toLocaleUpperCase();
        const sectionNumber = sectionNumberInput.value.trim().replace(/\s+/g, ' ');

        if (!isValidFirstName(firstName)) {
            playerFormError.textContent = 'Enter a valid first name using letters, spaces, apostrophes, or hyphens.';
            firstNameInput.focus();
            return;
        }
        if (!isValidLastInitial(lastInitial)) {
            playerFormError.textContent = 'Enter one letter for the last initial.';
            lastInitialInput.focus();
            return;
        }
        if (!sectionNumber || sectionNumber.length > 20) {
            playerFormError.textContent = 'Enter your section number.';
            sectionNumberInput.focus();
            return;
        }

        playerInfo = { firstName, lastInitial, sectionNumber };
        playerFormError.textContent = '';
        playerModal.classList.remove('is-open');
        startWarmup();
        leaderboardButton.focus({ preventScroll: true });
        mainContainer.scrollTop = 0;
        window.scrollTo(0, 0);
    });

    leaderboardButton.addEventListener('click', () => openLeaderboard());
    leaderboardCloseButton.addEventListener('click', closeLeaderboard);
    leaderboardRefreshButton.addEventListener('click', loadLeaderboard);
    playAgainButton.addEventListener('click', () => window.location.reload());

    leaderboardModal.addEventListener('click', (event) => {
        if (event.target === leaderboardModal) closeLeaderboard();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && leaderboardModal.classList.contains('is-open')) {
            closeLeaderboard();
        }
    });

    window.addEventListener('touchmove', (event) => {
        if (draggedItem) event.preventDefault();
    }, { passive: false });

    window.addEventListener('resize', () => window.requestAnimationFrame(syncCardPoolSpace));

    window.requestAnimationFrame(syncCardPoolSpace);
    window.setTimeout(() => firstNameInput.focus(), 50);
</script>
</body>
</html>
"""

custom_game_html = (
    game_template.replace("__HOOP_IMAGE_URI__", HOOP_IMAGE_URI)
    .replace("__BASKETBALL_IMAGE_URI__", BASKETBALL_IMAGE_URI)
    .replace("__SUCCESS_SOUND_URI__", SUCCESS_SOUND_URI)
    .replace("__MISS_SOUND_URI__", MISS_SOUND_URI)
    .replace("__BUZZER_SOUND_URI__", BUZZER_SOUND_URI)
    .replace("__SECTIONS_HTML__", sections_html)
    .replace("__CARDS_HTML__", cards_html)
    .replace("__GOOGLE_FORM_ACTION__", GOOGLE_FORM_ACTION)
    .replace("__LEADERBOARD_CSV_URL__", LEADERBOARD_CSV_URL)
    .replace("__FORM_FIRST_NAME__", FORM_FIELD_IDS["first_name"])
    .replace("__FORM_LAST_INITIAL__", FORM_FIELD_IDS["last_initial"])
    .replace("__FORM_SECTION_NUMBER__", FORM_FIELD_IDS["section_number"])
    .replace("__FORM_SCORE__", FORM_FIELD_IDS["score"])
    .replace("__FORM_ATTEMPT_ID__", FORM_FIELD_IDS["attempt_id"])
    .replace("__FORM_COMPLETION_TIME__", FORM_FIELD_IDS["completion_time"])
)

st.iframe(custom_game_html, height=920)
