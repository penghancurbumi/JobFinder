const { io } = require('socket.io-client')
const socket = io('http://localhost:3000', { transports: ['websocket'] })
const events = []
let startedAt = 0
let categoryStarts = new Set()
let categoryDone = new Set()

socket.on('connect', () => {
  console.log('[client] connected, emitting request-scrape')
  startedAt = Date.now()
  socket.emit('request-scrape')
})
socket.on('scrape-progress', (evt) => {
  events.push(evt)
  if (evt.status === 'category-start') categoryStarts.add(evt.category)
  if (evt.status === 'category-done') categoryDone.add(evt.category)
  if (evt.status === 'done') {
    const elapsed = ((Date.now() - startedAt) / 1000).toFixed(0)
    console.log(`\n=== SCRAPE FINISHED in ${elapsed}s (${(elapsed / 60).toFixed(1)} min) ===`)
    console.log(`categories started: ${[...categoryStarts].join(', ')}`)
    console.log(`categories done:    ${[...categoryDone].join(', ')}`)
    console.log(`progress events:    ${events.length}`)
    const cats = {}
    events.forEach((e) => { if (e.category && e.spider && e.status === 'done') { cats[e.category] = cats[e.category] || {}; cats[e.category][e.spider] = e.items } })
    for (const [c, sp] of Object.entries(cats)) {
      const total = Object.values(sp).reduce((a, b) => a + b, 0)
      console.log(`  ${c.padEnd(9)} spiders=${Object.keys(sp).length}/7 items=${total}`)
    }
    process.exit(0)
  }
})
socket.on('scrape-status', (s) => {
  if (s.status === 'scraping') console.log('[status] scraping started')
})
socket.on('jobs-updated', (d) => console.log(`[jobs-updated] total=${d.total}`))
socket.on('connect_error', (e) => { console.error('[error]', e.message); process.exit(1) })
socket.on('error', (e) => console.error('[socket error]', e && e.message))

setTimeout(() => { console.log('[TIMEOUT] 600s reached'); process.exit(2) }, 600000)
