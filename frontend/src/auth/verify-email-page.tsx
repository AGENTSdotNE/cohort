import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'

import { verifyEmail } from './api'
import { AuthCard } from './auth-card'
import { IncompleteLinkCard } from './incomplete-link-card'
import { useEmailLink } from './use-email-link'

export const VerifyEmailPage = () => {
  const { uid, token } = useEmailLink()

  const { isPending, isError } = useQuery({
    queryKey: ['verify-email', uid, token],
    queryFn: () => verifyEmail(uid, token),
    enabled: Boolean(uid && token),
    retry: false,
    // The token stops working once it has been used, so this POST must never be refetched.
    staleTime: Infinity,
    gcTime: Infinity,
  })

  if (!uid || !token) return <IncompleteLinkCard />

  if (isPending) return <AuthCard title="Confirming your email address" description="One moment." />

  if (isError) {
    return (
      <AuthCard
        title="That link did not work"
        description="It may have expired, or your email address may already be confirmed."
      >
        <div className="grid gap-2">
          <Button asChild className="w-full">
            <Link to="/sign-in">Try signing in</Link>
          </Button>
          <Button asChild variant="outline" className="w-full">
            <Link to="/resend-verification">Send a new link</Link>
          </Button>
        </div>
      </AuthCard>
    )
  }

  return (
    <AuthCard title="Email confirmed" description="Your account is ready to use.">
      <Button asChild className="w-full">
        <Link to="/sign-in">Sign in</Link>
      </Button>
    </AuthCard>
  )
}
