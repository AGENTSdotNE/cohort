import { InboundList } from './inbound-list'

export const InboundPage = () => (
  <div className="mx-auto grid max-w-4xl gap-6">
    <div>
      <h1 className="text-2xl font-semibold">Inbound</h1>
      <p className="text-muted-foreground mt-1">Everything that has arrived, from every channel, in one shared list.</p>
    </div>
    <InboundList />
  </div>
)
