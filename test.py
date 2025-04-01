from browser_use import Agent, Browser, BrowserConfig, Controller
from browser_use.browser.context import BrowserContext
from browser_use.agent.views import ActionResult
from langchain_openai import ChatOpenAI
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS path
        headless=False,
    )
)


controller = Controller()


@controller.action(
    "Upload file to interactive element",
)
async def upload_file(index: int, browser: BrowserContext):
    path = "/Users/joaoc/Downloads/test.pdf"

    if not os.path.exists(path):
        return ActionResult(error=f"File {path} does not exist")

    print(f"Uploading file to index {index}")
    dom_el = await browser.get_dom_element_by_index(index)

    # Get the file upload element
    file_upload_dom_el = dom_el.get_file_upload_element()

    if file_upload_dom_el is None:
        msg = f"No file upload element found at index {index}"
        print(msg)
        return ActionResult(error=msg)

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)

    if file_upload_el is None:
        msg = f"No file upload element found at index {index}"
        print(msg)
        return ActionResult(error=msg)

    # Set up file chooser handler
    async def handle_file_chooser(dialog):
        await dialog.accept(path)

    # Listen for file chooser events
    browser.page.on("filechooser", handle_file_chooser)

    try:
        # Click to trigger file chooser
        await file_upload_el.click()
        msg = f"Successfully uploaded file to index {index}"
        print(msg)
        return ActionResult(extracted_content=msg, include_in_memory=True)
    except Exception as e:
        msg = f"Failed to upload file to index {index}: {str(e)}"
        print(msg)
        return ActionResult(error=msg)


# Create the agent with your configured browser
agent = Agent(
    task="""
            1. Clique no botão para criar um novo notebook
            5. upload the file by droping it in the space
            6. Wait for the file to be processed. DO NOT CLICK ANYTHING while the file is processing.
            7. Generate an audio overview and wait for it to be processed
            8. Click on the three dots button and select Download the audio overview
            
            Important notes:
            - If you encounter any login prompts, handle them appropriately
            - Wait for each page/element to load before proceeding
            - If you need help or encounter issues, ask for assistance""",
    llm=ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    initial_actions=[
        {"open_tab": {"url": "https://notebooklm.google.com/"}},
    ],
    browser=browser,
    controller=controller,
    available_file_paths=["/Users/joaoc/Downloads/test.pdf"],
)


async def main():
    await agent.run()

    input("Press Enter to close the browser...")
    await browser.close()


if __name__ == "__main__":

    asyncio.run(main())
