import subprocess
import asyncio

async def cleanup_chrome_processes():
    """Aggressively cleanup zombie Chrome processes"""
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                ["pkill", "-9", "chrome"],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
        )
        await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                ["pkill", "-9", "chromedriver"],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
        )
        await asyncio.sleep(1)
    except Exception as e:
        print(f"[cleanup] Error: {e}")

