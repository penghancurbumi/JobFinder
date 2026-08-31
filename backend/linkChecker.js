// Link health checker: verifies that stored job URLs still resolve (not 404).
// Per URL: HEAD request first (cheap), fallback to GET when HEAD is rejected
// (many job boards answer 403/405 to HEAD). A browser-like User-Agent is used
// because job boards commonly block the default fetch UA.
//
// Results:
//   active    – 2xx after redirects
//   not_found – 404/410 (listing definitively gone)
//   unknown   – bot-blocked (401/403/429), 5xx, timeout, network failure —
//               inconclusive, never treated as dead

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

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
      if (res.ok) return "active"
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
