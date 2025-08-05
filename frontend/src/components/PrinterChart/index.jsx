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

    const chartData = {
        labels,
        datasets: [
            {
                label: 'Páginas impressas',
                data: statuses.map((s) => s.page_printer),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.3,
                yAxisID: 'y',
            },
            {
                label: 'Nível de toner (%)',
                data: statuses.map((s) => s.toner_printer),
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.3,
                yAxisID: 'y1',
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
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Páginas impressas',
                }
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                grid: {
                    drawOnChartArea: false,
                },
                title: {
                    display: true,
                    text: 'Nível de toner (%)',
                },
                min: 0,
                max: 100,
            
            },
        },
    };

    const lastToner = statuses?.[statuses.length - 1]?.toner_printer;

    return (
        <div style={{ maxWidth: '600px', marginBottom: '2rem' }}>
        {/* <div style={{ width: '100%', marginBottom: '2rem' }}> */}
            <h3>
                { location ?? 'Local desconhecido' } - { model ?? 'Modelo desconhecido' } ({ip})
            </h3>

            <Line data={chartData} options={options} />

            <p><strong>Nível atual de toner: </strong>{lastToner} (%)</p>

        </div>
    );
};

export default PrinterChart;



