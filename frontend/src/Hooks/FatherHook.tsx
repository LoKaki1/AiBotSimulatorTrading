import React from "react";
import { TickerProvider } from "./Context/TickerContext";

export default function FatherHook({ children }: { children: any }) {
  return (
    <>
      <TickerProvider>{children}</TickerProvider>
    </>
  );
}
