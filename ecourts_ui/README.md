# eCourts Real-time Cause List UI (Django)

This project is a minimal Django app that demonstrates a UI to fetch State, District, Court Complex and Court Name in real time from the eCourts website and *attempt* to download cause list PDFs.

IMPORTANT: The official eCourts cause list page enforces a CAPTCHA before returning cause list PDFs. **I cannot provide code to bypass that CAPTCHA automatically** (that would be inappropriate). Instead, this project provides:

1. A Django web UI (`templates/index.html`) that loads states and shows the UI.
2. Backend endpoints that attempt to fetch lists in real-time (note: much of the eCourts page is populated by JavaScript/AJAX; simple scraping is brittle).
3. A helper Selenium script `scripts/download_causelist.py` that opens a real browser session, navigates to the cause list page, and lets you solve the CAPTCHA manually once. After you solve the CAPTCHA in the opened browser, the script can continue to download PDFs for the selected complex/courts.

## How to run

1. Create and activate a Python virtual environment (Python 3.9+ recommended).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```
   python manage.py migrate
   ```
4. Run the Django server:
   ```
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/ in your browser.

5. To download cause lists that require CAPTCHA, use the Selenium helper:
   ```
   python scripts/download_causelist.py --state "<STATE>" --district "<DISTRICT>" --complex "<COMPLEX_NAME>" --date YYYY-MM-DD
   ```
   The script opens a browser window and will pause at the CAPTCHA. Solve it manually; after solving the script will continue and save PDFs to `downloads/`.

## Notes on CAPTCHA and Ethics

- Many CAPTCHAs are explicitly intended to stop automated scripts. Bypassing them with third-party captcha-solving services is possible but usually paid and may violate site terms of service.
- This project **does not** include or recommend bypassing CAPTCHAs programmatically without proper authorization. It provides a user-assisted way (Selenium + manual CAPTCHA solve) to continue.

## Files of interest

- `causelist/views.py` — Django views and API endpoints (with explanatory comments)
- `scripts/download_causelist.py` — Selenium helper script
- `templates/index.html` & `static/*` — Frontend UI

