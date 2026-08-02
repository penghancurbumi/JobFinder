import { createApp } from "vue"
import App from "./App.vue"
import router from "./router/index.js"
import "./assets/style.css"
import { createHead } from "@vueuse/head"

const app = createApp(App)
const head = createHead()

app.use(router).use(head).mount("#app")


