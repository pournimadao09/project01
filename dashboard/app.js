function loadData() {
    fetch("/status")
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById("data");
            tbody.innerHTML = "";

            Object.keys(data).forEach(sensor => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${sensor}</td>
                    <td>${data[sensor].value}</td>
                    <td class="${data[sensor].status}">
                        ${data[sensor].status}
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error("Error:", err));
}

setInterval(loadData, 2000);
loadData();
