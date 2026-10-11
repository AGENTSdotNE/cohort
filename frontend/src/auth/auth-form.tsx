import type { ReactNode } from 'react'

import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import type { useApiForm } from '@/lib/use-api-form'

type AuthFormProps = {
  apiForm: ReturnType<typeof useApiForm>
  submitLabel: string
  pendingLabel: string
  children: ReactNode
  footer?: ReactNode
}

export const AuthForm = ({ apiForm, submitLabel, pendingLabel, children, footer }: AuthFormProps) => (
  <form onSubmit={apiForm.submit} noValidate className="grid gap-4">
    {apiForm.error && (
      <Alert variant="destructive">
        <AlertDescription>{apiForm.error}</AlertDescription>
      </Alert>
    )}

    {children}

    <Button type="submit" disabled={apiForm.isSubmitting}>
      {apiForm.isSubmitting ? pendingLabel : submitLabel}
    </Button>

    {footer}
  </form>
)
