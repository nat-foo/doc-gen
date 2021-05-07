import { RoutineCall } from "@example/routine_call"
import { Transition } from "@example/transition"
import { Sprite } from "@example/sprite"
import { ReactNode, useState } from 'react'

export interface phaseProps {
  children: ReactNode
  id?: number
  routineCallsOnce?: RoutineCall[]
  routineCallsRecurring?: RoutineCall[]
  transitions?: Transition[]
  sprites?: Sprite[]
}

export const Phase = ({
  children,
  id = -1,
  routineCallsOnce = [],
  routineCallsRecurring = [],
  transitions = [],
  sprites = [],
}: phaseProps) => {
  const [_id, setId] = useState<number>(id)
  const [_routineCallsOnce, setRoutineCallsOnce] = useState<RoutineCall[]>(routineCallsOnce)
  const [_routineCallsRecurring, setRoutineCallsRecurring] = useState<RoutineCall[]>(routineCallsRecurring)
  const [_transitions, setTransitions] = useState<Transition[]>(transitions)
  const [_sprites, setSprites] = useState<Sprite[]>(sprites)

  return (
    {children}
  )
}

export default Phase

