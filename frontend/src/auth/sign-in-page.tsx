import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { FormField } from '@/components/form-field'
import { setSessionUser } from '@/lib/query-client'
import { useApiForm } from '@/lib/use-api-form'

import { signIn } from './api'
import { AuthCard } from './auth-card'
import { AuthForm } from './auth-form'
import { useSession } from './use-session'

const schema = z.object({
  email: z.email('Enter your email address'),
  password: z.string().min(1, 'Enter your password'),
})

type Values = z.infer<typeof schema>

export const SignInPage = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { data: user } = useSession()

  const destination = (location.state as { from?: string } | null)?.from ?? '/'

  const form = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { email: '', password: '' } })
  const apiForm = useApiForm(form, async ({ email, password }) => {
    setSessionUser(await signIn(email, password))
    void navigate(destination, { replace: true })
  })

  if (user) return <Navigate to={destination} replace />

  return (
    <AuthCard
      title="Sign in"
      description="Enter your email address and password to continue."
      footer={
        <>
          No account yet?{' '}
          <Link to="/sign-up" className="underline">
            Create one
          </Link>
        </>
      }
    >
      <AuthForm
        apiForm={apiForm}
        submitLabel="Sign in"
        pendingLabel="Signing in..."
        footer={
          <div className="text-muted-foreground flex flex-wrap justify-between gap-2 text-sm">
            <Link to="/forgot-password" className="underline">
              Forgotten your password?
            </Link>
            <Link to="/resend-verification" className="underline">
              Resend confirmation
            </Link>
          </div>
        }
      >
        <FormField
          label="Email address"
          type="email"
          autoComplete="username"
          error={form.formState.errors.email}
          registration={form.register('email')}
        />

        <FormField
          label="Password"
          type="password"
          autoComplete="current-password"
          error={form.formState.errors.password}
          registration={form.register('password')}
        />
      </AuthForm>
    </AuthCard>
  )
}
