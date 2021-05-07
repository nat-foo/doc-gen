import { Phase } from "@example/phase"
import { PhaseLimit } from "@example/phase_limit"
import { ReactNode, useState } from 'react'

export interface actionProps {
  children: ReactNode
  name?: string
  isDefault?: boolean
  phases?: Phase[]
  phaseLimits?: PhaseLimit[]
}

export const Action = ({
  children,
  name = "unspecifiedAction",
  isDefault = false,
  phases = [],
  phaseLimits = [],
}: actionProps) => {
  const [_name, setName] = useState<string>(name)
  const [_isDefault, setIsDefault] = useState<boolean>(isDefault)
  const [_phases, setPhases] = useState<Phase[]>(phases)
  const [_phaseLimits, setPhaseLimits] = useState<PhaseLimit[]>(phaseLimits)

  return (
    {children}
  )
}

export default Action

