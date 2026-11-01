"""
Record high-resolution demonstration video for Amanah-Genome.
Saves video as WebM, then converts to standard H.264 MP4 with optimal web flags.
"""

import asyncio
import os
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

RECORDING_DIR = Path("/home/fam/amanah-genome/recordings")
RECORDING_DIR.mkdir(parents=True, exist_ok=True)
RAW_VIDEO_DIR = RECORDING_DIR / "raw_video"
RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
FINAL_MP4 = RECORDING_DIR / "amanah_genome_demo.mp4"

# Set syslibs for Oracle Linux 8 Chromium
SYSLIBS = "/home/fam/gmaps-scraper/syslibs/usr/lib64"
if SYSLIBS not in os.environ.get("LD_LIBRARY_PATH", ""):
    os.environ["LD_LIBRARY_PATH"] = f"{SYSLIBS}:{os.environ.get('LD_LIBRARY_PATH', '')}"


async def smooth_scroll(page, target_y: int, duration_ms: int = 1500, steps: int = 25):
    """Smooth scroll the page over a defined duration."""
    current_y = await page.evaluate("window.scrollY")
    distance = target_y - current_y
    step_delay = (duration_ms / steps) / 1000.0
    for i in range(1, steps + 1):
        progress = i / steps
        # easeInOutQuad
        ease = 2 * progress * progress if progress < 0.5 else 1 - pow(-2 * progress + 2, 2) / 2
        y = current_y + (distance * ease)
        await page.evaluate(f"window.scrollTo(0, {y})")
        await asyncio.sleep(step_delay)


