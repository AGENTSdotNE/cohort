import { useUser } from '@/auth/use-user'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const NEXT_STEPS = [
  {
    title: 'Build your first feature',
    description: 'docs/adding-a-feature.md walks through one, from Django model to React page.',
  },
  {
    title: 'Add a page',
    description: 'Create it, then add a route in src/app/router.tsx and a link in src/app/layout/app-nav.tsx.',
  },
  {
    title: 'Add a component',
    description: 'Run npx shadcn@latest add <name> in frontend/ to drop one into src/components/ui.',
  },
]

export const DashboardPage = () => {
  const user = useUser()

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <p className="text-muted-foreground mt-1">
        Signed in as {user.email}. This page is deliberately empty, ready for whatever you build.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {NEXT_STEPS.map(({ title, description }) => (
          <Card key={title}>
            <CardHeader>
              <CardTitle className="text-base">{title}</CardTitle>
              <CardDescription>{description}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>

      <Card className="mt-6 border-dashed">
        <CardHeader>
          <CardTitle className="text-base">Your feature goes here</CardTitle>
          <CardDescription>
            Authentication, email and the app shell are already done, so you can start on the problem itself.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-muted-foreground text-sm">
          Delete this card once you have something real to show.
        </CardContent>
      </Card>
    </div>
  )
}
