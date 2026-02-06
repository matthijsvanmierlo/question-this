from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 1. Start Editor
        page.goto("http://localhost:8000")
        page.click("text=Start Creating")

        # 2. Set Title
        title_input = page.locator("#editor-panel input[type='text']").first
        title_input.fill("Final Verification Lesson")
        title_input.blur() # Trigger change event

        # 3. Load Video (Required for sharing)
        page.fill("#video-url-input", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        page.click("text=Load Video")
        page.wait_for_timeout(1000) # Wait for player stub

        # 4. Share/Student Mode
        page.click("text=Share Assignment")

        # Get the URL from the share input
        share_url = page.input_value("#share-url")
        print(f"Share URL: {share_url}")

        # Navigate to Student Mode
        page.goto(share_url)
        page.wait_for_selector("#student-video-container")

        # Verify Title is above video
        # Title should be in h1 inside level-left above the box
        expect(page.locator("h1.title.is-5")).to_have_text("Final Verification Lesson")

        # 5. Go Home
        page.click("text=Exit")

        # 6. Go to My Assignments
        # It should appear now that we have progress (init creates it)
        page.click("text=My Assignments")

        # 7. Verify Table
        page.wait_for_selector("table")
        expect(page.locator("table")).to_contain_text("Final Verification Lesson")

        # Take screenshot
        page.screenshot(path="/home/jules/verification/final_verification.png")
        print("Screenshot saved to /home/jules/verification/final_verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()
