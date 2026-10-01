import { LogOut, Settings } from 'lucide-react'
import { useState } from 'react'

import { AccountDialog } from '@/account/account-dialog'
import { signOut } from '@/auth/api'
import { useSession } from '@/auth/use-session'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { UserAvatar } from '@/components/user-avatar'
import { clearSession } from '@/lib/query-client'

export const UserMenu = () => {
  const { data: user } = useSession()
  const [accountOpen, setAccountOpen] = useState(false)

  const leave = async () => {
    await signOut()
    clearSession()
  }

  if (!user) return null

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="h-9 gap-2 px-2">
            <UserAvatar user={user} />
            <span className="sr-only text-sm sm:not-sr-only">{user.full_name || user.email}</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end" className="w-56">
          <DropdownMenuLabel className="font-normal">
            <p className="text-sm font-medium">{user.full_name || 'Signed in'}</p>
            <p className="text-muted-foreground text-xs">{user.email}</p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem onSelect={() => setAccountOpen(true)}>
            <Settings className="size-4" />
            Account settings
          </DropdownMenuItem>
          <DropdownMenuItem onSelect={() => void leave()}>
            <LogOut className="size-4" />
            Sign out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <AccountDialog open={accountOpen} onOpenChange={setAccountOpen} />
    </>
  )
}
