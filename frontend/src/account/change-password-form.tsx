import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import { z } from 'zod'

import { PASSWORD_HINT, passwordSchema } from '@/auth/password-rules'
import { FormField } from '@/components/form-field'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { useApiForm } from '@/lib/use-api-form'

import { changePassword } from './api'

const schema = z.object({
  current_password: z.string().min(1, 'Enter your current password'),
  new_password: passwordSchema,
})

type Values = z.infer<typeof schema>

export const ChangePasswordForm = () => {
  const form = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues: { current_password: '', new_password: '' },
  })

  const { submit, error, isSubmitting } = useApiForm(form, async ({ current_password, new_password }) => {
    await changePassword(current_password, new_password)
    form.reset()
    toast.success('Your password has been changed')
  })

  return (
    <form onSubmit={submit} noValidate className="grid gap-4">
      <FormField
        label="Current password"
        type="password"
        autoComplete="current-password"
        error={form.formState.errors.current_password}
        registration={form.register('current_password')}
      />
      <FormField
        label="New password"
        type="password"
        autoComplete="new-password"
        hint={PASSWORD_HINT}
        error={form.formState.errors.new_password}
        registration={form.register('new_password')}
      />

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Button type="submit" disabled={isSubmitting} className="justify-self-start">
        {isSubmitting ? 'Changing...' : 'Change password'}
      </Button>
    </form>
  )
}
