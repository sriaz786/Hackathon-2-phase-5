"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 py-20">
        {/* Animated background blobs */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000" />
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000" />
        </div>

        <div
          className={`relative z-10 max-w-6xl mx-auto text-center transition-all duration-1000 ${
            mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
          }`}
        >
         
          {/* Main Heading */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white mb-6 tracking-tight">
            Organize Your Life
            <br />
            <span className="bg-gradient-to-r from-yellow-200 via-pink-200 to-purple-200 bg-clip-text text-transparent">
              Effortlessly
            </span>
          </h1>

          <p className="text-sm md:text-xl text-white/90 mb-12 max-w-2xl mx-auto leading-relaxed">
            The smart todo app that understands natural language. Chat with AI
            to manage tasks, set priorities, and boost your productivity like
            never before.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Link
              href="/login"
              className="px-12 py-4 bg-white/10 backdrop-blur-md text-white rounded-full font-bold text-lg hover:bg-white/20 transition-all duration-300 border-2 border-white/30 transform hover:scale-105 w-full sm:w-auto"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="group relative px-12 py-4 bg-white text-purple-600 rounded-full font-bold text-lg hover:bg-opacity-90 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-white/50 w-full sm:w-auto"
            >
              <span className="relative z-10">Register</span>
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-yellow-400 to-pink-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300" />
            </Link>

          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-extrabold text-white mb-2">
                10K+
              </div>
              <div className="text-white/80 text-sm md:text-base">
                Active Users
              </div>
            </div>
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-extrabold text-white mb-2">
                1M+
              </div>
              <div className="text-white/80 text-sm md:text-base">
                Tasks Completed
              </div>
            </div>
            <div className="text-center">
              <div className="text-4xl md:text-5xl font-extrabold text-white mb-2">
                99%
              </div>
              <div className="text-white/80 text-sm md:text-base">
                Satisfaction
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
