# Progress ledger — hapus langsung lowongan ditutup

Plan: `docs/superpowers/plans/2026-08-12-delete-closed-jobs.md`
Spec: `docs/superpowers/specs/2026-08-12-delete-closed-jobs-design.md`
Base commit for this plan: `77632b8`

- [ ] Task 1: Bersihkan schema + helper (db.js)
- [ ] Task 2: deleteClosedJobs di scrapers/index.js
- [ ] Task 3: hapus showClosed/closedCount di server.js
- [ ] Task 4: hapus toggle/badge di JobsPage.vue
- [ ] Task 5: verifikasi end-to-end + cleanup

(Old "mark-closed" plan is superseded by this plan; its commits remain in history.)
Task 1: complete (commits 77632b8..cf64047, review clean; DELETE byUrls preserved, markClosedUrls removed, drop-migration verified)
Task 2: complete (commits cf64047..097e669, review clean; Minor backlog: [T2] komentar runCleanup masih 'Flag jobs...' ketinggalan dari edit)
Task 3: complete (commits 097e669..99cdb3c, review clean; all call sites verified no showClosed residue)
Task 4: complete (commits 99cdb3c..5781832, review clean; Minor backlog: [T4] indentasi </aside> berubah 2->10 spasi, kosmetik)
Task 5: complete (this commit; syntax OK, unittest 5/5 OK, scrape sim shows removedClosed no closedMarked, API has no closedCount + showClosed inert, grep 3 benign hits in db.js drop-migration + kitalulus.py source-field; temp script removed)
Task 5: complete (commits 5781832..871e826, review clean; Minor backlog: [T5] heading report bilang '2 hit benign' tapi 3, no trailing newline, BOM di progress.md)
