import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { ForgotPasswordPage } from '@/auth/forgot-password-page'
import { RequireAuth } from '@/auth/require-auth'
import { ResendVerificationPage } from '@/auth/resend-verification-page'
import { ResetPasswordPage } from '@/auth/reset-password-page'
import { SignInPage } from '@/auth/sign-in-page'
import { SignUpPage } from '@/auth/sign-up-page'
import { VerifyEmailPage } from '@/auth/verify-email-page'
import { DashboardPage } from '@/pages/dashboard-page'

import { AppShell } from './layout/app-shell'
import { NotFoundPage } from './not-found-page'

export const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/sign-in" element={<SignInPage />} />
      <Route path="/sign-up" element={<SignUpPage />} />
      <Route path="/verify-email" element={<VerifyEmailPage />} />
      <Route path="/resend-verification" element={<ResendVerificationPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      <Route element={<RequireAuth />}>
        <Route element={<AppShell />}>
          <Route index element={<DashboardPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Route>
    </Routes>
  </BrowserRouter>
)
