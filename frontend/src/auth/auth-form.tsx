import type { FormEventHandler, ReactNode } from 'react'

import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'

type AuthFormProps = {
  submit: FormEventHandler<HTMLFormElement>
  error: string | null
  isSubmitting: boolean
  submitLabel: string
  pendingLabel: string
  children: ReactNode
  footer?: ReactNode
}

export const AuthForm = ({
  submit,
  error,
  isSubmitting,
  submitLabel,
  pendingLabel,
  children,
  footer,
}: AuthFormProps) => (
  <form onSubmit={submit} noValidate className="grid gap-4">
    {error && (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )}

    {children}

    <Button type="submit" disabled={isSubmitting}>
      {isSubmitting ? pendingLabel : submitLabel}
    </Button>

    {footer}
  </form>
)
