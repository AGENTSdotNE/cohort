import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { z } from 'zod'

import { FormField } from '@/components/form-field'
import { Button } from '@/components/ui/button'
import { useApiForm } from '@/lib/use-api-form'

import { confirmPasswordReset } from './api'
import { AuthCard } from './auth-card'
import { AuthForm } from './auth-form'
import { IncompleteLinkCard } from './incomplete-link-card'
import { PASSWORD_HINT, passwordSchema } from './password-rules'
import { useEmailLink } from './use-email-link'

const schema = z.object({ password: passwordSchema })

type Values = z.infer<typeof schema>

export const ResetPasswordPage = () => {
  const { uid, token } = useEmailLink()

  const form = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { password: '' } })
  const { submit, error, succeeded, isSubmitting } = useApiForm(form, async ({ password }) => {
    await confirmPasswordReset(uid, token, password)
  })

  if (!uid || !token) return <IncompleteLinkCard />

  if (succeeded) {
    return (
      <AuthCard title="Password changed" description="You can sign in with your new password.">
        <Button asChild className="w-full">
          <Link to="/sign-in">Sign in</Link>
        </Button>
      </AuthCard>
    )
  }

  return (
    <AuthCard title="Choose a new password">
      <AuthForm
        submit={submit}
        error={error}
        isSubmitting={isSubmitting}
        submitLabel="Save new password"
        pendingLabel="Saving..."
      >
        <FormField
          label="New password"
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
