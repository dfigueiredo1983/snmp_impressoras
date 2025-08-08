import React, { useState, useEffect } from "react";
import PrinterChart from "../PrinterChart";
// import React from "react";

export default function BuscarDados() {

    const [ printers, setPrinters ] = useState(null);

    useEffect(() => {       
        const fetchPrinter = async () => {
            try {
                // const response = await fetch('http://localhost:8080/api/printers/')
                const response = await fetch('http://localhost:8585/api/printers-detail/')
                if(!response.ok){
                    // console.log('Erro ao buscar os dados');
                    throw new Error(`Http error! status ${response.status}`);
                }
                const result = await response.json();
                
                // console.log('Result: ', result);
                setPrinters(result);
            } catch (err) {
                console.log('Erro no fecth', err);
            } finally {
                console.log('Terminou o fetch');
            }
        };

        fetchPrinter(); // chama o fetch assim que o componente é criado
    }, []); // [] garante que o useEffect roda só uma vez a cada renderização do componente

    // const location = printers?.[printers.length - 1]?.location;
    // const model = printers?.[printers.length - 1]?.model;

    return (
        <>
            {printers && (
                <div
                    style={{
                        columnCount: '3',
                        width: '100%',
                        // // display: "flex",
                        // display: "",
                        // border: "1px solid red",
                        // gap: "20px",
                        // flexWrap: "wrap",
                        // alignItems: "flex-start"
                    }}
                >
                    {printers.map((printer) => (
                        <PrinterChart
                            key={printer.id}
                            location={printer.location}
                            model={printer.model}
                            ip={printer.ip}
                            statuses={printer.statuses}
                        />
                    ))}
                </div>
            )}
        </>
    )

    // <div
    //     style={{
    //         display: "flex",
    //         gap: "20px",
    //         flexWrap: "wrap",
    //         alignItems: "flex-start"
    //     }}
    // >
    //     {printers.map((printer) => (
    //         <PrinterChart
    //             key={printer.id}
    //             location={printer.location}
    //             model={printer.model}
    //             ip={printer.ip}
    //             statuses={printer.statuses}
    //         />
    //     ))}
    // </div>



}