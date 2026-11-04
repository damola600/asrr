
import Link from "next/link";
import styles from "./page.module.css";

const features = [
  {
    icon: "☾",
    title: "Daily Prayer Times",
    description:
      "Keep track of Fajr, Dhuhr, Asr, Maghrib, and Isha with prayer times based on your selected location and calculation preferences.",
  },
  {
    icon: "✦",
    title: "Sunnah Reminders",
    description:
      "Organize reminders for voluntary fasting, remembrance, and other Sunnah practices.",
  },
  {
    icon: "◷",
    title: "Islamic Calendar",
    description:
      "See important Islamic dates, holidays, and fasting days alongside your everyday schedule.",
  },
  {
    icon: "▦",
    title: "Google Calendar Sync",
    description:
      "Connect Google Calendar to create, update, and remove ASRR-managed events based on your preferences.",
  },
];

export default function HomePage() {
  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>☾</span>
          ASRR
        </Link>

        <nav className={styles.navigation}>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <Link href="/login" className={styles.loginButton}>
            Log In
          </Link>
        </nav>
      </header>

      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <span className={styles.eyebrow}>
            YOUR PERSONAL ISLAMIC CALENDAR
          </span>

          <h1>
            Make time for
            <span> what matters.</span>
          </h1>

          <p>
            ASRR helps you organize your daily prayers,
            Sunnah practices, fasting days, and important
            Islamic dates in one place with
            Google Calendar synchronization.
          </p>

          <div className={styles.heroActions}>
            <Link href="/login" className={styles.primaryButton}>
              Get Started
            </Link>

            <a href="#how-it-works" className={styles.secondaryButton}>
              Learn More
            </a>
          </div>

          <p className={styles.heroNote}>
            Your schedule. Your preferences. Your journey.
          </p>
        </div>

        <div className={styles.heroVisual}>
          <div className={styles.moon}>☾</div>
          <div className={styles.visualLabel}>
            Prayer · Remembrance · Sunnah
          </div>
        </div>
      </section>

      <section id="features" className={styles.section}>
        <div className={styles.sectionHeading}>
          <span className={styles.eyebrow}>WHAT ASRR OFFERS</span>
          <h2>Faith, thoughtfully organized.</h2>
          <p>
            Simple tools to help you plan your Islamic
            practices alongside your daily responsibilities.
          </p>
        </div>

        <div className={styles.featureGrid}>
          {features.map((feature) => (
            <article className={styles.featureCard} key={feature.title}>
              <div className={styles.featureIcon}>
                {feature.icon}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="how-it-works" className={styles.howSection}>
        <div className={styles.sectionHeading}>
          <span className={styles.eyebrow}>GETTING STARTED</span>
          <h2>Three simple steps.</h2>
        </div>

        <div className={styles.steps}>
          <div>
            <span>01</span>
            <h3>Create your account</h3>
            <p>Sign up and configure your location and preferences.</p>
          </div>

          <div>
            <span>02</span>
            <h3>Choose your reminders</h3>
            <p>Enable the prayer and Sunnah events you want to follow.</p>
          </div>

          <div>
            <span>03</span>
            <h3>Connect Google Calendar</h3>
            <p>
              Authorize ASRR to manage its calendar events
              and keep your selected reminders synchronized.
            </p>
          </div>
        </div>
      </section>

      <section className={styles.googleSection}>
        <div className={styles.googleContent}>
          <span className={styles.eyebrow}>
            GOOGLE CALENDAR INTEGRATION
          </span>
          <h2>Why does ASRR request Google Calendar access?</h2>
          <p>
            ASRR requests Google Calendar permission to
            create Islamic prayer reminders, Sunnah events,
            and Islamic calendar dates in your calendar.
            It also uses this permission to update or
            delete events it manages when your preferences
            or prayer times change.
          </p>
          <p>
            You choose which reminders to enable, and
            Google Calendar access is requested when you
            connect your account.
          </p>
          <Link href="/privacy" className={styles.textLink}>
            Read our Privacy Policy
          </Link>
        </div>
      </section>

      <section className={styles.cta}>
        <h2>Bring intention to your everyday schedule.</h2>
        <p>Start organizing your Islamic calendar with ASRR.</p>
        <Link href="/login" className={styles.primaryButton}>
          Get Started
        </Link>
      </section>

      <footer className={styles.footer}>
        <span>☾ ASRR</span>
        <div>
          <Link href="/privacy">Privacy Policy</Link>
          <Link href="/terms">Terms of Service</Link>
        </div>
        <p>© {new Date().getFullYear()} ASRR.</p>
      </footer>
    </main>
  );
}
