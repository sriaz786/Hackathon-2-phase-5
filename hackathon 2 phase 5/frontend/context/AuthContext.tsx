"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import api from "../lib/api";

interface User {
  id: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (token: string, refresh_token: string) => void;
  logout: () => void;
  loading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  login: () => {},
  logout: () => {},
  loading: true,
  isAuthenticated: false,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const decoded: any = jwtDecode(token);
          // Ideally fetch user details from API if decoded incomplete, but we can rely on sub/id
          setUser({ id: decoded.sub, email: "" }); // We might need an endpoint to get user details me
        } catch (error) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = (token: string, refresh_token: string) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("refresh_token", refresh_token);
    const decoded: any = jwtDecode(token);
    setUser({ id: decoded.sub, email: "" });
    router.push("/todos");
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{ user, login, logout, loading, isAuthenticated: !!user }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
