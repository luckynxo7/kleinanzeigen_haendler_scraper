import streamlit as st

# Import Selenium and WebDriver manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time


def scrape_dealer(dealer_url: str) -> list[str]:
    """Scrape all advertisement links from a Kleinanzeigen dealer page.

    The function opens the given dealer URL in a headless Chrome browser,
    accepts the cookie banner if present, iterates through all available
    pagination pages and collects unique links to individual ads.

    Args:
        dealer_url: URL of the dealer page on Kleinanzeigen (e.g. https://www.kleinanzeigen.de/pro/ff-wheels-by-felgenforum).

    Returns:
        A list of unique advertisement URLs found across all pages.
    """
    # Configure headless Chrome
    options = Options()
     options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
  
        options.add_argument("--disable-dev-shm-usage")ndbox")
    options.add_argument("--window-size=1920,1080")
   # Instantiate the driver; webdriver manager will download the binary if necessary
    # Instantiate the driver; webdriver manager will download the binary if necessary
    # New Selenium versions recommend passing a Service object instead of the driver path as the
    # first positional argument. Without using Service, passing the driver path can conflict
    # with other keyword arguments and raise errors like "got multiple values for argument 'options'".
    from selenium.webdriver.chrome.service import Service
    # Download the chromedriver binary via ChromeDriverManager and configure a Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(dealer_url)

    # Try to accept cookie consent if the banner appears
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Alle akzeptieren')]")
            )
        )
        cookie_button.click()
    except Exception:
        # Ignore if cookie banner is not present
        pass

    ad_links: set[str] = set()

    while True:
        # Wait a little to allow listings to load
        time.sleep(2)
        # Find all anchor elements whose href contains '/s-anzeige/'
        anchors = driver.find_elements(By.XPATH, "//a[contains(@href, '/s-anzeige/')]")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href and "/s-anzeige/" in href:
                # Some links might contain additional query parameters; strip them
                clean_href = href.split("?")[0]
                ad_links.add(clean_href)

        # Attempt to find a “Next” button in the pagination controls.
        # Kleinanzeigen uses arrow symbols or labels for navigation.
        try:
            next_button = driver.find_element(
                By.XPATH,
                "//a[contains(@aria-label, 'Nächste') or contains(text(), '›') or contains(text(), '»')]",
            )
            # If the next button has a disabled attribute or class, stop the loop
            classes = next_button.get_attribute("class") or ""
            if "disabled" in classes:
                break
            # Scroll the next button into view and click it
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
        except Exception:
            # No next page found; break the loop
            break

    driver.quit()
    return sorted(ad_links)


def main() -> None:
    """Streamlit user interface for scraping advertisement links from multiple dealer pages."""
    st.set_page_config(page_title="Kleinanzeigen Dealer Scraper", layout="centered")
    st.title("Kleinanzeigen Händler-Inserate sammeln")
    st.write(
        "Geben Sie einen oder mehrere Händlerlinks ein (jeweils eine URL pro Zeile). "
        "Die App besucht automatisch jede Seite, sammelt alle Inserat-Links und "
        "stellt das Ergebnis als herunterladbare Textdatei zur Verfügung."
    )

    url_input = st.text_area(
        "Händlerlinks eingeben", placeholder="https://www.kleinanzeigen.de/pro/haendler-a\nhttps://www.kleinanzeigen.de/pro/haendler-b", height=200
    )

    if st.button("Links sammeln"):
        # Split lines and remove empty entries
        urls = [line.strip() for line in url_input.splitlines() if line.strip()]
        if not urls:
            st.warning("Bitte geben Sie mindestens einen gültigen Händlerlink ein.")
            return

        all_links: list[str] = []
        progress_bar = st.progress(0.0, text="Starte Scraping...")
        for idx, dealer_url in enumerate(urls, start=1):
            st.write(f"Verarbeite {dealer_url}...")
            try:
                links = scrape_dealer(dealer_url)
                all_links.extend(links)
                st.success(f"{len(links)} Links von {dealer_url} gefunden.")
            except Exception as exc:
                st.error(f"Fehler beim Scraping von {dealer_url}: {exc}")
            progress_bar.progress(idx / len(urls))

        if all_links:
            st.write(f"Gesamt {len(all_links)} Inserat-Links gesammelt.")
            # Remove duplicates across dealers
            unique_links = sorted(set(all_links))
            # Prepare text for download
            content = "\n".join(unique_links)
            st.download_button(
                label="Download als TXT",
                data=content,
                file_name="kleinanzeigen_links.txt",
                mime="text/plain",
            )
        else:
            st.info("Es wurden keine Links gefunden.")


if __name__ == "__main__":
    main()
