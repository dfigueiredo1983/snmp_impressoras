import React, { useState, useEffect } from "react";
import PrinterChart from "../PrinterChart";

export default function BuscarDados() {

    const [ printers, setPrinters ] = useState(null);

    useEffect(() => {       
        const fetchPrinter = async () => {
            try {
                // const response = await fetch('http://localhost:8080/api/printers/')
                console.log("🔄 Executando fetch em:", new Date().toLocaleTimeString());
                // const response = await fetch('http://localhost:8585/api/printers-detail/')
                // const response = await fetch('http://localhost:8585/api/printers-with-history/1/')
                // const response = await fetch('http://localhost:8585/api/printers/6/statuses_chart/')
                // const response = await fetch('http://localhost:8585/api/printers/statuses_chart/')
                const response = await fetch('http://localhost:8585/api/chart')
                if(!response.ok){
                    // console.log('Erro ao buscar os dados');
                    throw new Error(`Http error! status ${response.status}`);
                }
                const result = await response.json();
                setPrinters(result);
                console.log("✅ Dados atualizados:", result);
            } catch (err) {
                console.log('❌ Erro no fecth', err);
            }
        };

        fetchPrinter(); // chama o fetch assim que o componente é criado
        const intervalId = setInterval(fetchPrinter, 300000);
        return () => clearInterval(intervalId);


    }, []); // [] garante que o useEffect roda só uma vez a cada renderização do componente

    console.log('Printer aqui: ', printers)
    return (
        <>
            {printers && (
                <div
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(4, 1fr)',
                        // border: '1px solid red',
                    }}
                >
                    {printers.map((printer) => (
                            // <h1 key={printer.printer.serial}>AQUI</h1>
                            // <p>{printer}</p>
                        <div key={printer.printer.serial}>
                            <PrinterChart
                                location={printer.printer.location}
                                model={printer.printer.model}
                                ip={printer.printer.ip}
                                statuses={printer.statuses}
                            />
                        </div>
                    ))}
                </div>
            )}
        </>
    )

}