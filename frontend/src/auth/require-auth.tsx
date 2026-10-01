import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'

import { AuthCard } from './auth-card'
import { useSession } from './use-session'

export const RequireAuth = () => {
  const { data: user, isPending, isError, error, refetch } = useSession()
  const location = useLocation()

  if (isPending) {
    return (
      <div className="flex min-h-svh items-center justify-center p-6">
        <Skeleton className="h-32 w-full max-w-sm" />
      </div>
    )
  }

  if (isError) {
    return (
      <AuthCard title="The app can't load right now" description={error.message}>
        <Button className="w-full" onClick={() => void refetch()}>
          Try again
        </Button>
      </AuthCard>
    )
  }

  if (!user) return <Navigate to="/sign-in" replace state={{ from: location.pathname }} />

  return <Outlet />
}
