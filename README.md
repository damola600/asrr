# ☾ ASRR — Islamic Calendar & Prayer Scheduling Platform

**ASRR** is a full-stack SaaS web application that helps Muslims integrate daily prayers, Sunnah practices, voluntary fasting, and important Islamic dates into Google Calendar.

Built to make Islamic scheduling more accessible, ASRR automates personalized calendar reminders while giving users control over their religious schedules.

🌐 **[Visit ASRR](https://asrr-seven.vercel.app/)**

## About ASRR

Managing daily prayers, fasting schedules, and Islamic events alongside work, school, and personal responsibilities can be challenging.

ASRR addresses this by connecting Islamic scheduling with Google Calendar, allowing users to manage their religious commitments within the calendar they already use.

Users can create an account, configure their location and preferences, connect Google Calendar, and automatically synchronize their selected events.

The platform is designed for real-world use, with a focus on automation, personalization, reliability, and scalability.

## Key Features

### 🕌 Personalized Prayer Scheduling
- Automatically generates calendar events for Fajr, Dhuhr, Asr, Maghrib, and Isha.
- Supports location-based prayer times and Madhab preferences.
- Updates prayer schedules when relevant settings change.
- Allows users to enable or disable prayer synchronization.

### 🌙 Sunnah & Islamic Reminders
- Monday and Thursday voluntary fasting
- White Days, Arafah, Ashura, and other fasting occasions
- Tahajjud and Duha prayers
- Morning and evening Adhkar
- Surah Al-Kahf and Al-Mulk reminders
- Important Islamic dates and occasions

Users can customize which reminders appear in their calendars.

### 📅 Google Calendar Integration
- Secure Google OAuth 2.0 authorization
- Automated event creation and updates
- Preference-based event deletion
- Synchronization tracking to manage existing events
- Background synchronization processing

### 🔄 Automated Islamic Calendar Management
- Hijri-to-Gregorian calendar mapping
- Recurring Islamic event generation
- Calendar initialization and refresh workflows
- Support for changing prayer times and personalized schedules

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Backend | Python, Django REST Framework |
| Database | PostgreSQL |
| Background Jobs | Celery, Redis |
| Authentication | Django Authentication, Google OAuth 2.0 |
| Integrations | Google Calendar API |
| Deployment | Vercel, Render |

## System Architecture

```text
                  ASRR Web Application
                           |
                    Next.js Frontend
                           |
                    Django REST API
                           |
           +---------------+---------------+
           |               |               |
       PostgreSQL      Celery/Redis     Google OAuth
           |               |               |
     User Profiles     Async Tasks     Google Calendar
     Prayer Times           |               API
     Hijri Calendar    Calendar Sync
     Event Records
```

ASRR uses a decoupled frontend and backend architecture. Django REST Framework manages application logic and user preferences, PostgreSQL provides persistent storage, and Celery handles asynchronous synchronization with Google Calendar.

## Engineering & Technical Highlights

**Full-Stack Application Development**

Designed and developed a complete web application using Next.js, TypeScript, Django, and PostgreSQL, including authentication, account configuration, REST APIs, and personalized dashboards.

**External API Integration**

Integrated Google OAuth 2.0 and the Google Calendar API to support user-authorized calendar operations and automated event management.

**Asynchronous Processing**

Implemented Celery and Redis to execute calendar synchronization tasks outside HTTP request handling, improving responsiveness during API-intensive operations.

**Calendar Synchronization Engine**

Developed backend logic to track synchronized events, identify scheduling changes, update existing Google Calendar entries, and remove events when users disable specific preferences.

**Recurring Event Generation**

Built scheduling services that combine Hijri calendar rules, Gregorian dates, prayer-time data, and individual user preferences to generate personalized recurring events.

## Product Development

ASRR is being developed as a user-facing SaaS platform rather than a demonstration-only application.

Development priorities include:

- Reliable and scalable calendar synchronization
- User-controlled prayer and Sunnah scheduling
- Secure account and Google Calendar integration
- Automated calendar maintenance
- Responsive and accessible user interfaces
- Monitoring and recovery from synchronization failures

## Application

**Website:** https://asrr-seven.vercel.app/

Users can create an account, configure their preferences, and connect Google Calendar to begin using ASRR.

*Google Calendar integration may be subject to Google's OAuth verification requirements during rollout.*

## Project Status

**Active Development — Preparing for Broader Public Use**

ASRR is independently designed and developed, with ongoing improvements to functionality, reliability, and the user experience.

## Ownership

ASRR is a proprietary software project. The source code and associated intellectual property are not offered under an open-source license.

**© 2026 ASRR. All rights reserved.**

---

### ☾ ASRR
*Make time for what matters.*
