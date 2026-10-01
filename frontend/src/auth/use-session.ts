import { useQuery } from '@tanstack/react-query'

import { ApiError } from '@/lib/api-client'
import { SESSION_KEY } from '@/lib/query-client'

import { fetchCurrentUser } from './api'

export const useSession = () =>
  useQuery({
    queryKey: SESSION_KEY,
    queryFn: async () => {
      try {
        return await fetchCurrentUser()
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) return null

        throw error
      }
    },
    retry: false,
    staleTime: 5 * 60 * 1000,
  })
