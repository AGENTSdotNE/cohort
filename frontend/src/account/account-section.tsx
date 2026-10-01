import type { ReactNode } from 'react'

type AccountSectionProps = { title: string; description: string; children: ReactNode }

export const AccountSection = ({ title, description, children }: AccountSectionProps) => (
  <section className="grid gap-4">
    <div>
      <h3 className="font-medium">{title}</h3>
      <p className="text-muted-foreground text-sm">{description}</p>
    </div>
    {children}
  </section>
)
