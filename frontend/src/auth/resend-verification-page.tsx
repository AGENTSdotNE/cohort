import { resendVerification } from './api'
import { EmailRequestCard } from './email-request-card'

export const ResendVerificationPage = () => (
  <EmailRequestCard
    title="Resend confirmation email"
    description="We will send a new link to confirm your email address."
    submitLabel="Send new link"
    sentMessage="If that address is waiting to be confirmed, a new link is on its way."
    send={resendVerification}
  />
)
