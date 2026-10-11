import { Link } from 'react-router-dom'

import { useAuthConfig } from './use-auth-config'

export const SignInEmailLinks = () => {
  const { data: config } = useAuthConfig()

  if (!config?.email_enabled) return null

  return (
    <div className="text-muted-foreground flex flex-wrap justify-between gap-2 text-sm">
      <Link to="/forgot-password" className="underline">
        Forgotten your password?
      </Link>
      <Link to="/resend-verification" className="underline">
        Resend confirmation
      </Link>
    </div>
  )
}
