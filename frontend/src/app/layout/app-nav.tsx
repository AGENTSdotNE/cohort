import { LayoutDashboard } from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { cn } from '@/lib/utils'

// Add your own pages here as you build them. The sidebar and the mobile menu both read this list.
const LINKS = [{ to: '/', label: 'Dashboard', icon: LayoutDashboard }]

export const AppNav = ({ onNavigate }: { onNavigate?: () => void }) => (
  <nav className="grid gap-1 p-2">
    {LINKS.map(({ to, label, icon: Icon }) => (
      <NavLink
        key={to}
        to={to}
        end
        onClick={onNavigate}
        className={({ isActive }) =>
          cn(
            'flex items-center gap-2 rounded-md px-3 py-2 text-sm',
            isActive ? 'bg-accent text-accent-foreground font-medium' : 'text-muted-foreground hover:bg-accent/50',
          )
        }
      >
        <Icon className="size-4" />
        {label}
      </NavLink>
    ))}
  </nav>
)
