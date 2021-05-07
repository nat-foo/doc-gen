
import { ReactNode, useState } from 'react'

export interface routineCallProps {
  children: ReactNode
  routineName?: string
  args?: any[]
}

export const RoutineCall = ({
  children,
  routineName = "unspecifiedRoutine",
  args = [],
}: routineCallProps) => {
  const [_routineName, setRoutineName] = useState<string>(routineName)
  const [_args, setArgs] = useState<any[]>(args)

  return (
    {children}
  )
}

export default RoutineCall

