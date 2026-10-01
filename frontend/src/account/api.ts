import type { User } from '@/auth/api'
import { apiRequest } from '@/lib/api-client'

export const updateProfile = (full_name: string) =>
  apiRequest<User>('/auth/me/', { method: 'PATCH', body: { full_name } })

export const changePassword = (current_password: string, new_password: string) =>
  apiRequest<void>('/auth/change-password/', { body: { current_password, new_password } })

export const uploadAvatar = (file: File) => {
  const body = new FormData()
  body.append('avatar', file)

  return apiRequest<User>('/auth/me/avatar/', { method: 'PUT', body })
}

export const removeAvatar = () => apiRequest<User>('/auth/me/avatar/', { method: 'DELETE' })
