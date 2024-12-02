import os
from dotenv import load_dotenv
import asyncio
from playwright.async_api import async_playwright

load_dotenv()
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")


async def login_and_save_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="auth_session.json")
        page = await context.new_page()
        
        # Navigate to login page
        await page.goto("https://suno.com/login")
        
        # Click on Google login
        await page.click('button:text("Sign in with Google")')

        # Enter Google credentials (adjust selectors based on the actual login form)
        await page.fill('input[type="email"]', GOOGLE_EMAIL)
        await page.click('button:has-text("Next")')
        await page.fill('input[type="password"]', GOOGLE_PASSWORD)
        await page.click('button:has-text("Next")')

        # Wait for successful login (adjust wait conditions based on the app)
        await page.wait_for_url("https://suno.com/dashboard")
        
        # Save session state
        await context.storage_state(path="auth_session.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_and_save_session())
