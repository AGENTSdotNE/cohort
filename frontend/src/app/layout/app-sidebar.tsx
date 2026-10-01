import { APP_NAME } from '@/app/app-name'

import { AppNav } from './app-nav'

export const AppSidebar = () => (
  <aside className="bg-sidebar hidden w-56 shrink-0 border-r md:block">
    <div className="flex h-14 items-center border-b px-4">
      <span className="font-semibold">{APP_NAME}</span>
    </div>

    <AppNav />
  </aside>
)
