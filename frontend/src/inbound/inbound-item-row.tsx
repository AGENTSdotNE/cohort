import type { InboundItem } from './api'
import { ReceivedDate } from './received-date'

const orDash = (value: string) => value.trim() || '-'

export const InboundItemRow = ({ item }: { item: InboundItem }) => (
  <li className="grid gap-1 px-4 py-3">
    <div className="text-muted-foreground flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
      <span className="text-foreground font-mono font-medium">{item.reference}</span>
      <ReceivedDate receivedAt={item.received_at} receivedRaw={item.received_raw} />
      <span className="capitalize">{item.channel}</span>
      <span>{orDash(item.sender)}</span>
    </div>
    <p className="text-sm font-medium">{orDash(item.subject)}</p>
    <p className="text-muted-foreground line-clamp-2 text-sm">{orDash(item.message)}</p>
  </li>
)
