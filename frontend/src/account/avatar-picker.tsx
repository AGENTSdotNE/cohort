import { useMutation } from '@tanstack/react-query'
import { type ChangeEvent, useRef } from 'react'
import { toast } from 'sonner'

import { useUser } from '@/auth/use-user'
import { Button } from '@/components/ui/button'
import { UserAvatar } from '@/components/user-avatar'
import { setSessionUser } from '@/lib/query-client'

import { removeAvatar, uploadAvatar } from './api'

export const AvatarPicker = () => {
  const user = useUser()
  const fileInput = useRef<HTMLInputElement>(null)

  const onError = (error: Error) => toast.error(error.message)
  const upload = useMutation({ mutationFn: uploadAvatar, onSuccess: setSessionUser, onError })
  const remove = useMutation({ mutationFn: removeAvatar, onSuccess: setSessionUser, onError })

  const choose = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    // Clearing the input means picking the same file again still counts as a change.
    event.target.value = ''

    if (file) upload.mutate(file)
  }

  const busy = upload.isPending || remove.isPending

  return (
    <div className="flex items-center gap-4">
      <UserAvatar user={user} size="lg" />

      <input ref={fileInput} type="file" accept="image/*" className="hidden" onChange={choose} />
      <div className="flex flex-wrap gap-2">
        <Button type="button" variant="outline" size="sm" disabled={busy} onClick={() => fileInput.current?.click()}>
          {upload.isPending ? 'Uploading...' : 'Choose picture'}
        </Button>
        {user.avatar_url && (
          <Button type="button" variant="ghost" size="sm" disabled={busy} onClick={() => remove.mutate()}>
            Remove
          </Button>
        )}
      </div>
    </div>
  )
}
