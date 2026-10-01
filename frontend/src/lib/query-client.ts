import { QueryClient } from '@tanstack/react-query'

import type { User } from '@/auth/api'

export const queryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false, retry: 1 } },
})

export const SESSION_KEY = ['session']

export const setSessionUser = (user: User) => queryClient.setQueryData(SESSION_KEY, user)

// Keeps the session entry, set to null, so RequireAuth redirects; drops everything the old user had loaded.
export const clearSession = () => {
  queryClient.setQueryData(SESSION_KEY, null)
  queryClient.removeQueries({ predicate: (query) => query.queryKey[0] !== SESSION_KEY[0] })
}
