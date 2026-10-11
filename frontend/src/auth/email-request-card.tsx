import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link } from 'react-router-dom'
import { z } from 'zod'

import { FormField } from '@/components/form-field'
import { Button } from '@/components/ui/button'
import { useApiForm } from '@/lib/use-api-form'

import { AuthCard } from './auth-card'
import { AuthForm } from './auth-form'

const schema = z.object({ email: z.email('Enter your email address') })

type Values = z.infer<typeof schema>

type EmailRequestCardProps = {
  title: string
  description: string
  submitLabel: string
  sentMessage: string
  send: (email: string) => Promise<void>
}

export const EmailRequestCard = ({ title, description, submitLabel, sentMessage, send }: EmailRequestCardProps) => {
  const form = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { email: '' } })
  const apiForm = useApiForm(form, ({ email }) => send(email))

  if (apiForm.succeeded) {
    return (
      <AuthCard title="Check your email" description={sentMessage}>
        <Button asChild variant="outline" className="w-full">
          <Link to="/sign-in">Back to sign in</Link>
        </Button>
      </AuthCard>
    )
  }

  return (
    <AuthCard title={title} description={description}>
      <AuthForm
        apiForm={apiForm}
        submitLabel={submitLabel}
        pendingLabel="Sending..."
        footer={
          <Link to="/sign-in" className="text-muted-foreground text-center text-sm underline">
            Back to sign in
          </Link>
        }
      >
        <FormField
          label="Email address"
          type="email"
          autoComplete="username"
          error={form.formState.errors.email}
          registration={form.register('email')}
        />
      </AuthForm>
    </AuthCard>
  )
}
