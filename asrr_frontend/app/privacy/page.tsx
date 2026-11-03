
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy | ASRR",
  description: "Learn how ASRR handles personal data and Google Calendar access.",
};

const sections = [
  {
    title: "1. Information We Collect",
    body: [
      "When you register for ASRR, we collect the account information needed to create and manage your account, including your email address.",
      "We collect preferences you provide, such as your city, country, Madhab, daily prayer settings, and selected Sunnah reminders.",
      "When you connect Google Calendar, we receive authorization credentials and the information necessary to create, update, and remove calendar events according to your preferences."
    ],
  },
  {
    title: "2. How We Use Your Information",
    body: [
      "We use your information to operate ASRR, calculate prayer schedules, personalize Islamic reminders, authenticate your account, and synchronize events with Google Calendar.",
      "We also may process technical information necessary to maintain service reliability, troubleshoot errors, and protect the application."
    ],
  },
  {
    title: "3. Google Calendar Data",
    body: [
      "ASRR uses Google Calendar authorization to create, update, and delete prayer-time and Islamic reminder events based on your selections.",
      "ASRR does not sell Google user data or use it for advertising. Google Calendar data is used to provide the calendar synchronization features you request.",
      "ASRR's use and transfer of information received from Google APIs will adhere to the Google API Services User Data Policy, including the Limited Use requirements."
    ],
  },
  {
    title: "4. Data Storage and Security",
    body: [
      "Account information, preferences, and calendar synchronization records are stored using the application's hosting and database infrastructure.",
      "We use reasonable technical and organizational measures to protect information. However, no internet-based service can guarantee absolute security."
    ],
  },
  {
    title: "5. Sharing of Information",
    body: [
      "Information may be processed by infrastructure providers that support the operation of ASRR, and by Google when you choose to connect Google Calendar.",
      "We do not sell your personal information. We may disclose information when required by applicable law."
    ],
  },
  {
    title: "6. Retention and Deletion",
    body: [
      "We retain information as needed to operate your account and provide the service. You may contact us to request deletion of your account and associated personal information.",
      "Disconnecting ASRR from your Google Account revokes its future authorization, but does not necessarily delete information already stored by ASRR or events previously created in Google Calendar."
    ],
  },
  {
    title: "7. Your Choices",
    body: [
      "You can change prayer and Sunnah preferences through ASRR. You can revoke ASRR's Google access through your Google Account permissions.",
      "You may contact us to request access to, correction of, or deletion of your personal information, subject to applicable requirements."
    ],
  },
  {
    title: "8. Changes to This Policy",
    body: [
      "We may update this Privacy Policy to reflect changes in our services, practices, or legal requirements. Updates will be published on this page."
    ],
  },
];

export default function PrivacyPage() {
  return (
    <main className='legal-page' style={{
      maxWidth: 820,
      margin: "0 auto",
      padding: "64px 24px",
      lineHeight: 1.8,
    }}>
      <Link href="/" style={{ color: "#23724c" }}>
        ← Back to ASRR
      </Link>

      <h1 style={{ fontSize: "2.5rem", marginTop: 28 }}>
        Privacy Policy
      </h1>
      <p>Last updated: November 3, 2026</p>

      <p>
        ASRR is an Islamic prayer and reminder scheduling application
        that helps users synchronize prayer times and selected Sunnah
        activities with Google Calendar. This policy explains how
        information is handled when you use ASRR.
      </p>

      {sections.map((section) => (
        <section key={section.title} style={{ marginTop: 32 }}>
          <h2 style={{ fontSize: "1.35rem" }}>
            {section.title}
          </h2>
          {section.body.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </section>
      ))}

      <section style={{ marginTop: 32 }}>
        <h2>9. Contact Us</h2>
        <p>
          For privacy inquiries, data requests, or concerns,
          contact: [YOUR SUPPORT EMAIL]
        </p>
      </section>

      <footer style={{ marginTop: 56 }}>
        <Link href="/terms">Terms of Service</Link>
        {" · "}
        <Link href="/">Home</Link>
      </footer>
    </main>
  );
}
