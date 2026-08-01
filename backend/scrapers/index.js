import { exec } from "child_process"
import fs from "fs/promises"
import path from "path"
import util from "util"
import { runQuery } from "../db.js"

const execPromise = util.promisify(exec)

const SCRAPY_PROJECT_DIR = path.join(process.cwd(), "scrapping-job")
const EXPORTS_DIR = path.join(SCRAPY_PROJECT_DIR, "exports", "json")
const ARCHIVE_DIR = path.join(EXPORTS_DIR, "archive")

export async function insertScrapedFiles(jobTypeFilter) {
  let count = 0
  
  // Ensure archive directory exists
  await fs.mkdir(ARCHIVE_DIR, { recursive: true })
  
  try {
    const files = await fs.readdir(EXPORTS_DIR)
    const jsonFiles = files.filter(f => f.endsWith(".json"))
    
    for (const file of jsonFiles) {
      const filePath = path.join(EXPORTS_DIR, file)
      try {
        const content = await fs.readFile(filePath, "utf-8")
        const scrapedItems = JSON.parse(content)
        
        for (const item of scrapedItems) {
          let salary = ""
          if (item.salary_min || item.salary_max) {
            const currency = item.salary_currency || "IDR"
            if (item.salary_min && item.salary_max) {
              salary = `${currency} ${item.salary_min.toLocaleString()} - ${item.salary_max.toLocaleString()}`
            } else if (item.salary_min) {
              salary = `${currency} ${item.salary_min.toLocaleString()}`
            }
          }
          
          const expertise = item.skills && item.skills.length > 0 ? item.skills.slice(0, 3).join(", ") : "Others"
          const postedDate = item.updated_at ? item.updated_at.substring(0, 10) : new Date().toISOString().substring(0, 10)
          
          // Insert into SQLite, refreshing type/description/salary on duplicate URL
          const query = `
            INSERT INTO jobs 
            (title, company, location, jobType, workType, expertise, source, url, description, postedDate, deadlineDate, salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
              jobType = CASE WHEN excluded.jobType != 'Full-time' THEN excluded.jobType ELSE jobType END,
              workType = CASE WHEN excluded.workType != 'On-site' THEN excluded.workType ELSE workType END,
              description = CASE WHEN excluded.description != '' THEN excluded.description ELSE description END,
              salary = CASE WHEN excluded.salary != '' THEN excluded.salary ELSE salary END,
              postedDate = excluded.postedDate
          `
          const params = [
            item.title || "Unknown Title",
            item.company_name || "Unknown Company",
            item.location || "Remote",
            item.job_type || "Full-time",
            item.work_type || "On-site",
            expertise,
            item.platform || "Scraper",
            item.source_url || "",
            item.description || "",
            postedDate,
            null, // deadlineDate
            salary
          ]
          
          const res = await runQuery(query, params)
          if (res.changes > 0) count++
        }
        
        // Move to archive so we don't read it again
        const archivePath = path.join(ARCHIVE_DIR, file)
        await fs.rename(filePath, archivePath)
        
      } catch (err) {
        console.error(`Error processing file ${file}:`, err.message)
      }
    }
  } catch(e) {
    console.error("Error reading exports:", e.message)
  }
  
  return count
}

export async function scrapeAll() {
  console.log("Starting Python Scrapy jobs for 5 job types...")
  
  const jobTypes = [
    { type: "fulltime", cmd: "python -m scrapy crawl_all -a job_type=fulltime -a max_pages=3" },
    { type: "parttime", cmd: "python -m scrapy crawl_all -a job_type=parttime -a max_pages=3" },
    { type: "intern", cmd: "python -m scrapy crawl_all -a job_type=internship -a max_pages=3" },
    { type: "hybrid", cmd: "python -m scrapy crawl_all -a work_type=hybrid -a max_pages=3" },
    { type: "freelance", cmd: "python -m scrapy crawl_all -a job_type=contract -a max_pages=3" }
  ]
  
  let totalNew = 0
  
  for (const jt of jobTypes) {
    console.log(`Scraping category: ${jt.type}...`)
    try {
      await execPromise(jt.cmd, { cwd: SCRAPY_PROJECT_DIR, timeout: 120000 })
      const added = await insertScrapedFiles(jt.type)
      console.log(`=> Added ${added} new ${jt.type} jobs to database.`)
      totalNew += added
    } catch (e) {
      console.error(`Scrape failed for ${jt.type}:`, e.message)
    }
  }

  console.log(`Scrapy execution completed. Total new jobs added: ${totalNew}`)
  return totalNew 
}
