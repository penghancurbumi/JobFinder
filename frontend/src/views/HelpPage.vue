<template>
  <div class="min-h-screen pt-[88px] bg-canvas-dark text-on-dark font-sans w-full max-w-[1200px] mx-auto px-xl">
    <div class="text-center mb-xxl">
      <p class="font-mono uppercase text-[13px] font-bold tracking-[1px] text-stone">Help Center</p>
      <h1 class="text-[32px] md:text-[40px] font-medium leading-[1.2] tracking-[-0.4px] text-on-dark mb-md">How can we help you?</h1>
      <p class="text-mute max-w-[600px] mx-auto text-[18px] font-normal leading-[1.56] tracking-[-0.09px]">Find guides, tutorials, and answers to common questions about JobFinder.</p>
    </div>

    <div class="flex flex-col gap-lg max-w-[800px] mx-auto">
      <section class="bg-surface-elevated rounded-[20px] p-xxl">
        <div class="flex items-center gap-md mb-lg pb-md border-b border-hairline-dark">
          <span class="w-[40px] h-[40px] rounded-[10px] bg-primary/10 text-primary flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
          </span>
          <h2 class="text-[20px] font-medium leading-[1.4] m-0 text-on-dark">Getting Started</h2>
        </div>
        <div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">What is JobFinder?</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">JobFinder is an AI-powered job aggregation platform that collects job listings from multiple sources across Indonesia — including JobStreet, Kalibrr, Glints, Tech in Asia, LinkedIn, KitaLulus, Pintarnya, and Fastwork — into a single application. Beyond job search, it helps you improve your CV with AI analysis, build professional CVs, and get personalized career recommendations.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Use the Platform</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">JobFinder is designed to be intuitive. Start by searching for jobs, then use filters to narrow results. Upload your CV for AI-powered analysis, build a new CV with the CV Builder, or ask the AI Career Chatbot for personalized advice. All features are accessible from the navigation bar.</p>
          </div>
        </div>
      </section>

      <section class="bg-surface-elevated rounded-[20px] p-xxl">
        <div class="flex items-center gap-md mb-lg pb-md border-b border-hairline-dark">
          <span class="w-[40px] h-[40px] rounded-[10px] bg-primary/10 text-primary flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          </span>
          <h2 class="text-[20px] font-medium leading-[1.4] m-0 text-on-dark">Job Search Guide</h2>
        </div>
        <div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Search Jobs</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Navigate to the <router-link to="/jobs" class="text-primary-bright no-underline hover:underline">Jobs page</router-link> and use the search bar to find positions by keyword, job title, company name, or skill. The platform searches across all aggregated sources in real-time.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">Using Search, Filter &amp; Sorting</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Refine your results with filters in the sidebar:</p>
            <ul class="text-[14px] font-normal leading-[1.5] text-on-dark-mute pl-[20px] mt-[8px] list-disc">
              <li class="mb-[4px]"><strong>Type Filter</strong> — Show only Full Time, Part Time, Internship, Freelance, Contract, Hybrid, or Remote positions</li>
              <li class="mb-[4px]"><strong>Sorting</strong> — Order results by newest, oldest, or alphabetical order</li>
              <li class="mb-[4px]"><strong>Location & Experience</strong> — Refine by location constraints and experience level</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="bg-surface-elevated rounded-[20px] p-xxl">
        <div class="flex items-center gap-md mb-lg pb-md border-b border-hairline-dark">
          <span class="w-[40px] h-[40px] rounded-[10px] bg-primary/10 text-primary flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          </span>
          <h2 class="text-[20px] font-medium leading-[1.4] m-0 text-on-dark">CV Analyzer Guide</h2>
        </div>
        <div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Upload CV</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Go to the <router-link to="/cv-analyzer" class="text-primary-bright no-underline hover:underline">CV Analyzer page</router-link> and select your file. The analysis begins automatically after upload and submission.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">Supported File Format</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Currently, the CV Analyzer supports <strong>PDF files only</strong>. Make sure your CV is saved as a PDF before uploading. Max size is 5MB.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Read ATS Score</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">The dashboard displays key metrics: Overall Score, ATS compatibility, Strengths, Weaknesses, Missing Skills, and AI Recommendations.</p>
          </div>
        </div>
      </section>

      <section class="bg-surface-elevated rounded-[20px] p-xxl">
        <div class="flex items-center gap-md mb-lg pb-md border-b border-hairline-dark">
          <span class="w-[40px] h-[40px] rounded-[10px] bg-primary/10 text-primary flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          </span>
          <h2 class="text-[20px] font-medium leading-[1.4] m-0 text-on-dark">CV Builder Guide</h2>
        </div>
        <div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Create CV</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Visit the <router-link to="/cv-builder" class="text-primary-bright no-underline hover:underline">CV Builder page</router-link> and follow the step-by-step wizard to build your personal information, education, experience, projects, certificates, skills, languages, and a professional summary.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Use AI Suggestion</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Each form field has a "✨ AI Generate" button. Click it to let AI help you write job descriptions, suggest relevant skills, or craft a professional summary.</p>
          </div>
        </div>
      </section>
      
      <section class="bg-surface-elevated rounded-[20px] p-xxl mb-xl">
        <div class="flex items-center gap-md mb-lg pb-md border-b border-hairline-dark">
          <span class="w-[40px] h-[40px] rounded-[10px] bg-primary/10 text-primary flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
          </span>
          <h2 class="text-[20px] font-medium leading-[1.4] m-0 text-on-dark">Telegram Bot Guide</h2>
        </div>
        <div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">How to Use Telegram Bot</h3>
            <p class="text-[14px] font-normal leading-[1.5] text-on-dark-mute">Search for our JobFinderBot on Telegram and start a chat. The bot provides quick access to job search, AI chat, CV tips, and the latest job updates — all without leaving Telegram.</p>
          </div>
          <div class="mb-lg last:mb-0">
            <h3 class="font-medium mb-xs text-[16px] text-on-dark">Available Commands</h3>
            <ul class="text-[14px] font-normal leading-[1.5] text-on-dark-mute pl-[20px] mt-[8px] list-disc">
              <li class="mb-[4px]"><code>/start</code> — Start the bot</li>
              <li class="mb-[4px]"><code>/search &lt;keyword&gt;</code> — Search for jobs by keyword</li>
              <li class="mb-[4px]"><code>/chat</code> — Enter chat mode with AI Career Assistant</li>
              <li class="mb-[4px]"><code>/cv</code> — Get CV writing tips</li>
              <li class="mb-[4px]"><code>/jobs</code> — Browse job listings</li>
              <li class="mb-[4px]"><code>/help</code> — Show help information</li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
</script>
