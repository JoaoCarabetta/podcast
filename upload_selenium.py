import time
import os
from playwright.sync_api import sync_playwright, expect
from pathlib import Path


def validate_file_path(pdf_file_path):
    """Validate that the PDF file path exists and is set correctly."""
    if "PASTE_YOUR_FULL_PDF_FILE_PATH_HERE" in pdf_file_path:
        print("ERROR: Please update the 'pdf_file_path' variable in the script.")
        return False

    if not os.path.exists(pdf_file_path):
        print(f"ERROR: The file specified does not exist: {pdf_file_path}")
        return False

    return True


def initialize_browser(playwright):
    """Initialize and configure the Chrome browser."""
    print("Initializing browser...")
    browser = playwright.chromium.launch(
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        headless=False,
    )
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    return browser, context, page


def wait_for_login(page, url):
    """Navigate to URL and wait for manual login."""
    print(f"Navigating to {url}")
    page.goto(url)
    input(
        "--> Please log in to your Google Account in the browser window and press Enter here when ready..."
    )
    print("Continuing script...")


def click_new_notebook(page):
    """Click the New Notebook button."""
    print("Looking for and clicking the 'Novo' button...")
    page.get_by_text("Novo").click()
    print("Clicked 'Novo'. Waiting for notebook interface...")
    page.wait_for_timeout(3000)


def upload_file(page, pdf_file_path):
    """Handle file upload process."""
    print("Looking for the 'Selecione o arquivo' button/link...")
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Selecione o arquivo").click()
    file_chooser = fc_info.value
    print(f"Uploading file: {pdf_file_path}")
    file_chooser.set_files(pdf_file_path)
    print("File uploaded.")


def wait_for_processing(page, pdf_file_path):
    """Wait for file upload and processing to complete."""
    print("Waiting for file to upload and process...")
    file_name_only = os.path.basename(pdf_file_path)

    # Wait for file to appear in list
    page.wait_for_selector(
        f"div.source-list-item >> text={file_name_only}", timeout=120000
    )
    print(f"Source item '{file_name_only}' found in the list.")

    # Wait for checkmark
    checkmark_selector = f"div.source-list-item:has-text('{file_name_only}') svg.check-icon, div.source-list-item:has-text('{file_name_only}') mat-icon:text-is('check_circle')"
    try:
        page.wait_for_selector(checkmark_selector, timeout=120000)
        print("File processing confirmed (checkmark found).")
    except TimeoutError:
        print(
            "ERROR: Timeout waiting for file processing to complete or checkmark to appear."
        )
        print("Attempting to continue, but later steps might fail.")

    page.wait_for_timeout(3000)


def generate_audio_overview(page):
    """Generate and wait for audio overview completion."""
    print("Looking for and clicking 'Visão geral em áudio'...")
    try:
        # Click the audio overview button
        audio_button_selector = "button:has-text('Visão geral em áudio')"
        page.wait_for_selector(audio_button_selector, timeout=30000)
        page.click(audio_button_selector)
        print("Clicked 'Visão geral em áudio'.")

        print("Waiting for audio overview generation to start and complete...")
        loading_selector = "div:has-text('Gerando a conversa'), div:has-text('Generating conversation'), div.spinner, div.loading"

        # Wait for loading indicator to appear and then disappear
        try:
            page.wait_for_selector(loading_selector, timeout=30000)
            print("Generation indicator found. Waiting for it to disappear...")
            page.wait_for_selector(loading_selector, state="hidden", timeout=120000)
            print("Audio overview generation appears complete.")
        except TimeoutError:
            print(
                "Warning: Could not find the generation indicator or it took too long. Assuming it finished."
            )

    except TimeoutError:
        print("ERROR: Could not find or click the 'Visão geral em áudio' button.")
    except Exception as e:
        print(f"An error occurred while clicking 'Visão geral em áudio': {e}")


def main():
    # Configuration
    notebooklm_url = "https://notebooklm.google.com/"
    pdf_file_path = r"/Users/joaoc/Downloads/test.pdf"

    if not validate_file_path(pdf_file_path):
        return

    with sync_playwright() as playwright:
        try:
            browser, context, page = initialize_browser(playwright)

            wait_for_login(page, notebooklm_url)
            click_new_notebook(page)
            upload_file(page, pdf_file_path)
            wait_for_processing(page, pdf_file_path)
            generate_audio_overview(page)

            print("Script finished the main steps.")

        except TimeoutError as e:
            print(
                f"ERROR: A timeout occurred - an element was not found or clickable within the time limit."
            )
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback

            traceback.print_exc()

        finally:
            print("Closing browser in 10 seconds...")
            time.sleep(10)
            context.close()
            browser.close()
            print("Browser closed.")


if __name__ == "__main__":
    main()
