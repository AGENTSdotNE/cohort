import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'

export const NotFoundPage = () => (
  <div className="mx-auto max-w-md text-center">
    <h1 className="text-2xl font-semibold">Page not found</h1>
    <p className="text-muted-foreground mt-1">Check the address, or head back to the dashboard.</p>
    <Button asChild className="mt-4">
      <Link to="/">Go to dashboard</Link>
    </Button>
  </div>
)
