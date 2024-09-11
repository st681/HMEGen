from generate import HideMyEmail
import asyncio

async def genProcess(cookie_string):
    async with HideMyEmail(cookies=cookie_string) as hide_my_email:
        while True: 
            for i in range(5):
                response = await hide_my_email.generate_email()
                print(f"Generated Email Response for cookie {cookie_string[:20]}...: {response}")

                if response.get('success'):
                    email = response['result']['hme']
                    print(f"Generated Email: {email}")

                    reserve_response = await hide_my_email.reserve_email(email)
                    print(f"Reserve Email Response for {email}: {reserve_response}")
                else:
                    print("Failed to generate email. Stopping process for this cookie.")
                    return 
            
            print(f"Waiting 30 minutes before generating next batch for cookie {cookie_string[:20]}...")
            await asyncio.sleep(1820)

async def main():
    print("iCloud Generator by stupit")
    input("Press enter to begin...")
    with open("cookies.txt", "r") as file:
        cookie_strings = [line.strip() for line in file.readlines() if line.strip()]

    num_cookies = len(cookie_strings)
    print(f"Found {num_cookies} cookies. Creating tasks for each.")

    tasks = []
    for cookie in cookie_strings:
        task = asyncio.create_task(genProcess(cookie))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())