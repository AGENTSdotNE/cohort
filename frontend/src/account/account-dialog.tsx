import { useUser } from '@/auth/use-user'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Separator } from '@/components/ui/separator'

import { AccountSection } from './account-section'
import { AvatarPicker } from './avatar-picker'
import { ChangePasswordForm } from './change-password-form'
import { ProfileForm } from './profile-form'

type AccountDialogProps = { open: boolean; onOpenChange: (open: boolean) => void }

export const AccountDialog = ({ open, onOpenChange }: AccountDialogProps) => {
  const user = useUser()

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90svh] gap-6 overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Account settings</DialogTitle>
          <DialogDescription>You sign in as {user.email}.</DialogDescription>
        </DialogHeader>

        <AccountSection title="Profile" description="Your picture and name are shown in the app.">
          <AvatarPicker />
          <ProfileForm />
        </AccountSection>

        <Separator />

        <AccountSection title="Password" description="You will stay signed in here. Other devices are signed out.">
          <ChangePasswordForm />
        </AccountSection>
      </DialogContent>
    </Dialog>
  )
}
