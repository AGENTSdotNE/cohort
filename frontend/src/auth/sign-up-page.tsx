import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, Navigate } from 'react-router-dom'
import { z } from 'zod'

import { FormField } from '@/components/form-field'
import { Button } from '@/components/ui/button'
import { setSessionUser } from '@/lib/query-client'
import { useApiForm } from '@/lib/use-api-form'

import { signUp } from './api'
import { AuthCard } from './auth-card'
import { AuthForm } from './auth-form'
import { PASSWORD_HINT, passwordSchema } from './password-rules'
import { useSession } from './use-session'

const schema = z.object({
  full_name: z.string().trim().min(1, 'Enter your name'),
  email: z.email('Enter your email address'),
  password: passwordSchema,
})

type Values = z.infer<typeof schema>

export const SignUpPage = () => {
  const { data: user } = useSession()

  const form = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues: { full_name: '', email: '', password: '' },
  })
  const { submit, error, succeeded, isSubmitting } = useApiForm(form, async (values) => {
    const newUser = await signUp(values)
    // Deployments without email skip verification and sign the new account in straight away.
    if (newUser.email_verified) setSessionUser(newUser)
  })

  if (user) return <Navigate to="/" replace />

  if (succeeded) {
    return (
      <AuthCard
        title="Check your email"
        description={`We have sent a confirmation link to ${form.getValues('email')}.`}
      >
        <p className="text-muted-foreground text-sm">
          Follow the link to confirm your address, then sign in. In development the email is printed in the Django
          terminal rather than sent.
        </p>
        <Button asChild variant="outline" className="mt-4 w-full">
          <Link to="/sign-in">Back to sign in</Link>
        </Button>
      </AuthCard>
    )
  }

  return (
    <AuthCard
      title="Create an account"
      footer={
        <>
          Already have one?{' '}
          <Link to="/sign-in" className="underline">
            Sign in
          </Link>
        </>
      }
    >
      <AuthForm
        submit={submit}
        error={error}
        isSubmitting={isSubmitting}
        submitLabel="Create account"
        pendingLabel="Creating account..."
      >
        <FormField
          label="Full name"
          autoComplete="name"
          error={form.formState.errors.full_name}
          registration={form.register('full_name')}
        />

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
          autoComplete="new-password"
          hint={PASSWORD_HINT}
          error={form.formState.errors.password}
          registration={form.register('password')}
        />
      </AuthForm>
    </AuthCard>
  )
}
