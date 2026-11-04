import Link from 'next/link';
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ASRR Islamic Calendar",
  description: "Your personal Islamic calendar for prayer, remembrance and Sunnah.",
  verification:{
    google: process.env.GOOGLE_SITE_VERIFICATION,
  }
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {children}

        <footer className="site-footer">
          <div>
            <p>© {new Date().getFullYear()}. All rights reserved.</p>
          </div>
          <nav aria-label="Legal">
            <Link href="/privacy">Privacy Policy</Link>
            <Link href="/terms">Terms of Service</Link>
          </nav>
        </footer>
      </body>
      
    </html>
    
  );
}
