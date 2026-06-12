"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getStoredUser, clearAuthToken, type AuthUser } from "@/lib/api";

type AuthContextType = {
  user: AuthUser | null;
  loading: boolean;
  logout: () => void;
  refresh: () => void;
};

const AuthContext = createContext<AuthContextType>({ user: null, loading: true, logout: () => {}, refresh: () => {} });

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = getStoredUser();
    setUser(stored);
    setLoading(false);
  }, []);

  function logout() {
    clearAuthToken();
    setUser(null);
  }

  function refresh() {
    const stored = getStoredUser();
    setUser(stored);
  }

  return (
    <AuthContext.Provider value={{ user, loading, logout, refresh }}>
      {children}
    </AuthContext.Provider>
  );
}
