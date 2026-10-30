/**
 * DevScribe / Flask Blogging Platform - Main Client Script
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Quill Rich Text Editor if container exists
    const editorContainer = document.getElementById('editor-container');
    const hiddenTextarea = document.getElementById('editor-textarea');
    const postForm = document.getElementById('post-form');

    if (editorContainer && hiddenTextarea) {
        // Hide default textarea visually (kept in DOM for Flask-WTF validation and submission)
        hiddenTextarea.style.display = 'none';

        // Initialize Quill
        const quill = new Quill('#editor-container', {
            theme: 'snow',
            placeholder: 'Write your story using rich text formatting, headings, code snippets...',
            modules: {
                toolbar: [
                    [{ 'header': [2, 3, 4, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    ['link', 'clean']
                ]
            }
        });

        // Pre-fill existing content for Edit mode
        if (hiddenTextarea.value.trim() !== '') {
            quill.root.innerHTML = hiddenTextarea.value;
        }

        // On form submission, sync Quill HTML to hidden textarea
        if (postForm) {
            postForm.addEventListener('submit', function (e) {
                const htmlContent = quill.root.innerHTML;
                // If editor is empty (just <p><br></p>), set empty string so required validator catches it
                if (htmlContent === '<p><br></p>' || quill.getText().trim().length === 0) {
                    hiddenTextarea.value = '';
                } else {
                    hiddenTextarea.value = htmlContent;
                }
            });
        }
    }

    // 2. Auto-dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // 3. Demo Login Autofill Helpers
    const fillAlexBtn = document.getElementById('btn-demo-alex');
    const fillSarahBtn = document.getElementById('btn-demo-sarah');
    const emailOrUserInput = document.getElementById('email_or_username');
    const passwordInput = document.getElementById('password');

    if (fillAlexBtn && emailOrUserInput && passwordInput) {
        fillAlexBtn.addEventListener('click', function () {
            emailOrUserInput.value = 'alex_dev';
            passwordInput.value = 'password123';
        });
    }

    if (fillSarahBtn && emailOrUserInput && passwordInput) {
        fillSarahBtn.addEventListener('click', function () {
            emailOrUserInput.value = 'sarah_tech';
            passwordInput.value = 'password123';
        });
    }

    // 4. Smooth Anchor Scrolling for Comments
    if (window.location.hash) {
        const target = document.querySelector(window.location.hash);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }
});
