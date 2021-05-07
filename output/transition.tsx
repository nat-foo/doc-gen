
import { ReactNode, useState } from 'react'

export interface transitionProps {
  children: ReactNode
  name?: string
  description?: string
  Behaviour: () => void
}

export const Transition = ({
  children,
  name = "unspecifiedTransition",
  description = "A transition description.",
  Behaviour,
}: transitionProps) => {
  const [_name, setName] = useState<string>(name)
  const [_description, setDescription] = useState<string>(description)
  const [_Behaviour, setBehaviour] = useState<() => void>(Behaviour)

  return (
    {children}
  )
}

export default Transition

