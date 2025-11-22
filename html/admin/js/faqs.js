document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };

    const faqTableBody = document.getElementById('faq-table-body');
    const modal = document.getElementById('faq-modal');
    const modalTitle = document.getElementById('modal-title');
    const faqForm = document.getElementById('faq-form');
    const faqIdInput = document.getElementById('faq-id');
    const questionInput = document.getElementById('question');
    const answerInput = document.getElementById('answer');
    
    const addFaqButton = document.getElementById('add-faq-button');
    const closeModalButton = document.getElementById('close-modal');
    const cancelButton = document.getElementById('cancel-button');
    const logoutButton = document.getElementById('logout-button');

    const apiBaseUrl = '/api/v1/faqs';

    // --- Funções da API ---

    async function fetchFaqs() {
        try {
            const response = await fetch(apiBaseUrl, { headers });
            if (!response.ok) throw new Error('Falha ao carregar FAQs');
            const faqs = await response.json();
            renderFaqs(faqs);
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }

    async function createFaq(faqData) {
        try {
            const response = await fetch(apiBaseUrl, {
                method: 'POST',
                headers,
                body: JSON.stringify(faqData)
            });
            if (!response.ok) throw new Error('Falha ao criar FAQ');
            await fetchFaqs(); // Recarrega a lista
            closeModal();
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }

    async function updateFaq(id, faqData) {
        try {
            const response = await fetch(`${apiBaseUrl}/${id}`, {
                method: 'PUT',
                headers,
                body: JSON.stringify(faqData)
            });
            if (!response.ok) throw new Error('Falha ao atualizar FAQ');
            await fetchFaqs(); // Recarrega a lista
            closeModal();
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }

    async function deleteFaq(id) {
        if (!confirm('Tem certeza que deseja excluir esta FAQ?')) return;
        try {
            const response = await fetch(`${apiBaseUrl}/${id}`, {
                method: 'DELETE',
                headers
            });
            if (!response.ok) throw new Error('Falha ao excluir FAQ');
            await fetchFaqs(); // Recarrega a lista
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }

    // --- Funções de UI ---

    function renderFaqs(faqs) {
        faqTableBody.innerHTML = '';
        faqs.forEach(faq => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${faq.question}</td>
                <td>${faq.answer}</td>
                <td class="actions">
                    <button class="edit-btn btn-secondary" data-id="${faq.id}">Editar</button>
                    <button class="delete-btn btn-danger" data-id="${faq.id}">Excluir</button>
                </td>
            `;
            faqTableBody.appendChild(row);
        });
    }

    function openModalForCreate() {
        faqForm.reset();
        faqIdInput.value = '';
        modalTitle.textContent = 'Adicionar Nova FAQ';
        modal.style.display = 'block';
    }

    function openModalForEdit(faq) {
        faqForm.reset();
        faqIdInput.value = faq.id;
        questionInput.value = faq.question;
        answerInput.value = faq.answer;
        modalTitle.textContent = 'Editar FAQ';
        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    // --- Event Listeners ---

    addFaqButton.addEventListener('click', openModalForCreate);
    closeModalButton.addEventListener('click', closeModal);
    cancelButton.addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            closeModal();
        }
    });

    faqForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const id = faqIdInput.value;
        const faqData = {
            question: questionInput.value,
            answer: answerInput.value
        };
        if (id) {
            await updateFaq(id, faqData);
        } else {
            await createFaq(faqData);
        }
    });

    faqTableBody.addEventListener('click', async (event) => {
        const target = event.target;
        const id = target.dataset.id;
        if (target.classList.contains('edit-btn')) {
            const response = await fetch(`${apiBaseUrl}/${id}`, { headers });
            const faq = await response.json();
            openModalForEdit(faq);
        }
        if (target.classList.contains('delete-btn')) {
            await deleteFaq(id);
        }
    });
    
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    });

    // Carregamento inicial
    fetchFaqs();
});
