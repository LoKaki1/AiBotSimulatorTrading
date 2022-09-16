import React, { useContext, useState, Dispatch, SetStateAction, createContext } from 'react'

type ContextType = {
    ticker: string,
    setTicker: Dispatch<SetStateAction<string>> | any
}
const TickerContext = createContext<ContextType>({ticker: '', setTicker: null});
export function TickerProvider({ children } : {children : any}) {
  const [ticker, setTicker] = useState<string>('');
    return (
        <TickerContext.Provider value={{ ticker, setTicker }}>
              {children}
        </TickerContext.Provider>
    )
}

export const useTicker = () => {
  const { ticker, setTicker } = useContext(TickerContext)
  return {ticker, setTicker }
}
