# tests/test_ui.py
import pytest
from playwright.sync_api import sync_playwright, expect

APP_URL = "http://localhost:8000"  # change to the Posit Connect URL when testing deployed

# Verifies the app loads with both tabs visible and no crashes on startup,
# since a broken import or layout error would prevent any user interaction.
def test_app_loads_with_tabs():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        assert page.locator("text=Crime Dashboard").is_visible()
        assert page.locator("text=AI Explorer").is_visible()
        browser.close()

# Verifies that selecting a crime metric updates the KPI cards from placeholder to a value,
# since the peak_year and crime_rate outputs depend entirely on crime_type being set.
def test_crime_type_selection_updates_kpis():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        # Select "Violent Crime" from the Crime Metric dropdown
        page.select_option("#crime_type", "Violent Crime")
        page.wait_for_timeout(1500)
        # KPI cards should no longer show the placeholder text
        placeholder = page.locator("text=Select a type of Crime")
        expect(placeholder).not_to_be_visible()
        browser.close()

# Verifies that clicking the RESET button clears the crime type back to "None",
# since a broken reset would leave users stuck with stale filter state.
def test_reset_button_clears_crime_type():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        # First set a value
        page.select_option("#crime_type", "Homicide")
        page.wait_for_timeout(500)
        # Then reset
        page.click("#reset")
        page.wait_for_timeout(1000)
        # crime_type select should be back to "None"
        val = page.eval_on_selector("#crime_type", "el => el.value")
        assert val == "None"
        browser.close()