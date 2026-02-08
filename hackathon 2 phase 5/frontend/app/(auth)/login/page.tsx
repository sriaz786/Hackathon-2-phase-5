"use client";

import { useState } from "react";
import { useAuth } from "../../../context/AuthContext";
import Link from "next/link";
import api from "../../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Using FormData for OAuth2 compatibility
    const formData = new FormData();
    formData.append("username", email); // OAuth2 expects 'username' field, we map email to it
    formData.append("password", password);

    try {
      const response = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const { access_token, refresh_token } = response.data;
      login(access_token, refresh_token);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4">
      <div className="w-full max-w-md p-8 bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/20">
        <h1 className="text-3xl font-extrabold mb-2 text-center text-gray-800 tracking-tight">
          Welcome Back
        </h1>
        <p className="text-center text-gray-500 mb-8">
          Sign in to continue to your dashboard
        </p>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
              placeholder="john@example.com"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none text-gray-900"
              placeholder="••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold py-3 rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-[1.02] shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>

        <p className="mt-8 text-center text-gray-600 text-sm">
          Don't have an account?{" "}
          <Link
            href="/signup"
            className="text-indigo-600 hover:text-indigo-800 font-semibold hover:underline"
          >
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
