document.addEventListener('DOMContentLoaded', () => {
    const filterType = document.getElementById('filterType');
    const filterByQuarter = document.getElementById('filterByQuarter');
    const filterByMonth = document.getElementById('filterByMonth');

    filterType.addEventListener('change', () => {
        if(filterType.value === 'month') {
            filterByQuarter.classList.add('hidden');
            filterByQuarter.classList.remove('block');

            filterByMonth.classList.add('block');
            filterByMonth.classList.remove('hidden');
        }else {
            filterByMonth.classList.add('hidden');
            filterByMonth.classList.remove('block');

            filterByQuarter.classList.add('block');
            filterByQuarter.classList.remove('hidden');           
        }
    })

    var columnChart = new ej.charts.Chart({
        //Initializing Primary X Axis
        primaryXAxis: {
            valueType: 'Category',
            title: 'Revenue',
        },
        //Initializing Primary Y Axis
         primaryYAxis: {
            title: 'Revenue per quarter'
        },

        //Initializing Chart Series
        series: [
            {
                type: 'Column',
                dataSource: [
                    { country: "First", medal: 50 },
                    { country: "Second", medal: 40 },
                    { country: "Third", medal: 70 },
                    { country: "Fouth", medal: 60 },
                ],
                xName: 'country',
                yName: 'medal',
            }
        ],
    });
    columnChart.appendTo('#columnChartContainer');


    var pieChart = new ej.charts.AccumulationChart({
        //Initializing Series
        series: [
            {
                type: 'Pie',
                dataSource: [
                    { country: "First", medal: 50 },
                    { country: "Second", medal: 40 },
                    { country: "Third", medal: 70 },
                    { country: "Fourth", medal: 60 },
                ],
                xName: 'country',
                yName: 'medal',
                dataLabel: {
                    visible: true,
                    position: 'Outside',
                    name: 'Revenue',
                }
            }
        ],
        legendSettings: {
            visible: true,
        },
    });
    pieChart.appendTo('#pieChartContainer');

    var lineChart = new ej.charts.Chart({
        //Initializing Primary X Axis
        primaryXAxis: {
            valueType: 'Category',
            title: 'Revenue',
        },
        //Initializing Primary Y Axis
        primaryYAxis: {
            title: 'Revenue per quarter'
        },
    
        //Initializing Chart Series
        series: [
            {
                type: 'Line',
                dataSource: [
                    { country: "First", medal: 50 },
                    { country: "Second", medal: 40 },
                    { country: "Third", medal: 70 },
                    { country: "Fourth", medal: 60 },
                ],
                xName: 'country',
                yName: 'medal',
                marker: {
                    visible: true,
                    width: 10,
                    height: 10
                }
            }
        ],
    });
    lineChart.appendTo('#lineChartContainer');


    var rangeAreaChart = new ej.charts.Chart({
        //Initializing Primary X Axis
        primaryXAxis: {
            valueType: 'Category',
            title: 'Revenue',
        },
        //Initializing Primary Y Axis
        primaryYAxis: {
            title: 'Revenue per quarter'
        },
    
        //Initializing Chart Series
        series: [
            {
                type: 'RangeArea',
                dataSource: [
                    { country: "First", low: 30, high: 50 },
                    { country: "Second", low: 25, high: 40 },
                    { country: "Third", low: 50, high: 70 },
                    { country: "Fourth", low: 40, high: 60 },
                ],
                xName: 'country',
                high: 'high',
                low: 'low',
                name: 'Medals',
                opacity: 0.5
            }
        ],
    });
    rangeAreaChart.appendTo('#rangeAreaChartContainer');
})