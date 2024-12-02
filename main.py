import asyncio
import os
from loginautomate import login_and_save_session
from song_request import send_song_request, monitor_status

async def main():
    # Step 1: Automate Login if `auth_session.json` doesn't exist
    if not os.path.exists("auth_session.json"):
        print("Session not found. Logging in...")
        await login_and_save_session()
        print("Login successful. Session saved.")

    # Step 2: Send a song generation request
    print("Sending song generation request...")
    uuid = await send_song_request()
    if not uuid:
        print("Failed to send song generation request. Exiting.")
        return

    # Step 3: Monitor the song generation status
    print("Monitoring song generation status...")
    await monitor_status(uuid)

if __name__ == "__main__":
    asyncio.run(main())
