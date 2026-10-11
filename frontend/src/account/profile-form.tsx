import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import { z } from 'zod'

import { useUser } from '@/auth/use-user'
import { FormField } from '@/components/form-field'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { setSessionUser } from '@/lib/query-client'
import { useApiForm } from '@/lib/use-api-form'

import { updateProfile } from './api'

const schema = z.object({ full_name: z.string().trim().min(1, 'Enter your name') })

type Values = z.infer<typeof schema>

export const ProfileForm = () => {
  const user = useUser()
  const form = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { full_name: user.full_name } })

  const { submit, error, isSubmitting } = useApiForm(form, async ({ full_name }) => {
    setSessionUser(await updateProfile(full_name))
    toast.success('Your name has been saved')
  })

  return (
    <form onSubmit={submit} noValidate className="grid gap-4">
      <FormField
        label="Full name"
        autoComplete="name"
        error={form.formState.errors.full_name}
        registration={form.register('full_name')}
      />

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Button type="submit" disabled={isSubmitting} className="justify-self-start">
        {isSubmitting ? 'Saving...' : 'Save'}
      </Button>
    </form>
  )
}
