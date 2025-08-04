import React, { useState, useEffect } from "react";
import PrinterChart from "../PrinterChart";
// import React from "react";

export default function BuscarDados() {

    const [ printers, setPrinters ] = useState(null);
    const [ loading, setLoading ] = useState(false);
    const [ error, setError ] = useState(null);

    useEffect(() => {       
        const fetchPrinter = async () => {
            setLoading(true);
            setError(null);
            try {
                // const response = await fetch('http://localhost:8080/api/printers/')
                const response = await fetch('http://localhost:8080/api/printers-detail/')
                if(!response.ok){
                    // console.log('Erro ao buscar os dados');
                    throw new Error(`Http error! status ${response.status}`);
                }
                const result = await response.json();
                
                console.log('Result: ', result);
                setPrinters(result);
            } catch (err) {
                // console.log('Erro no fecth');
                setError(err);
            } finally {
                // console.log('Terminou o fetch');
                setLoading(false);
            }
        };

        fetchPrinter(); // chama o fetch assim que o componente é criado
    }, []); // [] garante que o useEffect roda só uma vez a cada renderização do componente

    // const location = printers?.[printers.length - 1]?.location;
    // const model = printers?.[printers.length - 1]?.model;

    return (
        <div>
            <h1>Gráficos por Impressoras</h1>
            {loading && <p>Carregando impressoras...</p>}
            {error && <p style={{ color: 'red'}}>Error: {error}</p>}

            {printers && (
                <div>
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
        </div>
    )
}