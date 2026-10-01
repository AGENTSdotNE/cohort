import { Menu } from 'lucide-react'
import { useState } from 'react'

import { APP_NAME } from '@/app/app-name'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from '@/components/ui/sheet'

import { AppNav } from './app-nav'

export const MobileNav = () => {
  const [open, setOpen] = useState(false)

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden" aria-label="Open menu">
          <Menu />
        </Button>
      </SheetTrigger>

      <SheetContent side="left" className="w-56 gap-0 p-0" aria-describedby={undefined}>
        <SheetTitle className="flex h-14 items-center border-b px-4">{APP_NAME}</SheetTitle>
        <AppNav onNavigate={() => setOpen(false)} />
      </SheetContent>
    </Sheet>
  )
}
