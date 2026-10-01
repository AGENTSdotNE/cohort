import type { ReactNode } from 'react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

type AuthCardProps = { title: string; description?: string; children?: ReactNode; footer?: ReactNode }

export const AuthCard = ({ title, description, children, footer }: AuthCardProps) => (
  <div className="bg-muted/40 flex min-h-svh items-center justify-center p-6">
    <div className="w-full max-w-sm">
      <Card>
        <CardHeader>
          {/* shadcn's CardTitle is a div, but this is the page's main heading. */}
          <CardTitle asChild>
            <h1 className="text-xl">{title}</h1>
          </CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent>{children}</CardContent>
      </Card>
      {footer && <div className="text-muted-foreground mt-4 text-center text-sm">{footer}</div>}
    </div>
  </div>
)
