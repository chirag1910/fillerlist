import json
from os import path
from datetime import date


def add(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        with open(analytics_file_path, "r") as f:
            ips_data = json.loads(f.read())

        ips_data["data"].append({"ip": ip, "date": str(date.today())})

        with open(analytics_file_path, "w") as f:
            f.write(json.dumps(ips_data, indent=4))

    except:
        None


def get():
    def to_date(date_string):
        date_list = date_string.split("-")
        return date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

    def day(analytics_data, date=date.today()):
        ip_list = []

        for element in analytics_data:
            if(element["date"] == str(date)):
                ip_list.append(element["ip"])

        return ip_list

    def same_month(analytics_data):
        ip_list = []
        today = date.today()

        for element in analytics_data:
            visit_date = to_date(element["date"])
            if (visit_date.month == today.month) and (visit_date.year == today.year):
                ip_list.append(element["ip"])

        return ip_list

    def same_year(analytics_data):
        ip_list = []
        today = date.today()

        for element in analytics_data:
            if to_date(element["date"]).year == today.year:
                ip_list.append(element["ip"])

        return ip_list

    def all_time(analytics_data):
        ip_list = []

        for element in analytics_data:
            ip_list.append(element["ip"])

        return ip_list

    def graph_data(analytics_data):
        dates = []

        for element in analytics_data:
            if(element["date"] not in dates):
                dates.append(element["date"])

        dates = sorted(dates, key=lambda x: to_date(x))

        graph_data_list = []

        for date in dates:
            ip_list = day(analytics_data, date)
            graph_data_list.append({"date": date, "visits": len(
                ip_list), "unique_visits": len(set(ip_list))})

        return graph_data_list

    def create_graph_script(graph_data_list):
        labels = []
        visits_data = []
        unique_visits_data = []

        for entry in graph_data_list:
            labels.append(entry["date"])
            visits_data.append(entry["visits"])
            unique_visits_data.append(entry["unique_visits"])

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

    try:
        with open(analytics_file_path, "r") as f:
            analytics_data = json.loads(f.read())["data"]

        ip_list = all_time(analytics_data)
        total_visits = len(ip_list)
        total_unique_visits = len(set(ip_list))

        ip_list = same_year(analytics_data)
        year_vists = len(ip_list)
        year_unique_visits = len(set(ip_list))

        ip_list = same_month(analytics_data)
        month_vists = len(ip_list)
        month_unique_visits = len(set(ip_list))

        ip_list = day(analytics_data)
        day_vists = len(ip_list)
        day_unique_visits = len(set(ip_list))

        graph_data_list = graph_data(analytics_data)
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

    except:
        return {
            "all_time": 0,
            "all_time_unique": 0,
            "year": 0,
            "year_unique": 00,
            "month": 0,
            "month_unique_visits": 0,
            "day": 0,
            "day_unique_visits": 0,
            "graph_script": ""
        }


analytics_file_path = path.join(path.dirname(
    path.abspath(__file__)), "analytics_data.json")
