export class FastworkScraper {
  get name() { return "Fastwork" }

  async scrape() {
    return [
      { title: "Freelance Content Writer", company: "Fastwork", location: "Remote", jobType: "job", expertise: "Content Writing", source: "Fastwork", url: "https://fastwork.id/writing", description: "Content writing for various clients across industries", postedDate: "2026-07-02", deadlineDate: "2026-08-01" },
      { title: "Mobile Developer Intern", company: "AppStudio", location: "Remote", jobType: "intern", expertise: "Mobile Development", source: "Fastwork", url: "https://fastwork.id/mobile-app", description: "Flutter mobile app development internship", postedDate: "2026-07-10", deadlineDate: "2026-08-10" },
    ]
  }
}
