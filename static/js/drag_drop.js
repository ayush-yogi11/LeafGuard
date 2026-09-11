/**
 * Handles drag-and-drop + click-to-browse file selection, live image
 * preview, and a loading spinner on form submission.
 *
 * Design note: we reuse Django's ImageUploadForm's hidden <input type="file">
 * (rendered by {{ form.image }}) rather than creating a separate input,
 * so server-side validation (size/type/integrity) still runs unchanged —
 * this script only improves the UX around that same input.
 */
document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('id_image');
    const promptEl = document.getElementById('drop-zone-prompt');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('image-preview');
    const fileNameEl = document.getElementById('file-name');
    const submitBtn = document.getElementById('submit-btn');
    const scanForm = document.getElementById('scan-form');
    const spinner = document.getElementById('spinner');
    const submitLabel = document.getElementById('submit-label');

    // Clicking anywhere in the drop zone opens the native file picker
    dropZone.addEventListener('click', () => fileInput.click());

    // Visual feedback while dragging a file over the zone
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-active');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-active');
        });
    });

    // Handle a dropped file: assign it to the real input so Django's
    // form processes it exactly like a normal file-picker selection.
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    // Handle a file chosen via the native picker
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Basic client-side sanity check — NOT a substitute for the
        // server-side validation in ImageUploadForm.clean_image(), which
        // still runs and is the actual source of truth.
        if (!file.type.match('image/(jpeg|png)')) {
            alert('Please select a JPG or PNG image.');
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            fileNameEl.textContent = file.name;
            promptEl.classList.add('hidden');
            previewContainer.classList.remove('hidden');
            submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Show a spinner and disable the button on submit, so users can't
    // double-submit while inference is running (which can take a couple
    // seconds on CPU).
    scanForm.addEventListener('submit', () => {
        submitBtn.disabled = true;
        spinner.classList.remove('hidden');
        submitLabel.textContent = 'Analyzing...';
    });
});