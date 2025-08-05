import React from "react";
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend
);

const PrinterChart = ({location, model, ip, statuses }) => {

    // console.log('PrinterChart')
    // console.log(ip)
    // console.log(statuses)

    const labels = statuses.map((s, index) => `#${index + 1}`);

    const pagesData = {
        labels,
        datasets: [
            {
                label: `Setor: ${location} - Modelo: ${model} - IP: ${ip}`,
                data: statuses.map((s) => s.page_printer),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.3,
            },
        ],
    };

    const tonerData = {
        labels,
        datasets: [
            {
                // `` - usado quando eu quero passar uma variável
                label: `Nível de toner (%)`,
                data: statuses.map((s) => s.toner_printer),
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.3,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
            },
            // y: {
            //     beginAtZero: false,
            //     title: {
            //         display: true,
            //         text: 'Páginas Impressas',
            //     },
            // },
        },
    };

    const lastToner = statuses?.[statuses.length - 1]?.toner_printer;

    return (
        <div style={{ marginBottom: '2rem' }}>
            <h3>
                { location ?? 'Local desconhecido' } - { model ?? 'Modelo desconhecido' } ({ip})
            </h3>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap:'2rem' }}>
                <div style={{ flex: 1, minWidth: 300}}>
                    <Line data={pagesData} options={options} />
                </div>

                <div>
                    <Line data={tonerData} options={options} />
                </div>0

                <p><strong>Nível atual de toner: </strong>{lastToner} (%)</p>

            </div>
        </div>
    );
};

export default PrinterChart;



