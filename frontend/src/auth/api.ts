import { apiRequest } from '@/lib/api-client'

export type User = { id: number; email: string; full_name: string; email_verified: boolean; avatar_url: string | null }

export const fetchCurrentUser = () => apiRequest<User>('/auth/me/')

export const signIn = (email: string, password: string) =>
  apiRequest<User>('/auth/sign-in/', { body: { email, password } })

export const signOut = () => apiRequest<void>('/auth/sign-out/', { method: 'POST' })

export const signUp = (body: { email: string; full_name: string; password: string }) =>
  apiRequest<User>('/auth/sign-up/', { body })

export const verifyEmail = (uid: string, token: string) =>
  apiRequest<User>('/auth/verify-email/', { body: { uid, token } })

export const resendVerification = (email: string) => apiRequest<void>('/auth/resend-verification/', { body: { email } })

export const requestPasswordReset = (email: string) => apiRequest<void>('/auth/password-reset/', { body: { email } })

export const confirmPasswordReset = (uid: string, token: string, password: string) =>
  apiRequest<void>('/auth/password-reset/confirm/', { body: { uid, token, password } })
