"""
Entry point.

Usage:
    python run.py wiki_research
    python run.py form_fill
    python run.py book_search_compare
    python run.py quotes_extract
    python run.py --custom "https://example.com" "Do X then Y then Z"

Produces:
    recordings/*.webm   - full screen recording of the browser session (Playwright video)
    traces/*.zip        - Playwright trace (open with `playwright show-trace traces/xxx.zip`
                           for a step-by-step replay with DOM snapshots, useful for debugging)
"""
import asyncio
import sys
import os
import time
from playwright.async_api import async_playwright

from agent import config
from agent.agent import BrowserAgent
from tasks import TASKS


async def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <task_name> | --custom <url> <instruction>")
        print(f"Available tasks: {list(TASKS.keys())}")
        return

    if sys.argv[1] == "--custom":
        start_url, instruction = sys.argv[2], sys.argv[3]
        task_name = "custom"
    else:
        task_name = sys.argv[1]
        if task_name not in TASKS:
            print(f"Unknown task '{task_name}'. Available: {list(TASKS.keys())}")
            return
        start_url = TASKS[task_name]["start_url"]
        instruction = TASKS[task_name]["instruction"]

    if not config.ANTHROPIC_API_KEY:
        raise SystemExit("Set the ANTHROPIC_API_KEY environment variable before running.")

    os.makedirs(config.RECORD_VIDEO_DIR, exist_ok=True)
    os.makedirs(config.TRACE_DIR, exist_ok=True)
    run_id = f"{task_name}_{int(time.time())}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO_MS)
        context = await browser.new_context(
            viewport={"width": config.SCREENSHOT_WIDTH, "height": config.SCREENSHOT_HEIGHT},
            record_video_dir=config.RECORD_VIDEO_DIR,
            record_video_size={"width": config.SCREENSHOT_WIDTH, "height": config.SCREENSHOT_HEIGHT},
        )
        await context.tracing.start(screenshots=True, snapshots=True, sources=False)

        page = await context.new_page()
        await page.goto(start_url, wait_until="domcontentloaded")

        agent = BrowserAgent(page, instruction)
        result = await agent.run()

        trace_path = os.path.join(config.TRACE_DIR, f"{run_id}.zip")
        await context.tracing.stop(path=trace_path)
        await context.close()  # flushes the video file to disk
        await browser.close()

        print("\n=== RESULT ===")
        print(result)
        print(f"Video saved under: {config.RECORD_VIDEO_DIR}")
        print(f"Trace saved to:    {trace_path}")


if __name__ == "__main__":
    asyncio.run(main())
