import asyncio
import httpx
import json

async def send_song_request():
    async with httpx.AsyncClient() as client:
        # Load session cookies
        with open("auth_session.json") as f:
            auth_session = json.load(f)
        
        cookies = {c["name"]: c["value"] for c in auth_session["cookies"]}

        # Define the request payload
        payload = {
            "song_name": "My Generated Song",
            "genre": "Pop",
            "length": 3.5  # Song length in minutes
        }

        # Send POST request to the song generation endpoint
        response = await client.post(
            "https://suno.com/api/generate",
            json=payload,
            cookies=cookies
        )

        # Handle the response
        if response.status_code == 200:
            data = response.json()
            print("Song generation initiated:", data)
            return data["uuid"]
        else:
            print("Failed to initiate song generation:", response.text)
            return None
        
async def monitor_status(uuid):
    async with httpx.AsyncClient() as client:
        url = f"https://suno.com/song/status/{uuid}"
        
        while True:
            response = await client.get(url)
            if response.status_code == 200:
                status = response.json().get("status")
                print(f"Current status: {status}")
                
                if status == "completed":
                    print("Song generation completed!")
                    break
                elif status == "failed":
                    print("Song generation failed.")
                    break
            else:
                print("Failed to fetch status:", response.text)
            
            # Wait for 5 seconds before retrying
            await asyncio.sleep(5)
       

if __name__ == "__main__":
    asyncio.run(send_song_request())
