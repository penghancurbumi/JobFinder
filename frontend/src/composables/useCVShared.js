import axios from 'axios'

export const MONTHS = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]

const currentYearNum = new Date().getFullYear()
export const YEARS = []
for (let y = currentYearNum + 5; y >= 1990; y--) { YEARS.push(y) }

export function isPeriodValid(startMonth, startYear, endMonth, endYear) {
  if (!startMonth || !startYear || !endMonth || !endYear) return true
  const sy = Number(startYear), ey = Number(endYear)
  if (ey < sy) return false
  if (ey === sy) return MONTHS.indexOf(endMonth) >= MONTHS.indexOf(startMonth)
  return true
}

export function formatGPA(val) {
  const num = parseFloat(val)
  return isNaN(num) ? val : num.toFixed(2)
}

export async function getSuggestion(fieldLabel, expertise) {
  try {
    const { data } = await axios.post('/api/cv/suggestion', { fieldLabel, expertise })
    return data.suggestion
  } catch {
    return `Saran: Buat agar relevan dengan posisi ${expertise}.`
  }
}
