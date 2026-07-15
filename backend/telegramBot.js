import "dotenv/config"
import TelegramBot from "node-telegram-bot-api"
import { chat } from "./chatbot.js"

const TOKEN = process.env.TELEGRAM_BOT_TOKEN

export function runBot() {
  if (!TOKEN || TOKEN === "your_telegram_bot_token_here") {
    console.log("Telegram bot not configured — skipping")
    return
  }

  const bot = new TelegramBot(TOKEN, { polling: true })

  bot.onText(/\/start|\/help/, (msg) => {
    bot.sendMessage(msg.chat.id,
      "👋 Welcome to Job & Intern Finder Bot!\n\n" +
      "Commands:\n" +
      "/jobs - Browse job listings\n" +
      "/internships - Browse internships\n" +
      "/cv - CV analysis tips\n" +
      "/search [area] - Search jobs by expertise\n" +
      "/chat - Chat with AI assistant\n" +
      "/help - Show this message"
    )
  })

  bot.onText(/\/jobs|\/internships/, (msg) => {
    bot.sendMessage(msg.chat.id,
      "📋 *Listings*\n\n" +
      "Available expertise areas:\n" +
      "- IT Infra\n- Software Development\n- Graphic Design\n" +
      "- Data Science\n- UI/UX Design\n- Digital Marketing\n" +
      "- Cyber Security\n- AI/ML\n\n" +
      "Try: /search Software Development\n" +
      "Or visit our web app for full results."
    )
  })

  bot.onText(/\/search (.+)/, (msg, match) => {
    const query = match[1]
    bot.sendMessage(msg.chat.id, `🔍 Searching for jobs in '${query}'...\n\nFor full results with filters, visit our website.`)
  })

  bot.onText(/\/cv/, (msg) => {
    bot.sendMessage(msg.chat.id,
      "📄 *CV Tips*\n\n" +
      "1. Use ATS-friendly format (simple, clean layout)\n" +
      "2. Include keywords from the job description\n" +
      "3. Use action verbs and metrics\n" +
      "4. Keep it to 1-2 pages\n" +
      "5. Save as PDF\n\n" +
      "Visit our web app for CV analysis and builder!"
    )
  })

  bot.onText(/\/chat/, (msg) => {
    bot.sendMessage(msg.chat.id, "💬 Chat mode! Ask me anything about jobs, career, or CV tips. Send /done to exit.")
    global.telegramChatMode = global.telegramChatMode || {}
    global.telegramChatMode[msg.chat.id] = true
  })

  bot.onText(/\/done/, (msg) => {
    global.telegramChatMode = global.telegramChatMode || {}
    if (global.telegramChatMode[msg.chat.id]) {
      delete global.telegramChatMode[msg.chat.id]
      bot.sendMessage(msg.chat.id, "Exited chat mode.")
    }
  })

  bot.on("message", async (msg) => {
    global.telegramChatMode = global.telegramChatMode || {}
    if (!global.telegramChatMode[msg.chat.id]) return
    if (msg.text?.startsWith("/")) return

    const reply = await chat(msg.text, [])
    bot.sendMessage(msg.chat.id, reply.slice(0, 4000))
  })

  console.log("Telegram bot running...")
}
