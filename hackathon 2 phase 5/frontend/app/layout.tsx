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
  title: "Smart Todo App | Organize Tasks & Boost Productivity",
  description:
    "A fast, simple, and powerful Todo App to manage daily tasks, track progress, and stay productive. Built with Next.js for speed and reliability.",
};

import { AuthProvider } from "../context/AuthContext";
import Chatbot from "../components/Chatbot";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          {children}
          <Chatbot />
        </AuthProvider>
      </body>
    </html>
  );
}
