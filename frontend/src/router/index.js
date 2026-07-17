import { createRouter, createWebHistory } from "vue-router"
import HomePage from "../views/HomePage.vue"
import JobsPage from "../views/JobsPage.vue"
import CVAnalyzerPage from "../views/CVAnalyzerPage.vue"
import CVBuilderPage from "../views/CVBuilderPage.vue"
import ChatbotPage from "../views/ChatbotPage.vue"
import HelpPage from "../views/HelpPage.vue"

const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/jobs", name: "Jobs", component: JobsPage },
  { path: "/cv-analyzer", name: "CVAnalyzer", component: CVAnalyzerPage },
  { path: "/cv-builder", name: "CVBuilder", component: CVBuilderPage },
  { path: "/chatbot", name: "Chatbot", component: ChatbotPage },
  { path: "/help", name: "Help", component: HelpPage },
]

export default createRouter({ history: createWebHistory(), routes })
