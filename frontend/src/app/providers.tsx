import { QueryClientProvider } from '@tanstack/react-query'
import type { ReactNode } from 'react'

import { Toaster } from '@/components/ui/sonner'
import { queryClient } from '@/lib/query-client'

export const Providers = ({ children }: { children: ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    {children}
    <Toaster />
  </QueryClientProvider>
)
