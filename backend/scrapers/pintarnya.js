export class PintarnyaScraper {
  get name() { return "Pintarnya" }

  async scrape() {
    return [
      { title: "Cyber Security Analyst", company: "SecureNet", location: "Jakarta", jobType: "job", expertise: "Cyber Security", source: "Pintarnya", url: "https://pintarnya.com/lowongan", description: "Security monitoring and vulnerability assessment", postedDate: "2026-07-11", deadlineDate: "2026-08-11" },
      { title: "AI/ML Intern", company: "AIInnovate", location: "Yogyakarta", jobType: "intern", expertise: "AI / Machine Learning", source: "Pintarnya", url: "https://pintarnya.com/lowongan", description: "Machine learning model development and training", postedDate: "2026-07-05", deadlineDate: "2026-07-31" },
      { title: "Product Manager", company: "TechProduct", location: "Jakarta", jobType: "job", expertise: "Product Management", source: "Pintarnya", url: "https://pintarnya.com/lowongan", description: "Product strategy, roadmap, and stakeholder management", postedDate: "2026-07-08", deadlineDate: "2026-08-08" },
    ]
  }
}
