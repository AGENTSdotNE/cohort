import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Skeleton } from '@/components/ui/skeleton'

import { InboundItemRow } from './inbound-item-row'
import { useInboundItems } from './use-inbound-items'

export const InboundList = () => {
  const { data: items, isPending, isError, error } = useInboundItems()

  if (isPending) return <Skeleton className="h-48 w-full" />

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Could not load inbound items</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </Alert>
    )
  }

  if (items.length === 0) return <p className="text-muted-foreground text-sm">There are no inbound items yet.</p>

  return (
    <ul className="divide-y rounded-md border">
      {items.map((item) => (
        <InboundItemRow key={item.id} item={item} />
      ))}
    </ul>
  )
}
