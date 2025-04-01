import os
import sys
from pathlib import Path

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import logging

from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Initialize controller first
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS path
        headless=False,
    )
)

controller = Controller()


@controller.action(
    "Upload file to interactive element with file path ",
)
async def upload_file(
    index: int, path: str, browser: BrowserContext, available_file_paths: list[str]
):
    if path not in available_file_paths:
        return ActionResult(error=f"File path {path} is not available")

    if not os.path.exists(path):
        return ActionResult(error=f"File {path} does not exist")

    dom_el = await browser.get_dom_element_by_index(index)

    file_upload_dom_el = dom_el.get_file_upload_element()
    print(file_upload_dom_el)

    if file_upload_dom_el is None:
        msg = f"AA No file upload element found at index {index}"
        print(msg)
        return ActionResult(error=msg)

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)
    print()
    print(file_upload_el)

    if file_upload_el is None:
        msg = f"BB No file upload element found at index {index}"
        print(msg)
        return ActionResult(error=msg)

    try:
        await file_upload_el.set_input_files(path)
        msg = f"Successfully uploaded file to index {index}"
        print(msg)
        return ActionResult(extracted_content=msg, include_in_memory=True)
    except Exception as e:
        msg = f"Failed to upload file to index {index}: {str(e)}"
        print(msg)
        return ActionResult(error=msg)


@controller.action("Read the file content of a file given a path")
async def read_file(path: str, available_file_paths: list[str]):
    if path not in available_file_paths:
        return ActionResult(error=f"File path {path} is not available")

    with open(path, "r") as f:
        content = f.read()
    msg = f"File content: {content}"
    print(msg)
    return ActionResult(extracted_content=msg, include_in_memory=True)


def create_file(file_type: str = "txt"):
    with open(f"tmp.{file_type}", "w") as f:
        f.write("test")
    file_path = Path.cwd() / f"tmp.{file_type}"
    print(f"Created file: {file_path}")
    return str(file_path)


async def main():
    task = """ 
            1. Clique no botão para criar um novo notebook
            5. upload the file by droping it in the space
            6. Wait for the file to be processed. DO NOT CLICK ANYTHING while the file is processing.
            7. Generate an audio overview and wait for it to be processed
            8. Click on the three dots button and select Download the audio overview
"""

    available_file_paths = [create_file("txt"), create_file("pdf"), create_file("csv")]

    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    agent = Agent(
        task=task,
        llm=model,
        controller=controller,
        browser=browser,
        available_file_paths=available_file_paths,
        initial_actions=[
            {"open_tab": {"url": "https://notebooklm.google.com/"}},
        ],
    )

    await agent.run()

    await browser.close()

    input("Press Enter to close...")


if __name__ == "__main__":
    asyncio.run(main())
