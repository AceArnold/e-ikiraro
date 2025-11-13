// This script will collect the documents of the user from the database and display them as clickable links.

document.addEventListener('DOMContentLoaded', function() {
    // Fetch documents from the backend API
    fetch('http://127.0.0.1:8000/api/documents/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const documentsContainer = document.getElementById('documents-container');
            
            // Check if there are any documents
            if (!data || data.length === 0) {
                documentsContainer.innerHTML = '<p>No documents found.</p>';
                return;
            }
            
            // Display each document
            data.forEach(doc => {
                const item = document.createElement('div');
                item.style.marginBottom = '10px';
                
                const link = document.createElement('a');
                link.href = `http://127.0.0.1:8000/${doc.file}`;
                link.textContent = `${doc.document_type} - ${new Date(doc.uploaded_at).toLocaleDateString()}`;
                link.target = '_blank';
                link.style.textDecoration = 'none';
                link.style.color = '#007bff';
                
                item.appendChild(link);
                documentsContainer.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error fetching documents:', error);
            const documentsContainer = document.getElementById('documents-container');
            documentsContainer.innerHTML = `<p style="color: red;">Error loading documents: ${error.message}</p>`;
        });
});