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

function getColorForChart(color) {
    switch(color) {
        case 'magenta': return 'rgb(255, 0, 255)';
        case 'yellow':  return 'rgb(255, 255, 0)';
        case 'cyan':    return 'rgb(0, 255, 255)';
        case 'black':   return 'rgb(0, 0, 0)';
        default:        return 'rgb(100,100,100)';
    }
}

const PrinterChart = ({location, model, ip, statuses}) => {
    if (!statuses || statuses.length === 0) return <p>Sem dados disponíveis</p>

    const labels = statuses.map((s, index) => `#${index + 1}`);

    const first_counter = statuses[0].total_pages;
    const last_counter = statuses[statuses.length - 1].total_pages;
    const count_printer = (last_counter - first_counter).toString();

    // Definir cores dependendo se a impressora é colorida ou monocromática
    const isColorPrinter = ip === '10.44.0.114'; // ajustar conforme sua lógica
    const tonerColors = isColorPrinter
        ? ['magenta', 'yellow', 'cyan', 'black']
        : ['black'];

// Gerar datasets dinamicamente
    const tonerDatasets = tonerColors.map((color) => ({
        label: `Toner ${color} (%)`,
        data: statuses.map((s) => s[`avg_toner_${color}`]),
        fill: false,
        borderColor: getColorForChart(color),
        tension: 0.3,
        yAxisID: 'y1',
    }));

    // Montar chartData completo
    const chartData = {
        labels,
        datasets: [
            {
                label: `Páginas impressas: ${count_printer}`,
                data: statuses.map((s) => s.total_pages),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.3,
                yAxisID: 'y',
            },
            ...tonerDatasets,
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { display: true },
        },
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: { display: true, text: 'Páginas impressas' },
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                grid: { drawOnChartArea: false },
                title: { display: true, text: 'Nível de toner (%)' },
                min: 0,
                max: 100,
            },
        },
    };

    return (
        <div>
            <h3>
                {location ?? 'Local desconhecido'} - {model ?? 'Modelo desconhecido'} ({ip})
            </h3>
            <Line data={chartData} options={options} />
            <div key={ip}>
                {isColorPrinter ? (
                    <>
                        {tonerColors.map((color) => (
                            <p key={color}>
                                <strong>Unidade de imagem {color}: </strong>
                                {statuses[statuses.length - 1][`avg_toner_${color}`]}(%)
                            </p>
                        ))}
                    </>
                ) : (
                    <p>
                        <strong>Unidade de imagem: </strong>
                        {statuses[statuses.length - 1][`avg_unit_black`]}(%)
                    </p>
                )}
            </div>
        </div>
    );
};

export default PrinterChart;



//     const chartData = {
//         labels,
//         datasets: [
//             {
//                 label: `Páginas impressas: ${count_printer}`,
//                 data: statuses.map((s) => s.total_pages),
//                 fill: false,
//                 borderColor: 'rgb(75, 192, 192)',
//                 tension: 0.3,
//                 yAxisID: 'y',
//             },
//             {
//                 label: `Nível de toner ${last_toner}(%)`,
//                 data: statuses.map((s) => s.avg_toner),
//                 fill: false,
//                 borderColor: 'rgb(255, 99, 132)',
//                 tension: 0.3,
//                 yAxisID: 'y1',
//             },
//         ],
//     };

//     const options = {
//         responsive: true,
//         plugins: {
//             legend: {
//                 display: true,
//             },
//         },
//         scales: {
//             y: {
//                 type: 'linear',
//                 display: true,
//                 position: 'left',
//                 title: {
//                     display: true,
//                     text: 'Páginas impressas',
//                 }
//             },
//             y1: {
//                 type: 'linear',
//                 display: true,
//                 position: 'right',
//                 grid: {
//                     drawOnChartArea: false,
//                 },
//                 title: {
//                     display: true,
//                     text: 'Nível de toner (%)',
//                 },
//                 min: 0,
//                 max: 100,
//             },
//         },
//     };

//     const lastImage = statuses?.[statuses.length - 1]?.avg_unit;


//     return (
//         <div>
//             <h3>
//                 { location ?? 'Local desconhecido' } - { model ?? 'Modelo desconhecido' } ({ip})
//             </h3>
//             <Line data={chartData} options={options} />

//             {ip === '10.44.0.114' ? 
//             (
//                 <>
//                     {['magenta', 'yellow', 'cyan', 'black'].map((color) => (
//                     <p key={color}>
//                         <strong>Unidade de imagem {color}: </strong>
//                         {statuses[statuses.length - 1][`avg_toner_${color}`]}(%)
//                     </p>
//                     ))}
//                 </>
//             ) : (
//                 <p>
//                     <strong>Unidade de imagem: </strong>
//                     {lastImage}(%)  
//                 </p>
//             )}


//         </div>
//     );
// };

// export default PrinterChart;



