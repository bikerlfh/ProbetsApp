import { truncateSync } from 'fs';
import React from 'react'
import {Radar} from 'react-chartjs-2';

const data = {
  labels: ['won games', 'lost games', 'won pdt', 'lost pdt'],
  datasets: [
    {
        label: 'Home Stats',
        data: [9, 10, 5, 2],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
    },
    {
        label: 'Away Stats',
        data: [15, 5, 10, 2],
        backgroundColor: 'rgb(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235)',
        borderWidth: 1,
    }
  ],
}

const options = {
  scale: {
    ticks: { beginAtZero: true },
  },
}

const RadarChart = () => (
  <>
    <div className='header'>
      <h1 className='title'>Radar Chart</h1>
      <div className='links'>
        <a
          className='btn btn-gh'
          href='https://github.com/reactchartjs/react-chartjs-2/blob/react16/example/src/charts/Radar.js'
        >
          Github Source
        </a>
      </div>
    </div>
    <Radar data={data} options={options} />
  </>
)

export default RadarChart