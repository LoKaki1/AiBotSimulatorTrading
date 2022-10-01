import { useContext, useState, Dispatch, SetStateAction, createContext } from 'react'
import { CandleType } from '../../Common/Types/CandleType';

type ContextType = {
    interval: string,
    setInterval: Dispatch<SetStateAction<string>>,
} | any

const intervalContext = createContext<ContextType>({});
export function IntervalContextProvider({ children } : {children : any}) {
  const [interval, setInterval] = useState<string>('1d');
    return (
        <intervalContext.Provider value={{ interval, setInterval }}>
              {children}
        </intervalContext.Provider>
    );
}

export const useInterval = () => {
  const { interval, setInterval } = useContext(intervalContext);
  return {interval, setInterval };
}