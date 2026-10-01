import { Outlet } from 'react-router-dom'

import { APP_NAME } from '@/app/app-name'

import { AppSidebar } from './app-sidebar'
import { MobileNav } from './mobile-nav'
import { UserMenu } from './user-menu'

export const AppShell = () => (
  <div className="flex min-h-svh">
    <AppSidebar />

    <div className="flex min-w-0 flex-1 flex-col">
      <header className="flex h-14 items-center gap-2 border-b px-4">
        <MobileNav />
        <span className="font-semibold md:hidden">{APP_NAME}</span>
        <div className="ml-auto">
          <UserMenu />
        </div>
      </header>

      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  </div>
)