async def record_demo():
    print("[1/5] Initializing Playwright with high-res recording...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--force-device-scale-factor=1",
                "--window-size=1920,1080",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(RAW_VIDEO_DIR),
            record_video_size={"width": 1920, "height": 1080},
        )

        page = await context.new_page()
        page.set_default_timeout(45000)

        # ------------------------------------------------------------------
        # SCENE 1: HERO & INTRODUCTION (0:00 - 0:25)
        # ------------------------------------------------------------------
        print("[2/5] Navigating to Amanah-Genome Portal...")
        await page.goto("http://127.0.0.1:8020/app/", wait_until="networkidle")
        await asyncio.sleep(2)

        # Highlight header
        print("  - Scene 1: Header & Institutional Badges")
        await asyncio.sleep(5)  # Let viewer read title, GITEX badge, and DoH context

        # ------------------------------------------------------------------
        # SCENE 2: UAE RECESSIVE DISORDERS PANEL REGISTRY (0:25 - 0:50)
        # ------------------------------------------------------------------
        print("  - Scene 2: Opening UAE Panel Registry...")
        panel_btn = page.locator('button:has-text("UAE Panel")')
        await panel_btn.click()
        await asyncio.sleep(3)

        # Smooth scroll modal if scrollable
        await page.evaluate("window.scrollBy({ top: 400, behavior: 'smooth' })")
        await asyncio.sleep(6)  # Pause to show 10 UAE disorders (HBB, SMN1, CFTR, etc.)

        # Return to Couple Portal
        couple_btn = page.locator('button:has-text("Couple Portal")')
        await couple_btn.click()
        await asyncio.sleep(3)
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await asyncio.sleep(2)

        # ------------------------------------------------------------------
        # SCENE 3: LOAD BENCHMARK SCENARIO 2 (HIGH RISK BETA-THALASSEMIA) (0:50 - 1:20)
        # ------------------------------------------------------------------
        print("  - Scene 3: Selecting Scenario 2 (Beta-Thalassemia)...")
        await smooth_scroll(page, target_y=380, duration_ms=1200)
        await asyncio.sleep(3)

        # Click Scenario 2 Card
        scenario_2 = page.locator('button:has-text("Scenario 2: High Risk Beta-Thalassemia")')
        await scenario_2.click()
        await asyncio.sleep(5)  # Pause to show dual VCF upload badges & Merkle commitment

        # Scroll to match button
        await smooth_scroll(page, target_y=680, duration_ms=1200)
        await asyncio.sleep(3)

        # ------------------------------------------------------------------
        # SCENE 4: EXECUTE ZERO-KNOWLEDGE MATCH (1:20 - 1:55)
        # ------------------------------------------------------------------
        print("  - Scene 4: Executing ZK-PSI Match...")
        match_btn = page.locator('button:has-text("Execute Zero-Knowledge Compatibility Match")')
        await match_btn.click()
        await asyncio.sleep(4)  # Wait for evaluation & animation to settle

        # Scroll to view High Risk Card
        await smooth_scroll(page, target_y=880, duration_ms=1500)
        await asyncio.sleep(7)  # Generous pause: 25% risk, HBB gene, Zero Leaked genes, Audit hash

        # ------------------------------------------------------------------
        # SCENE 5: CULTURAL AI COMPANION GUIDANCE (1:55 - 2:35)
        # ------------------------------------------------------------------
        print("  - Scene 5: Interacting with Amanah-AI Companion...")
        await smooth_scroll(page, target_y=1400, duration_ms=1500)
        await asyncio.sleep(4)

        # Inquiry 1: Should we cancel our wedding?
        print("    Inquiry 1: Should we cancel wedding?")
        pill_cancel = page.locator('button:has-text("Should we cancel our wedding?")')
        await pill_cancel.click()
        await asyncio.sleep(7)  # Pause to read the reassuring non-cancellation guidance

        # Inquiry 2: What is PGT-M / IVF?
        print("    Inquiry 2: What is PGT-M / IVF?")
        pill_pgtm = page.locator('button:has-text("What is PGT-M / IVF?")')
        await pill_pgtm.click()
        await asyncio.sleep(8)  # Pause to read PGT-M clinical pathway & Abu Dhabi support

        # ------------------------------------------------------------------
        # SCENE 6: DISPATCH DOH REFERRAL TICKET (2:35 - 3:00)
        # ------------------------------------------------------------------
        print("  - Scene 6: Dispatching DoH Referral Ticket...")
        await smooth_scroll(page, target_y=880, duration_ms=1200)
        await asyncio.sleep(3)

        referral_btn = page.locator('button:has-text("Connect with Certified DoH Counselor")')
        await referral_btn.click()
        await asyncio.sleep(4)  # Pause to see ticket ID generated

        # ------------------------------------------------------------------
        # SCENE 7: DOH COUNSELOR TRIAGE PORTAL (3:00 - 3:35)
        # ------------------------------------------------------------------
        print("  - Scene 7: Switching to Counselor Triage Portal...")
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await asyncio.sleep(2)

        counselor_tab = page.locator('button:has-text("Counselor Triage")')
        await counselor_tab.click()
        await asyncio.sleep(4)  # View triage queue with incoming tickets

        # Scroll to view ticket details
        await smooth_scroll(page, target_y=350, duration_ms=1200)
        await asyncio.sleep(5)  # View Sanitized Clinical Summary Brief (HBB, PGT-M, Zero PI)

        # Click Schedule Teleconsultation
        tele_btn = page.locator('button:has-text("Schedule Teleconsultation")')
        if await tele_btn.count() > 0:
            await tele_btn.first.click()
            await asyncio.sleep(5)  # Status updates to TELECONSULT_SCHEDULED

        # ------------------------------------------------------------------
        # SCENE 8: SCENARIO 1 (HARMONIOUS & COMPATIBLE) CLEARANCE (3:35 - 4:00)
        # ------------------------------------------------------------------
        print("  - Scene 8: Showing Harmonious Compatible Scenario...")
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        await asyncio.sleep(2)

        await page.locator('button:has-text("Couple Portal")').click()
        await asyncio.sleep(2)

        await smooth_scroll(page, target_y=380, duration_ms=1000)
        await asyncio.sleep(2)

        # Select Scenario 1
        sc1 = page.locator('button:has-text("Scenario 1: Harmonious & Compatible")')
        await sc1.click()
        await asyncio.sleep(3)

        await smooth_scroll(page, target_y=680, duration_ms=1000)
        await asyncio.sleep(2)

        await page.locator('button:has-text("Execute Zero-Knowledge Compatibility Match")').click()
        await asyncio.sleep(3)

        await smooth_scroll(page, target_y=880, duration_ms=1200)
        await asyncio.sleep(6)  # Display green "Harmonious Genetic Compatibility" status

        print("[3/5] Recording completed. Closing browser context...")
        await context.close()
        await browser.close()


def post_process_video():
    print("[4/5] Locating recorded video file...")
    webm_files = list(RAW_VIDEO_DIR.glob("*.webm"))
    if not webm_files:
        raise RuntimeError("No recorded WebM video found in directory!")

    latest_webm = max(webm_files, key=os.path.getctime)
    print(f"  Found WebM: {latest_webm} ({latest_webm.stat().st_size / (1024*1024):.2f} MB)")

    print("[5/5] Transcoding to high-compatibility H.264/AAC MP4 via FFmpeg...")
    ffmpeg_bin = "/home/fam/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"

    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(latest_webm),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(FINAL_MP4),
    ]

    subprocess.run(cmd, check=True)
    mp4_size_mb = FINAL_MP4.stat().st_size / (1024 * 1024)
    print(f"SUCCESS! Rendered final MP4: {FINAL_MP4} ({mp4_size_mb:.2f} MB)")


if __name__ == "__main__":
    asyncio.run(record_demo())
    post_process_video()
