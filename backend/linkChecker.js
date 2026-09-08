// Link health checker: verifies that stored job URLs still resolve (not 404).
// Per URL: HEAD request first (cheap), fallback to GET when HEAD is rejected
// (many job boards answer 403/405 to HEAD). A browser-like User-Agent is used
// because job boards commonly block the default fetch UA.
//
// Results:
//   active    – 2xx after redirects AND page content doesn't look closed
//   not_found – 404/410, or 200 whose page text shows the listing is closed
//               (many boards return 200 with a "closed" page instead of 404)
//   unknown   – bot-blocked (401/403/429), 5xx, timeout, network failure —
//               inconclusive, never treated as dead

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

// Mirror of job_scraper/constants.py CLOSED_MARKERS (general list), matched
// against stripped page text. If any marker appears, the listing is closed
// even though HTTP says 200.
const CLOSED_MARKERS = [
  "lowongan telah ditutup",
  "lowongan ini telah ditutup",
  "lowongan ditutup",
  "lowongan telah berakhir",
  "lowongan ini telah berakhir",
  "tidak menerima lamaran",
  "posisi telah ditutup",
  "lowongan ini tidak tersedia",
  "position closed",
  "this position has been closed",
  "this position is closed",
  "job closed",
  "this job is closed",
  "this job has been closed",
  "no longer accepting applications",
  "not accepting applications",
  "no longer available",
  "position is no longer available",
  "this position is no longer available",
  "job is no longer available",
  "this job is no longer available",
  "vacancy closed",
  "this vacancy has been filled",
  "application closed",
  "jobclosedheader",
]

const TAG_RE = /<[^>]+>/g
const SCRIPT_STYLE_RE = /<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi

// Cheap "closed page" detection: strip scripts/styles/tags, lowercase, look
// for a marker. Bounded to the first 60 KB of body text for speed.
export function hasClosedContent(html) {
  if (!html) return false
  const text = String(html)
    .replace(SCRIPT_STYLE_RE, " ")
    .replace(TAG_RE, " ")
    .toLowerCase()
  const slice = text.slice(0, 60000)
  return CLOSED_MARKERS.some((m) => slice.includes(m))
}

export async function checkUrl(url, timeoutMs = 10000) {
  if (!url || !/^https?:\/\//i.test(String(url))) return "unknown"
  for (const method of ["HEAD", "GET"]) {
    const ctrl = new AbortController()
    const timer = setTimeout(() => ctrl.abort(), timeoutMs)
    try {
      const res = await fetch(url, {
        method,
        redirect: "follow",
        signal: ctrl.signal,
        headers: {
          "User-Agent": UA,
          Accept: "text/html,application/xhtml+xml,*/*;q=0.8",
        },
      })
      if (res.ok) {
        // HEAD can't inspect content; a 200 from HEAD is provisionally active.
        // GET inspects the body for closed-page markers (boards return 200 for
        // closed listings instead of 404).
        if (method === "GET") {
          try {
            const body = await res.text()
            if (hasClosedContent(body)) return "not_found"
          } catch { /* body read failure → trust the 200 */ }
        }
        return "active"
      }
      if (res.status === 404 || res.status === 410) return "not_found"
      // 403/405 on HEAD → retry with GET; anything else is inconclusive
      if (res.status !== 403 && res.status !== 405) return "unknown"
    } catch {
      // network error / timeout → try GET once, else unknown
    } finally {
      clearTimeout(timer)
    }
  }
  return "unknown"
}

// Runs checkUrl over a list of jobs with bounded concurrency. onProgress is
// awaited per job (may perform DB writes / socket emissions).
export async function checkJobsBatch(jobs, { concurrency = 6, onProgress } = {}) {
  const results = []
  let idx = 0
  let done = 0

  async function worker() {
    while (idx < jobs.length) {
      const job = jobs[idx++]
      const status = await checkUrl(job.url)
      results.push({ url: job.url, status })
      done++
      try {
        await onProgress?.({ done, total: jobs.length, url: job.url, status })
      } catch {
        /* progress failure must not abort the run */
      }
    }
  }

  await Promise.all(
    Array.from({ length: Math.max(Math.min(concurrency, jobs.length), 1) }, worker)
  )
  return results
}
