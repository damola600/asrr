# ☾ ASRR — Islamic Calendar & Prayer Scheduling Platform

**ASRR** is a full-stack web application that integrates Islamic prayer times, Sunnah practices, and important Islamic dates directly into Google Calendar.

The platform allows users to personalize their religious schedules, automate calendar event creation, and keep reminders synchronized as their preferences or prayer times change.

**Live Application:** [ASRR](https://asrr-seven.vercel.app/)

## Overview

ASRR was developed to solve a practical scheduling challenge: integrating daily Islamic practices into the digital calendars people already use.

Rather than requiring users to manually create recurring prayer reminders, fasting schedules, and Islamic events, ASRR generates personalized calendar entries and manages their synchronization with Google Calendar.

The application combines a Next.js frontend, Django REST API, PostgreSQL database, and asynchronous background processing with Celery and Redis.

## Key Features

**Google Calendar Integration**
- Implemented OAuth 2.0 authentication for connecting Google accounts.
- Integrated the Google Calendar API to create, update, and delete calendar events.
- Developed synchronization logic to detect scheduling changes and manage previously created events.
- Maintains Google event identifiers and synchronization states in PostgreSQL.

**Automated Prayer Scheduling**
- Generates calendar events for the five daily Islamic prayers.
- Retrieves prayer times based on user location and selected Madhab.
- Updates scheduled events when prayer times or location preferences change.
- Supports enabling or disabling daily prayer synchronization.

**Customizable Sunnah Reminders**
- Supports voluntary fasting schedules, including Mondays, Thursdays, White Days, Arafah, and Ashura.
- Provides reminders for Tahajjud, Duha, Adhkar, and other Sunnah practices.
- Allows users to enable or disable individual reminders.
- Automatically updates synchronized events when preferences change.

**Hijri Calendar Management**
- Maps Hijri calendar dates to Gregorian dates.
- Generates recurring events based on Islamic dates, weekdays, and monthly schedules.
- Supports significant Islamic occasions, including Ramadan and Eid.
- Includes backend management commands for calendar initialization and annual refreshes.

**User Authentication and Background Processing**
- Built user registration, login, and profile management with Django.
- Developed REST API endpoints for managing user preferences.
- Integrated Celery and Redis for asynchronous calendar synchronization.
- Used PostgreSQL to store user settings, prayer data, calendar events, and synchronization records.

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | Next.js, React, TypeScript, CSS |
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| Background Processing | Celery, Redis |
| API Integration | Google Calendar API, Google OAuth 2.0 |
| Deployment | Vercel, Render |
| Development Tools | Git, GitHub |

## System Architecture

```text
                   Next.js Frontend
                          |
                    Django REST API
                          |
            +-------------+-------------+
            |             |             |
       PostgreSQL      Celery         Google OAuth
            |             |             |
      User Profiles     Redis       Google Calendar API
      Prayer Times        |
      Hijri Calendar   Background
      Event Records    Sync Tasks
```

The frontend communicates with Django REST Framework endpoints to manage authentication, user settings, and calendar preferences.

PostgreSQL stores application data, while Celery processes synchronization tasks asynchronously. The Google Calendar API handles event creation, modification, and deletion.

## Engineering Highlights

### 1. Google Calendar Synchronization

Designed a synchronization workflow that manages the relationship between internal database records and external Google Calendar events.

Each synchronized event maintains a Google Calendar event ID and synchronization state, allowing the backend to determine whether an event should be created, updated, or deleted.

This reduces unnecessary event creation and supports changes to user preferences without requiring users to rebuild their calendars manually.

### 2. Asynchronous Task Processing

Implemented background task processing with Celery and Redis to separate calendar synchronization from HTTP request handling.

When users update their preferences, the backend can queue synchronization tasks instead of performing all Google Calendar operations during the API request.

### 3. Personalized Event Generation

Developed backend services that generate user-specific schedules using location, prayer-time data, Hijri dates, and individual Sunnah preferences.

The scheduling system supports multiple recurrence patterns, including daily, weekly, and Hijri-calendar-based events.

### 4. External API Integration

Integrated Google OAuth 2.0 and the Google Calendar API, including token management and API error handling.

Implemented synchronization states and deletion workflows to manage events across both the application database and Google Calendar.

## Challenges and Technical Decisions

- **Calendar consistency:** Tracking external Google event IDs to update existing entries instead of blindly creating new events.
- **Dynamic schedules:** Supporting prayer times that change throughout the year and vary by location.
- **Recurring Islamic dates:** Translating Hijri-based recurrence rules into Gregorian calendar events.
- **Background execution:** Using Celery to process potentially large numbers of calendar operations asynchronously.
- **User-controlled synchronization:** Designing event creation and deletion around individual user preferences.

## Deployment

ASRR uses a separated frontend and backend deployment architecture.

- **Frontend:** Vercel
- **Backend API:** Render
- **Database:** PostgreSQL
- **Background processing:** Celery and Redis

**Application:** https://asrr-seven.vercel.app/

## Project Status

ASRR is an actively developed personal software engineering project.

Current development focuses on improving calendar synchronization reliability, automating annual calendar updates, and refining the user experience.

---

**ASRR — Make time for what matters.**
