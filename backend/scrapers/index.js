import { LinkedInScraper } from "./linkedin.js"
import { GlintsScraper } from "./glints.js"
import { JobstreetScraper } from "./jobstreet.js"
import { FastworkScraper } from "./fastwork.js"
import { PintarnyaScraper } from "./pintarnya.js"

const SCRAPERS = [
  new LinkedInScraper(),
  new GlintsScraper(),
  new JobstreetScraper(),
  new FastworkScraper(),
  new PintarnyaScraper(),
]

export async function scrapeAll() {
  const results = []
  for (const scraper of SCRAPERS) {
    try {
      const jobs = await scraper.scrape()
      results.push(...jobs)
    } catch (e) {
      console.error(`Scraper ${scraper.name} failed:`, e.message)
    }
  }
  return results
}
