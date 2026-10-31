/**
 * EduTrack - Main Application JavaScript
 * Handles interactive modals, AJAX CRUD operations, validation feedback, and sidebar toggling.
 */

document.addEventListener('DOMContentLoaded', () => {

    // ----------------------------------------------------
    // 1. Mobile Sidebar Toggle
    // ----------------------------------------------------
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');

    if (mobileToggle && sidebar && backdrop) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            backdrop.classList.toggle('hidden');
        });

        backdrop.addEventListener('click', () => {
            sidebar.classList.remove('open');
            backdrop.classList.add('hidden');
        });
    }

    // ----------------------------------------------------
    // 2. Toast Notifications Helper
    // ----------------------------------------------------
    window.showToast = function (message, type = 'success') {
        const toastEl = document.getElementById('liveToast');
        const toastMsg = document.getElementById('toastMessage');
        if (!toastEl || !toastMsg) return;

        // Reset classes
        toastEl.className = 'toast align-items-center text-white border-0 shadow-lg rounded-xl';
        if (type === 'success') {
            toastEl.classList.add('bg-indigo-600');
        } else if (type === 'danger') {
            toastEl.classList.add('bg-rose-600');
        } else if (type === 'warning') {
            toastEl.classList.add('bg-amber-600');
        } else {
            toastEl.classList.add('bg-slate-800');
        }

        toastMsg.innerHTML = message;
        const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
        toast.show();
    };

    // ----------------------------------------------------
    // 3. Clear Validation State Helper
    // ----------------------------------------------------
    function clearFormValidation(form) {
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(el => el.textContent = '');
    }

    function applyFormErrors(form, errors, alertBox) {
        if (alertBox) {
            const firstErr = Object.values(errors)[0];
            alertBox.textContent = firstErr || 'Please correct the highlighted errors.';
            alertBox.classList.remove('d-none');
        }

        for (const [field, message] of Object.entries(errors)) {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('is-invalid');
                let feedback = input.closest('.col-md-6, .col-md-3, .col-12')?.querySelector('.invalid-feedback');
                if (!feedback) {
                    feedback = input.nextElementSibling;
                }
                if (feedback && feedback.classList.contains('invalid-feedback')) {
                    feedback.textContent = message;
                }
            }
        }
    }

    // ----------------------------------------------------
    // 4. Add Student Form (AJAX submission)
    // ----------------------------------------------------
    const addStudentForm = document.getElementById('addStudentForm');
    const addModalEl = document.getElementById('addStudentModal');
    const addSubmitBtn = document.getElementById('addSubmitBtn');
    const addFormAlert = document.getElementById('addFormAlert');

    if (addStudentForm) {
        addStudentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearFormValidation(addStudentForm);
            if (addFormAlert) addFormAlert.classList.add('d-none');

            // Button loading state
            if (addSubmitBtn) {
                addSubmitBtn.disabled = true;
                addSubmitBtn.querySelector('.normal-state')?.classList.add('d-none');
                addSubmitBtn.querySelector('.loading-state')?.classList.remove('d-none');
            }

            const formData = new FormData(addStudentForm);
            const payload = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(addStudentForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    // Hide Modal
                    const modal = bootstrap.Modal.getInstance(addModalEl);
                    if (modal) modal.hide();
                    addStudentForm.reset();

                    showToast(result.message || 'Student added successfully!', 'success');

                    // If currently on students or dashboard, refresh to show new data
                    setTimeout(() => {
                        window.location.reload();
                    }, 800);
                } else {
                    applyFormErrors(addStudentForm, result.errors || {}, addFormAlert);
                }
            } catch (err) {
                console.error('Error adding student:', err);
                if (addFormAlert) {
                    addFormAlert.textContent = 'Server communication error. Please try again.';
                    addFormAlert.classList.remove('d-none');
                }
            } finally {
                if (addSubmitBtn) {
                    addSubmitBtn.disabled = false;
                    addSubmitBtn.querySelector('.normal-state')?.classList.remove('d-none');
                    addSubmitBtn.querySelector('.loading-state')?.classList.add('d-none');
                }
            }
        });
    }

    // ----------------------------------------------------
    // 5. Edit Student Button & Form Handling
    // ----------------------------------------------------
    const editModalEl = document.getElementById('editStudentModal');
    const editStudentForm = document.getElementById('editStudentForm');
    const editSubmitBtn = document.getElementById('editSubmitBtn');
    const editFormAlert = document.getElementById('editFormAlert');

    let editModal = null;
    if (editModalEl) {
        editModal = new bootstrap.Modal(editModalEl);
    }

    document.querySelectorAll('.edit-student-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const studentId = btn.getAttribute('data-student-id');
            if (!studentId || !editModalEl) return;

            clearFormValidation(editStudentForm);
            if (editFormAlert) editFormAlert.classList.add('d-none');

            try {
                const response = await fetch(`/students/${studentId}/json`);
                if (!response.ok) throw new Error('Could not retrieve student details.');

                const student = await response.json();

                // Populate Form Fields
                document.getElementById('edit_student_id').value = student.id;
                document.getElementById('edit_full_name').value = student.full_name;
                document.getElementById('edit_roll_number').value = student.roll_number;
                document.getElementById('edit_email').value = student.email;
                document.getElementById('edit_phone').value = student.phone_number;
                document.getElementById('edit_department').value = student.department;
                document.getElementById('edit_year_semester').value = student.year_semester;
                document.getElementById('edit_status').value = student.status;

                editStudentForm.action = `/students/edit/${student.id}`;

                editModal.show();
            } catch (error) {
                console.error(error);
                showToast('Failed to load student details for editing.', 'danger');
            }
        });
    });

    if (editStudentForm) {
        editStudentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearFormValidation(editStudentForm);
            if (editFormAlert) editFormAlert.classList.add('d-none');

            if (editSubmitBtn) {
                editSubmitBtn.disabled = true;
                editSubmitBtn.querySelector('.normal-state')?.classList.add('d-none');
                editSubmitBtn.querySelector('.loading-state')?.classList.remove('d-none');
            }

            const formData = new FormData(editStudentForm);
            const payload = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(editStudentForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    editModal.hide();
                    showToast(result.message || 'Student updated successfully!', 'success');
                    setTimeout(() => {
                        window.location.reload();
                    }, 700);
                } else {
                    applyFormErrors(editStudentForm, result.errors || {}, editFormAlert);
                }
            } catch (err) {
                console.error('Error editing student:', err);
                if (editFormAlert) {
                    editFormAlert.textContent = 'Server error while updating. Please try again.';
                    editFormAlert.classList.remove('d-none');
                }
            } finally {
                if (editSubmitBtn) {
                    editSubmitBtn.disabled = false;
                    editSubmitBtn.querySelector('.normal-state')?.classList.remove('d-none');
                    editSubmitBtn.querySelector('.loading-state')?.classList.add('d-none');
                }
            }
        });
    }

    // ----------------------------------------------------
    // 6. Delete Student Prompt & Confirmation
    // ----------------------------------------------------
    const deleteModalEl = document.getElementById('deleteStudentModal');
    const deleteStudentForm = document.getElementById('deleteStudentForm');
    const deleteStudentName = document.getElementById('deleteStudentName');
    const deleteStudentRoll = document.getElementById('deleteStudentRoll');

    let deleteModal = null;
    if (deleteModalEl) {
        deleteModal = new bootstrap.Modal(deleteModalEl);
    }

    document.querySelectorAll('.delete-student-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const studentId = btn.getAttribute('data-student-id');
            const studentName = btn.getAttribute('data-student-name');
            const studentRoll = btn.getAttribute('data-student-roll');

            if (!studentId || !deleteModal) return;

            deleteStudentName.textContent = studentName || 'Unknown Student';
            deleteStudentRoll.textContent = studentRoll || '';
            deleteStudentForm.action = `/students/delete/${studentId}`;

            deleteModal.show();
        });
    });

    if (deleteStudentForm) {
        deleteStudentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actionUrl = deleteStudentForm.action;

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const result = await response.json();
                deleteModal.hide();

                if (response.ok && result.success) {
                    showToast(result.message || 'Student record deleted successfully.', 'danger');
                    setTimeout(() => {
                        window.location.reload();
                    }, 700);
                } else {
                    showToast('Failed to delete student.', 'danger');
                }
            } catch (err) {
                console.error('Error deleting student:', err);
                // Fallback standard submit
                deleteStudentForm.submit();
            }
        });
    }
});
