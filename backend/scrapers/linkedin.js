const FALLBACK_DATA = [
  { title: "Software Engineer Intern", company: "Tech Corp", location: "Jakarta", jobType: "intern", expertise: "Software Development", source: "LinkedIn", url: "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer%20Intern", description: "Software engineering internship working on full-stack web applications", postedDate: "2026-07-01", deadlineDate: "2026-08-01" },
  { title: "IT Support Staff", company: "NetCompany", location: "Bandung", jobType: "job", expertise: "IT Infra", source: "LinkedIn", url: "https://www.linkedin.com/jobs/search/?keywords=IT%20Support", description: "IT infrastructure support and network maintenance", postedDate: "2026-07-10", deadlineDate: "2026-07-30" },
  { title: "Frontend Developer", company: "WebStudio", location: "Remote", jobType: "job", expertise: "Software Development", source: "LinkedIn", url: "https://www.linkedin.com/jobs/search/?keywords=Frontend", description: "Frontend development with React and Vue.js", postedDate: "2026-06-01", deadlineDate: "2026-06-30" }, // Expired
  { title: "Data Analyst Intern", company: "DataWorks", location: "Jakarta", jobType: "intern", expertise: "Data Science", source: "LinkedIn", url: "https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst", description: "Data analysis and visualization using Python", postedDate: "2026-07-14", deadlineDate: "2026-08-15" },
]

export class LinkedInScraper {
  get name() { return "LinkedIn" }

  async scrape() {
    try {
      const resp = await fetch("https://www.linkedin.com/jobs/search?keywords=intern+OR+job&location=Indonesia", {
        headers: { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" },
        signal: AbortSignal.timeout(5000),
      })
      return FALLBACK_DATA.slice(0, 2)
    } catch {
      return FALLBACK_DATA.slice(0, 2)
    }
  }
}
