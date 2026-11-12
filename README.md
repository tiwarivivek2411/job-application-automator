# 🤖 Job Application Automator

A comprehensive automated application engine designed to stream, fill, and submit applications across multiple tech hiring platforms and Applicant Tracking Systems (ATS).

## 🌐 Supported Platforms & ATS
- **Hiring Platforms**: Weekday, Wellfound, Instahyre, Talent500, Cutshort, Naukri
- **Applicant Tracking Systems (ATS)**: Ashby, Greenhouse, Lever, Workable
- **Direct Company Portals**: Automated forms for Gitlab, Abnormal Security, and custom company careers pages

## ⚡ Features
- Multi-step form auto-filling (education, experience, custom dropdowns, radios)
- Automated resume file attachment via OSAScript / Playwright / Chrome DevTools
- Paginated streaming application workflows with rate limiting and guardrails
- Application tracking and deduplication

## 🚀 Quick Start
1. Copy `candidate_profile.example.json` to `candidate_profile.json` and update your details:
   ```bash
   cp candidate_profile.example.json candidate_profile.json
   ```
2. Run platform-specific stream runners:
   ```bash
   python weekday_software_roles_runner.py
   python wellfound_auto_applicant.py
   python apply_instahyre_stream.py
   ```
