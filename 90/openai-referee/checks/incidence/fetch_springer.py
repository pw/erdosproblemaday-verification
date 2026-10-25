import sys, asyncio
from playwright.async_api import async_playwright
url, out = sys.argv[1], sys.argv[2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(accept_downloads=True, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
        page = await ctx.new_page()
        got = {}
        async def on_resp(r):
            ct = r.headers.get("content-type","")
            if "pdf" in ct:
                try:
                    got['b'] = await r.body()
                except Exception as e:
                    print("body err", e)
        page.on("response", on_resp)
        try:
            async with page.expect_download(timeout=45000) as dl:
                try:
                    await page.goto(url, timeout=45000)
                except Exception as e:
                    print("goto:", e)
            d = await dl.value
            await d.save_as(out); print("download saved")
        except Exception as e:
            print("no download:", e)
            await page.wait_for_timeout(8000)
            if 'b' in got:
                open(out,'wb').write(got['b']); print("pdf body saved", len(got['b']))
            else:
                print((await page.content())[:500])
        await b.close()
asyncio.run(main())
