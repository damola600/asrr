
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Terms of Service | ASRR",
  description: "Terms governing use of the ASRR application.",
};

const sections = [
  {
    title: "1. Acceptance of Terms",
    text: "By accessing or using ASRR, you agree to these Terms of Service. If you do not agree, please discontinue use of the application."
  },
  {
    title: "2. Description of Service",
    text: "ASRR helps users organize Islamic prayer times, fasting reminders, and selected Sunnah activities through Google Calendar synchronization. Features may change as the application develops."
  },
  {
    title: "3. User Accounts",
    text: "You are responsible for providing accurate account information, maintaining the security of your credentials, and activity performed through your account. You must not access another person's account without authorization."
  },
  {
    title: "4. Google Calendar Integration",
    text: "By connecting Google Calendar, you authorize ASRR to perform the calendar operations described during Google's authorization process. Depending on your preferences, ASRR may create, modify, or remove events. You may revoke Google authorization through your Google Account settings."
  },
  {
    title: "5. Prayer Times and Religious Information",
    text: "Prayer times and Islamic dates may vary based on location, calculation methods, local moon sightings, and religious interpretation. ASRR provides scheduling assistance and does not replace guidance from your local mosque or qualified religious authorities. You should independently verify important times and dates."
  },
  {
    title: "6. Acceptable Use",
    text: "You agree not to misuse ASRR, attempt unauthorized access, interfere with service availability, exploit security vulnerabilities, or use the application in violation of applicable law."
  },
  {
    title: "7. Third-Party Services",
    text: "ASRR relies on third-party services, including Google Calendar and hosting providers. Their services are governed by their own terms and policies. Availability of integrations may change."
  },
  {
    title: "8. Availability and Changes",
    text: "ASRR may be updated, interrupted, or discontinued. We do not guarantee uninterrupted availability, error-free operation, or delivery of every calendar reminder."
  },
  {
    title: "9. Disclaimer",
    text: "ASRR is provided on an 'as available' basis. To the extent permitted by applicable law, we disclaim warranties not expressly stated in these Terms. Nothing in these Terms excludes rights or protections that cannot lawfully be excluded."
  },
  {
    title: "10. Limitation of Liability",
    text: "To the extent permitted by applicable law, ASRR's operator is not responsible for indirect or consequential losses arising from use of the service, including missed reminders, synchronization errors, or service interruptions. Applicable consumer protections remain unaffected."
  },
  {
    title: "11. Termination",
    text: "We may suspend access when reasonably necessary to address misuse, security risks, or legal requirements. Users may stop using the service and request account deletion."
  },
  {
    title: "12. Changes to Terms",
    text: "These Terms may be revised from time to time. Material changes will be communicated as required by applicable law. Continued use after changes take effect may constitute acceptance where legally permitted."
  },
];

export default function TermsPage() {
  return (
    <main style={{
      maxWidth: 820,
      margin: "0 auto",
      padding: "64px 24px",
      lineHeight: 1.8,
      color: "var(--foreground, #202a25)"
    }}>
      <Link href="/" style={{ color: "#23724c" }}>
        ← Back to ASRR
      </Link>

      <h1 style={{ fontSize: "2.5rem", marginTop: 28 }}>
        Terms of Service
      </h1>
      <p>Last updated: November 3, 2026</p>

      <p>
        Welcome to ASRR. These Terms govern your use of our
        Islamic calendar and reminder scheduling application.
      </p>

      {sections.map((section) => (
        <section key={section.title} style={{ marginTop: 32 }}>
          <h2 style={{ fontSize: "1.35rem" }}>
            {section.title}
          </h2>
          <p>{section.text}</p>
        </section>
      ))}

      <section style={{ marginTop: 32 }}>
        <h2>13. Contact</h2>
        <p>
          Questions about these Terms may be sent to:
          <a href="asrr4698@gmail.com">Email</a>
        </p>
        <p>
          Service operator: ASRR Organization
        </p>
      </section>

      <footer style={{ marginTop: 56 }}>
        <Link href="/privacy">Privacy Policy</Link>
        {" · "}
        <Link href="/">Home</Link>
      </footer>
    </main>
  );
}
