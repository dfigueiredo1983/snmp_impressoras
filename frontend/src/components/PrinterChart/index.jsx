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

    const chartData = {
        labels: statuses.map((s, index) => `#${index + 1}`),
        datasets: [
            {
                label: `Setor: ${location} - Modelo: ${model} - IP: ${ip}`,
                data: statuses.map((s) => s.page_printer),
                fill: false,
                borderColor: 'rgb(75, 192, 192',
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
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Páginas Impressas',
                },
            },
        },
    };

    const lastToner = statuses?.[statuses.length - 1]?.toner_printer;
    // const location = statuses?.[statuses.length - 1]?.toner_printer;
    // console.log('Nível de toner: ', lastToner);

    console.log(location)

    return (
        <div style={{ maxWidth: '600px', marginBottom: '2rem' }}>
            <Line data={chartData} options={options}/>
            <p>
                <strong>Nível atual de toner: </strong>
                {lastToner ?? 'N/A'}%
           </p>
        </div>
    );
};

export default PrinterChart;



