import { apiRequest } from '@/lib/api-client'

export type InboundItem = {
  id: number
  reference: string
  received_raw: string
  received_at: string | null
  channel: string
  sender: string
  subject: string
  message: string
  logged_by: string
}

export const fetchInboundItems = () => apiRequest<InboundItem[]>('/inbound/')
