
import { ReactNode, useState } from 'react'

export interface spriteProps {
  children: ReactNode
  name?: string
  speed?: number
  xOffset?: number
  yOffset?: number
  width?: number
  height?: number
  maskWidth?: number
  maskHeight?: number
  maskLeft?: number
  maskRight?: number
  maskTop?: number
  maskBottom?: number
}

export const Sprite = ({
  children,
  name = "unspecifiedSprite",
  speed = 1,
  xOffset = 0,
  yOffset = 0,
  width = 32,
  height = 32,
  maskWidth = 32,
  maskHeight = 32,
  maskLeft = 0,
  maskRight = 0,
  maskTop = 0,
  maskBottom = 0,
}: spriteProps) => {
  const [_name, setName] = useState<string>(name)
  const [_speed, setSpeed] = useState<number>(speed)
  const [_xOffset, setXOffset] = useState<number>(xOffset)
  const [_yOffset, setYOffset] = useState<number>(yOffset)
  const [_width, setWidth] = useState<number>(width)
  const [_height, setHeight] = useState<number>(height)
  const [_maskWidth, setMaskWidth] = useState<number>(maskWidth)
  const [_maskHeight, setMaskHeight] = useState<number>(maskHeight)
  const [_maskLeft, setMaskLeft] = useState<number>(maskLeft)
  const [_maskRight, setMaskRight] = useState<number>(maskRight)
  const [_maskTop, setMaskTop] = useState<number>(maskTop)
  const [_maskBottom, setMaskBottom] = useState<number>(maskBottom)

  return (
    {children}
  )
}

export default Sprite

