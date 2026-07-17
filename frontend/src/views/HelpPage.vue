<template>
  <div class="page" style="padding-top: var(--spacing-section);">
    <div class="container">
      <div class="help-hero stagger-1" style="text-align: center; margin-bottom: var(--spacing-xxl);">
        <p class="mono-eyebrow">Help Center</p>
        <h1 class="display-md" style="margin-bottom: var(--spacing-md);">How can we help you?</h1>
        <p class="help-subtitle" style="color: var(--color-mute); max-width: 600px; margin: 0 auto;">Find guides, tutorials, and answers to common questions about JobFinder.</p>
      </div>

      <div class="help-content">
        <section class="help-section card stagger-2">
          <div class="section-header" style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--color-hairline);">
            <span class="section-icon badge-neutral" style="width: 40px; height: 40px; border-radius: 10px; background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: none; padding: 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
            </span>
            <h2 class="heading-sm" style="margin: 0;">Getting Started</h2>
          </div>
          <div class="section-body">
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">What is JobFinder?</h3>
              <p class="body-sm" style="color: var(--color-graphite);">JobFinder is an AI-powered job aggregation platform that collects job listings from multiple sources across Indonesia — including JobStreet, Kalibrr, Glints, Tech in Asia, LinkedIn, KitaLulus, Pintarnya, and Fastwork — into a single application. Beyond job search, it helps you improve your CV with AI analysis, build professional CVs, and get personalized career recommendations.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Use the Platform</h3>
              <p class="body-sm" style="color: var(--color-graphite);">JobFinder is designed to be intuitive. Start by searching for jobs, then use filters to narrow results. Upload your CV for AI-powered analysis, build a new CV with the CV Builder, or ask the AI Career Chatbot for personalized advice. All features are accessible from the navigation bar.</p>
            </div>
          </div>
        </section>

        <section class="help-section card stagger-2">
          <div class="section-header" style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--color-hairline);">
            <span class="section-icon badge-neutral" style="width: 40px; height: 40px; border-radius: 10px; background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: none; padding: 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            </span>
            <h2 class="heading-sm" style="margin: 0;">Job Search Guide</h2>
          </div>
          <div class="section-body">
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Search Jobs</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Navigate to the <router-link to="/jobs" style="color: var(--color-link-blue);">Jobs page</router-link> and use the search bar to find positions by keyword, job title, company name, or skill. The platform searches across all aggregated sources in real-time.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">Using Search, Filter &amp; Sorting</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Refine your results with filters in the sidebar:</p>
              <ul class="body-sm" style="color: var(--color-graphite); padding-left: 20px; margin-top: 8px;">
                <li style="margin-bottom: 4px;"><strong>Type Filter</strong> — Show only Full Time, Part Time, Internship, Freelance, Contract, Hybrid, or Remote positions</li>
                <li style="margin-bottom: 4px;"><strong>Sorting</strong> — Order results by newest, oldest, or alphabetical order</li>
                <li style="margin-bottom: 4px;"><strong>Location & Experience</strong> — Refine by location constraints and experience level</li>
              </ul>
            </div>
          </div>
        </section>

        <section class="help-section card stagger-2">
          <div class="section-header" style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--color-hairline);">
            <span class="section-icon badge-neutral" style="width: 40px; height: 40px; border-radius: 10px; background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: none; padding: 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </span>
            <h2 class="heading-sm" style="margin: 0;">CV Analyzer Guide</h2>
          </div>
          <div class="section-body">
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Upload CV</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Go to the <router-link to="/cv-analyzer" style="color: var(--color-link-blue);">CV Analyzer page</router-link> and select your file. The analysis begins automatically after upload and submission.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">Supported File Format</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Currently, the CV Analyzer supports <strong>PDF files only</strong>. Make sure your CV is saved as a PDF before uploading. Max size is 5MB.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Read ATS Score</h3>
              <p class="body-sm" style="color: var(--color-graphite);">The dashboard displays key metrics: Overall Score, ATS compatibility, Strengths, Weaknesses, Missing Skills, and AI Recommendations.</p>
            </div>
          </div>
        </section>

        <section class="help-section card stagger-2">
          <div class="section-header" style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--color-hairline);">
            <span class="section-icon badge-neutral" style="width: 40px; height: 40px; border-radius: 10px; background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: none; padding: 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            </span>
            <h2 class="heading-sm" style="margin: 0;">CV Builder Guide</h2>
          </div>
          <div class="section-body">
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Create CV</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Visit the <router-link to="/cv-builder" style="color: var(--color-link-blue);">CV Builder page</router-link> and follow the step-by-step wizard to build your personal information, education, experience, projects, certificates, skills, languages, and a professional summary.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Use AI Suggestion</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Each form field has a "✨ AI Generate" button. Click it to let AI help you write job descriptions, suggest relevant skills, or craft a professional summary.</p>
            </div>
          </div>
        </section>
        
        <section class="help-section card stagger-2">
          <div class="section-header" style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--color-hairline);">
            <span class="section-icon badge-neutral" style="width: 40px; height: 40px; border-radius: 10px; background: rgba(243, 100, 88, 0.1); color: var(--color-brand); border: none; padding: 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
            </span>
            <h2 class="heading-sm" style="margin: 0;">Telegram Bot Guide</h2>
          </div>
          <div class="section-body">
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">How to Use Telegram Bot</h3>
              <p class="body-sm" style="color: var(--color-graphite);">Search for our JobFinderBot on Telegram and start a chat. The bot provides quick access to job search, AI chat, CV tips, and the latest job updates — all without leaving Telegram.</p>
            </div>
            <div class="guide-item" style="margin-bottom: var(--spacing-lg);">
              <h3 style="font-weight: 500; margin-bottom: var(--spacing-xs);">Available Commands</h3>
              <ul class="body-sm" style="color: var(--color-graphite); padding-left: 20px; margin-top: 8px;">
                <li><code>/start</code> — Start the bot</li>
                <li><code>/search &lt;keyword&gt;</code> — Search for jobs by keyword</li>
                <li><code>/chat</code> — Enter chat mode with AI Career Assistant</li>
                <li><code>/cv</code> — Get CV writing tips</li>
                <li><code>/jobs</code> — Browse job listings</li>
                <li><code>/help</code> — Show help information</li>
              </ul>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.help-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  max-width: 800px;
  margin: 0 auto;
}
.guide-item:last-child {
  margin-bottom: 0 !important;
}
</style>
