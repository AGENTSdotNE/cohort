import { useQuery } from '@tanstack/react-query'

import { fetchAuthConfig } from './api'

export const useAuthConfig = () =>
  useQuery({
    queryKey: ['auth-config'],
    queryFn: fetchAuthConfig,
    staleTime: Infinity,
  })
