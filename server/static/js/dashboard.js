document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/nat-table')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#nat-table tbody");
            data.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${row.source_ip}</td>
                    <td>${row.source_port}</td>
                    <td>${row.external_ip}</td>
                    <td>${row.external_port}</td>
                `;
                tableBody.appendChild(tr);
            });
        });
});
