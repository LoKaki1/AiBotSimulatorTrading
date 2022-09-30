import { useContext, useState, Dispatch, SetStateAction, createContext } from 'react'
import { CandleType } from '../../Common/Types/CandleType';

type ContextType = {
    historicalData: CandleType[],
    setHistoricalData: Dispatch<SetStateAction<CandleType>>,
} | any

const historicalDataContext = createContext<ContextType>({});
export function HistoricalDataContextProvider({ children } : {children : any}) {
  const [historicalData, setHistoricalData] = useState<CandleType[]>([]);
    return (
        <historicalDataContext.Provider value={{ historicalData, setHistoricalData }}>
              {children}
        </historicalDataContext.Provider>
    );
}

export const useHistoricalData = () => {
  const { historicalData, setHistoricalData } = useContext(historicalDataContext);
  return {historicalData, setHistoricalData };
}