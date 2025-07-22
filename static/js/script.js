let isSimplifiedView = false;

function toggleTableView() {
    const tableHeader = document.getElementById('table-header');
    const tableBody = document.getElementById('table-body');
    const fetchMoreButton = document.getElementById('fetch-more');

    if (!isSimplifiedView) {
        // Simplified view: show only TransactionID and Fraud Status
        tableHeader.innerHTML = `
            <tr>
                <th>Transaction ID</th>
                <th>Fraud Status</th>
            </tr>
        `;
        const rows = tableBody.getElementsByTagName('tr');
        for (let row of rows) {
            row.innerHTML = `
                <td>${row.cells[0].innerText}</td>
                <td class="${row.cells[4].className}">${row.cells[4].innerText}</td>
            `;
        }
        fetchMoreButton.innerText = 'Show Details';
        isSimplifiedView = true;
    } else {
        // Full view: reload to restore original table
        window.location.reload();
    }
}