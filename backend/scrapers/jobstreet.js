export class JobstreetScraper {
  get name() { return "Jobstreet" }

  async scrape() {
    return [
      { title: "Frontend Developer Intern", company: "StartupXYZ", location: "Jakarta", jobType: "intern", expertise: "Software Development", source: "Jobstreet", url: "https://www.jobstreet.co.id/id/job-search/frontend-jobs/", description: "Frontend development with Vue.js", postedDate: "2026-07-01", deadlineDate: "2026-08-05" },
      { title: "DevOps Engineer", company: "CloudTech", location: "Jakarta", jobType: "job", expertise: "DevOps", source: "Jobstreet", url: "https://www.jobstreet.co.id/id/job-search/devops-jobs/", description: "CI/CD pipelines and cloud infrastructure", postedDate: "2026-07-12", deadlineDate: "2026-08-12" },
      { title: "Digital Marketing Intern", company: "MarketHub", location: "Bandung", jobType: "intern", expertise: "Digital Marketing", source: "Jobstreet", url: "https://www.jobstreet.co.id/id/job-search/digital-marketing-jobs/", description: "Social media and SEO marketing campaigns", postedDate: "2026-07-14", deadlineDate: "2026-08-30" },
    ]
  }
}
