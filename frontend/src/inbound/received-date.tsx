import { TriangleAlert } from 'lucide-react'

import { Badge } from '@/components/ui/badge'

import { formatReceivedDate } from './format-received-date'

type ReceivedDateProps = { receivedAt: string | null; receivedRaw: string }

export const ReceivedDate = ({ receivedAt, receivedRaw }: ReceivedDateProps) => {
  if (receivedAt) {
    return (
      <time dateTime={receivedAt} title={receivedRaw}>
        {formatReceivedDate(receivedAt)}
      </time>
    )
  }

  return (
    <span className="flex items-center gap-2" title={receivedRaw ? `Received as "${receivedRaw}"` : undefined}>
      Date unknown
      <Badge variant="destructive">
        <TriangleAlert />
        Urgent
      </Badge>
    </span>
  )
}
