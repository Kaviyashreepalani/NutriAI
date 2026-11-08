import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from './api';

export interface User {
  id?: string;
  auth_uid?: string;
  email: string;
  full_name?: string;
  role?: string;
  age?: number;
  life_stage?: string;
  date_of_birth?: string;
  preferred_language?: string;
  requires_guardian_consent?: boolean;
  guardian_consent_granted?: boolean;
  profile_completion_pct?: number;
  [key: string]: any;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithDevAccount: (accountId: string) => Promise<void>;
  loginWithToken: (token: string) => Promise<void>;
  register: (data: any) => Promise<any>;
  logout: () => void;
  sendPasswordReset: (email: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('nutriai_token') || localStorage.getItem('token');
  });
  const [isLoading, setIsLoading] = useState(true);

  // Initialize and restore session on mount
  useEffect(() => {
    const initSession = async () => {
      const storedToken = localStorage.getItem('nutriai_token') || localStorage.getItem('token');
      if (storedToken) {
        try {
          const res = await api.post('/auth/session', { token: storedToken });
          if (res.data) {
            setUser(res.data);
            setToken(storedToken);
          }
        } catch {
          // Token invalid or expired
          localStorage.removeItem('nutriai_token');
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    initSession();
  }, []);

  const saveAuthSession = (authToken: string, userData: User) => {
    localStorage.setItem('nutriai_token', authToken);
    localStorage.setItem('token', authToken);
    setToken(authToken);
    setUser(userData);
  };

  const login = async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password });
    if (res.data?.token && res.data?.user) {
      saveAuthSession(res.data.token, res.data.user);
    }
  };

  const loginWithDevAccount = async (accountId: string) => {
    const res = await api.post('/auth/dev-login', { account_key: accountId });
    if (res.data?.token && res.data?.user) {
      saveAuthSession(res.data.token, res.data.user);
    }
  };

  const loginWithToken = async (newToken: string) => {
    const res = await api.post('/auth/session', { token: newToken });
    if (res.data) {
      saveAuthSession(newToken, res.data);
    }
  };

  const register = async (data: any) => {
    const res = await api.post('/auth/register', data);
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('nutriai_token');
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const sendPasswordReset = async (email: string) => {
    await api.post('/auth/forgot-password', { email });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        loginWithDevAccount,
        loginWithToken,
        register,
        logout,
        sendPasswordReset,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
