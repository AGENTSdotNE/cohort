import { useState } from 'react'
import type { FieldValues, Path, UseFormReturn } from 'react-hook-form'

import { ApiError } from './api-client'

export const useApiForm = <T extends FieldValues>(form: UseFormReturn<T>, action: (values: T) => Promise<void>) => {
  const [error, setError] = useState<string | null>(null)
  const [succeeded, setSucceeded] = useState(false)

  const submit = form.handleSubmit(async (values) => {
    setError(null)

    try {
      await action(values)
      setSucceeded(true)
    } catch (caught) {
      if (!(caught instanceof ApiError)) throw caught

      const fieldErrors = caught.fieldErrors()
      const handled = Object.entries(fieldErrors).filter(([field]) => field in values)

      handled.forEach(([field, message]) => form.setError(field as Path<T>, { message }))

      if (handled.length === 0) setError(caught.message)
    }
  })

  return { submit, error, succeeded, isSubmitting: form.formState.isSubmitting }
}
