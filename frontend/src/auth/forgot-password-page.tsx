import { requestPasswordReset } from './api'
import { EmailRequestCard } from './email-request-card'

export const ForgotPasswordPage = () => (
  <EmailRequestCard
    title="Reset your password"
    description="We will email you a link to choose a new one."
    submitLabel="Send reset link"
    sentMessage="If that address has an account, a reset link is on its way."
    send={requestPasswordReset}
  />
)
