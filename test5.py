from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    # Example: ignore all links, don't escape HTML, and wrap text at 80 characters
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80
        }
    )

    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com/docs", config=config)
        if result.success:
            md = result.markdown 
            with open("output.md", "w", encoding="utf-8") as f:
                f.write(md)
            print("Markdown:\n", result.markdown[:500])  # Just a snippet
        else:
            print("Crawl failed:", result.error_message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
