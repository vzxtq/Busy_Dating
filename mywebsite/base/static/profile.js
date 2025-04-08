
        const addPhotoButton = document.getElementById('addPhotoButton');
        const fileInput = document.getElementById('fileInput');
    
        addPhotoButton.addEventListener('click', () => {
            fileInput.click();
        });
    
        fileInput.addEventListener('change', (event) => {
            const files = event.target.files;
    
            if (files.length === 0) {
                console.log("No files selected.");
                return;
            }
    
            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('profilePhotos', files[i]);
            }
    
            fetch('/upload_photos/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success && Array.isArray(data.profilePhotos)) {
                    const gallery = document.querySelector('.photo-gallery');
                    
                    const placeholder = gallery.querySelector('.add-photo-btn');
                    if (placeholder) {
                        placeholder.remove();
                    }
                    data.profilePhotos.forEach(profilePhoto => {
                        const photoItem = document.createElement('div');
                        photoItem.className = 'photo-item';
                        photoItem.dataset.photoId = profilePhoto.id;

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox'
                        checkbox.className = 'photo-checkbox';

                        const img = document.createElement('img');
                        img.src = profilePhoto.url;
                        img.alt = 'Gallery Photo';
                        img.style = "width: 100%; height: 200px; object-fit: cover; border-radius: 8px; transition: transform 0.3s ease, box-shadow 0.3s ease;";

                        photoItem.appendChild(checkbox);
                        photoItem.appendChild(img);
                        gallery.appendChild(photoItem);
                    });
                } else {
                    console.error("Unexpected response:", data);
                }
            })
            .catch(error => {
                console.error('Error occurred while uploading photos:', error.message);
                alert("Failed to upload photos. Please try again later.");
            });
        });

        document.addEventListener('DOMContentLoaded', () => {
            const deleteBtn = document.getElementById('deleteSelectedBtn');
            const gallery = document.querySelector('.photo-gallery');
        
            deleteBtn.addEventListener('click', () => {
                const selectedCheckboxes = document.querySelectorAll('.photo-checkbox:checked');
        
                if (selectedCheckboxes.length === 0) {
                    alert('Please select photos to delete.');
                    return;
                }
        
                if (!confirm('Are you sure you want to delete the selected photos?')) {
                    return;
                }
                const photoIds = Array.from(selectedCheckboxes).map(checkbox =>
                    checkbox.closest('.photo-item').dataset.photoId
                );
        
                fetch('/delete_selected_photos/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ photo_ids: photoIds }) 
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete photos');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        selectedCheckboxes.forEach(checkbox => {
                            checkbox.closest('.photo-item').remove();
                        });

                        const remainingPhotoItems = gallery.querySelectorAll('.photo-item');
                        if (remainingPhotoItems.length === 0) {
                            const placeholder = document.createElement('div');
                            placeholder.className = 'add-photo-btn';
                            placeholder.id = 'photoHolder';
                            placeholder.innerHTML = '<span>No photos yet</span>';
                            gallery.appendChild(placeholder);
                        }
                    } else {
                        console.error('Error:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Error occurred:', error);
                    alert('Failed to delete photos. Please try again later.');
                });
            });
        });
