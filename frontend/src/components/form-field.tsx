import type { ComponentProps } from 'react'
import type { FieldError, UseFormRegisterReturn } from 'react-hook-form'

import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

type FormFieldProps = ComponentProps<'input'> & {
  label: string
  hint?: string
  error?: FieldError | string | null
  registration: UseFormRegisterReturn
}

export const FormField = ({ label, hint, error, registration, ...props }: FormFieldProps) => {
  const message = typeof error === 'string' ? error : error?.message

  return (
    <div className="grid gap-2">
      <Label htmlFor={registration.name}>{label}</Label>
      <Input id={registration.name} aria-invalid={Boolean(message)} {...registration} {...props} />
      {hint && !message && <p className="text-muted-foreground text-sm">{hint}</p>}
      {message && (
        <p role="alert" className="text-destructive text-sm">
          {message}
        </p>
      )}
    </div>
  )
}
