import { useContext, useState, Dispatch, SetStateAction, createContext } from 'react'

type ContextType = {
    loader: boolean,
    setLoader: Dispatch<SetStateAction<boolean>>,
} | any

const LoaderContext = createContext<ContextType>({});
export function LoaderContextProvider({ children } : {children : any}) {
  const [loader, setLoader] = useState<boolean>(false);
    return (
        <LoaderContext.Provider value={{ loader, setLoader }}>
              {children}
        </LoaderContext.Provider>
    );
}

export const useLoader = () => {
  const { loader, setLoader } = useContext(LoaderContext);
  return {loader, setLoader };
}