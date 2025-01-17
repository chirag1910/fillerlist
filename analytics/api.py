from django.utils import timezone
from analytics.models import Analytic


def add(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    Analytic.objects.create(ip_address=ip, time=timezone.now())


def get():
    def create_graph_script(graph_data_list):
        labels = [entry["date"].strftime('%d-%m-%Y') for entry in graph_data_list]
        visits_data = [entry["visits"] for entry in graph_data_list]
        unique_visits_data = [entry["unique_visits"] for entry in graph_data_list]

        code = f'''
            <script>
                var chart;
                var data;
                var congif;
                var leftHandle;
                var righthandle;

                const resetGraph = () => {{
                    const graphContainer = document.querySelector(".chart-container");
                    document.querySelector("#chart").remove();
                    const canvasElement = document.createElement("CANVAS");
                    canvasElement.id = "chart";
                    graphContainer.insertBefore(canvasElement, graphContainer.firstChild);
                    chart?.destroy();
                }}

                const drawChart = (left = 0, right = {len(labels)}) => {{
                    data = {{
                        labels: {str(labels)}.slice(left, right),
                        datasets: [{{
                            backgroundColor: 'rgba(255, 127, 80, 0.2)',
                            borderColor: 'rgba(255, 127, 80, 0.8)',
                            pointBackgroundColor: 'rgba(255, 127, 80, 1)',
                            pointRadius: 4,
                            pointHitRadius: 10,
                            pointHoverRadius: 7,
                            data: {str(visits_data)}.slice(left, right),
                        }},
                        {{
                            backgroundColor: 'rgba(253, 137, 40, 0.2)',
                            borderColor: 'rgba(253, 137, 40, 0.8)',
                            pointBackgroundColor: 'rgba(253, 137, 40, 1)',
                            pointRadius: 4,
                            pointHitRadius: 10,
                            pointHoverRadius: 7,
                            data: {str(unique_visits_data)}.slice(left, right),
                        }}
                        ]
                    }};

                    config = {{
                        type: 'line',
                        data: data,
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            layout: {{
                                padding: {{
                                    top : 30,
                                    bottom: 20,
                                    left: 20,
                                    right: 20
                                }}
                            }},
                            legend: {{
                                display: false
                            }},
                            scales: {{
                                xAxes: [{{
                                    gridLines: {{
                                        display: false
                                    }},
                                    ticks: {{
                                        fontColor: "#e6e6e6",
                                        padding: 20,
                                    }}
                                }}],
                                yAxes: [{{
                                    gridLines: {{
                                        display: false
                                    }},
                                    ticks: {{
                                        fontColor: "#e6e6e6",
                                        padding: 20,
                                    }}
                                }}]
                            }},
                            animation: {{
                                duration: 0
                            }}
                        }},
                    }};

                    chart = new Chart(
                        document.getElementById('chart'),
                        config
                    );
                }}

                resetGraph();
                drawChart(0, 0);

                const data2 = {{
                    labels: {str(labels)},
                    datasets: [{{
                        backgroundColor: 'rgba(255, 127, 80, 0.2)',
                        borderColor: 'rgba(255, 127, 80, 0.8)',
                        pointBackgroundColor: 'rgba(255, 127, 80, 1)',
                        pointRadius: 0,
                        pointHitRadius: 0,
                        pointHoverRadius: 0,
                        data: {str(visits_data)},
                    }}]
                }};

                const config2 = {{
                    type: 'line',
                    data: data2,
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        layout: {{
                            padding: 0
                        }},
                        legend: {{
                            display: false
                        }},
                        scales: {{
                            xAxes: [{{
                                gridLines: {{
                                    display: false
                                }},
                                ticks: {{
                                    display: false
                                }}
                            }}],
                            yAxes: [{{
                                gridLines: {{
                                    display: false
                                }},
                                ticks: {{
                                    display: false
                                }}
                            }}]
                        }},
                        animation: {{
                            duration: 0
                        }}
                    }},
                }};

                const chart2 = new Chart(
                    document.getElementById('chart-thumbnail'),
                    config2
                );

                const onResize = () => {{
                    resetGraph();
                    leftHandle = Math.floor((range.offsetLeft / container.offsetWidth) * {len(labels)});
                    righthandle = Math.ceil(((range.offsetLeft + range.offsetWidth) / container.offsetWidth) * {len(labels)});
                    drawChart(leftHandle, righthandle);
                    setCustomCount({visits_data}.slice(leftHandle, righthandle).reduce((a, b) => a + b, 0));
                }};

                new ResizeObserver(onResize).observe(range);
            </script>
        '''

        return code

    current_time = timezone.now()

    current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    day_vists = Analytic.objects.get_visits(current_time)
    day_unique_visits = Analytic.objects.get_visits(current_time, unique=True)

    current_time = current_time.replace(day=1)

    month_vists = Analytic.objects.get_visits(current_time)
    month_unique_visits = Analytic.objects.get_visits(current_time, unique=True)

    current_time = current_time.replace(month=1)

    year_vists = Analytic.objects.get_visits(current_time)
    year_unique_visits = Analytic.objects.get_visits(current_time, unique=True)

    total_visits = Analytic.objects.get_visits(current_time)
    total_unique_visits = Analytic.objects.get_visits(current_time, unique=True)

    graph_data_list = [
        {
            "date": entry["day"],
            "visits": entry["total"],
            "unique_visits": entry["unique"]
        } for entry in Analytic.objects.get_daily_trend()
    ]

    graph_script = create_graph_script(graph_data_list)

    return {
        "all_time": total_visits,
        "all_time_unique": total_unique_visits,
        "year": year_vists,
        "year_unique": year_unique_visits,
        "month": month_vists,
        "month_unique_visits": month_unique_visits,
        "day": day_vists,
        "day_unique_visits": day_unique_visits,
        "graph_script": graph_script
    }
