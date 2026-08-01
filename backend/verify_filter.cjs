const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('jobs.sqlite', sqlite3.OPEN_READONLY);
db.all("SELECT jobType, COUNT(*) c FROM jobs WHERE source IN ('jobstreet','kitalulus','pintarnya') GROUP BY jobType ORDER BY c DESC", (e, r) => {
  console.log('== jobType (3 spider) ==');
  if (e) console.log(e.message); else r.forEach(x => console.log('  ' + JSON.stringify(x.jobType) + ' = ' + x.c));
});
db.all("SELECT workType, COUNT(*) c FROM jobs WHERE source IN ('jobstreet','kitalulus','pintarnya') GROUP BY workType ORDER BY c DESC", (e, r) => {
  console.log('== workType (3 spider) ==');
  if (e) console.log(e.message); else r.forEach(x => console.log('  ' + JSON.stringify(x.workType) + ' = ' + x.c));
});
const tests = {
  'total': "SELECT COUNT(*) c FROM jobs",
  'onsite': "SELECT COUNT(*) c FROM jobs WHERE REPLACE(LOWER(workType),'-','') LIKE '%onsite%'",
  'remote': "SELECT COUNT(*) c FROM jobs WHERE REPLACE(LOWER(workType),'-','') LIKE '%remote%'",
  'hybrid': "SELECT COUNT(*) c FROM jobs WHERE REPLACE(LOWER(workType),'-','') LIKE '%hybrid%'",
  'fulltime': "SELECT COUNT(*) c FROM jobs WHERE LOWER(jobType) LIKE '%full%time%'",
  'parttime': "SELECT COUNT(*) c FROM jobs WHERE LOWER(jobType) LIKE '%part%time%'",
  'contract': "SELECT COUNT(*) c FROM jobs WHERE LOWER(jobType) LIKE '%contract%'",
  'freelance': "SELECT COUNT(*) c FROM jobs WHERE LOWER(jobType) LIKE '%freelance%'",
  'intern': "SELECT COUNT(*) c FROM jobs WHERE LOWER(jobType) LIKE '%intern%'",
};
db.all("SELECT 1", () => {
  for (const [k, q] of Object.entries(tests)) {
    db.all(q, (e, r) => console.log(k + ': ' + (r && r[0].c) + ' jobs' + (e ? ' ERR ' + e.message : '')));
  }
});
