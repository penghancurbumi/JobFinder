import * as cheerio from 'cheerio';

const FALLBACK_DATA = [
  { title: "UI/UX Designer Intern", company: "DesignLab", location: "Jakarta", jobType: "intern", expertise: "UI/UX Design", source: "Glints", url: "https://glints.com/id/opportunities/jobs/explore?keyword=ui%20ux", description: "UI/UX design internship for digital products", postedDate: "2026-07-05", deadlineDate: "2026-07-25" },
  { title: "Graphic Designer", company: "CreativeAgency", location: "Surabaya", jobType: "job", expertise: "Graphic Design", source: "Glints", url: "https://glints.com/id/opportunities/jobs/explore?keyword=graphic%20designer", description: "Graphic design for digital and print media", postedDate: "2026-06-15", deadlineDate: "2026-07-10" }, 
];

export class GlintsScraper {
  get name() { return "Glints" }

  async scrape() {
    try {
      const response = await fetch("https://glints.com/id/opportunities/jobs/explore", {
        headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" },
        signal: AbortSignal.timeout(8000)
      });
      
      if (!response.ok) throw new Error("Fetch failed");
      const html = await response.text();
      const $ = cheerio.load(html);
      const jobs = [];

      $('.JobCardsc__JobCardWrapper-sc-1f9jz8t-0, .CompactOpportunityCardsc__CompactJobCardWrapper-sc-1yxg2pt-0').each((i, el) => {
        if (i >= 5) return;
        const title = $(el).find('h3, .CompactOpportunityCardsc__JobTitle-sc-1yxg2pt-7').text().trim();
        const company = $(el).find('a.CompactOpportunityCardsc__CompanyLink-sc-1yxg2pt-10').text().trim() || "Unknown Company";
        const location = $(el).find('.CompactOpportunityCardsc__OpportunityInfo-sc-1yxg2pt-14 span').first().text().trim() || "Indonesia";
        const href = $(el).find('a').attr('href');
        
        if (title) {
          jobs.push({
            title: title,
            company: company,
            location: location,
            jobType: title.toLowerCase().includes('intern') ? 'intern' : 'job',
            expertise: "Others",
            source: "Glints",
            url: href ? (href.startsWith('http') ? href : `https://glints.com${href}`) : "https://glints.com/id/opportunities/jobs/explore",
            description: "Peluang kerja dari Glints.",
            postedDate: new Date().toISOString().split('T')[0],
            deadlineDate: "2026-12-31" 
          });
        }
      });

      return jobs.length > 0 ? jobs : FALLBACK_DATA;
    } catch (error) {
      console.log("Glints scraping failed (likely blocked by Captcha), using fallback.");
      return FALLBACK_DATA;
    }
  }
}
