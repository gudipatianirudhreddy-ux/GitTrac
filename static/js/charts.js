console.log("Chart JS Loaded");
console.log(languageData);

const ctx = document.getElementById("languageChart");

if (ctx) {
    const chartCtx = ctx.getContext("2d");
    new Chart(chartCtx, {
        type: "pie",
        data: {
            labels: Object.keys(languageData),
            datasets: [{
                label: "Languages",
                data: Object.values(languageData),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1,
            plugins: {
                legend: {
                    position: "right"
                }
            }
        }
    });
}