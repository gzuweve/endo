// Обработка клика по иконке пользователя
document.addEventListener('DOMContentLoaded', function() {
    const userIcon = document.getElementById('userIcon');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (userIcon) {
        userIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });
    }

    // Закрытие dropdown при клике вне его области
    window.addEventListener('click', function() {
        if (dropdownMenu) {
            dropdownMenu.classList.remove('show');
        }
    });

    // Предотвращение закрытия при клике внутри dropdown
    if (dropdownMenu) {
        dropdownMenu.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Добавляем анимацию при наведении на заказы
    const orderItems = document.querySelectorAll('.order-item');
    orderItems.forEach(item => {
        // Пропускаем пустые элементы
        if (!item.querySelector('.order-title')) return;

        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        });
    });

    // Добавляем обработку клавиатуры для доступности
    orderItems.forEach(item => {
        if (!item.querySelector('.order-title')) return;

        item.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });

        // Делаем заказы фокусируемыми для клавиатуры
        item.setAttribute('tabindex', '0');
    });

    // Функция для обновления статуса заказа (можно использовать для drag&drop)
    function updateOrderStatus(orderId, newStatus) {
        const csrfToken = getCSRFToken();

        fetch('/api/orders/update_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                order_id: orderId,
                status: newStatus
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Статус заказа обновлен', 'success');
                // Обновляем интерфейс
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showNotification('Ошибка обновления статуса', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка соединения', 'error');
        });
    }

    // Вспомогательная функция для получения CSRF токена
    function getCSRFToken() {
        const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfCookie ? csrfCookie.split('=')[1] : '';
    }

    // Функция для показа уведомлений
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '1000';
        notification.style.minWidth = '300px';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Инициализация drag and drop (опционально)
    initializeDragAndDrop();
});

// Функция для инициализации drag and drop между колонками
function initializeDragAndDrop() {
    const orderItems = document.querySelectorAll('.order-item[draggable="true"]');

    orderItems.forEach(item => {
        item.setAttribute('draggable', 'true');

        item.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', this.dataset.orderId);
            this.classList.add('dragging');
        });

        item.addEventListener('dragend', function() {
            this.classList.remove('dragging');
        });
    });

    const columns = document.querySelectorAll('.orders-section');

    columns.forEach(column => {
        column.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        column.addEventListener('dragleave', function() {
            this.classList.remove('drag-over');
        });

        column.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');

            const orderId = e.dataTransfer.getData('text/plain');
            const newStatus = this.classList.contains('pending-orders') ? 'pending' :
                            this.classList.contains('in-progress-orders') ? 'processing' :
                            'completed';

            updateOrderStatus(orderId, newStatus);
        });
    });
}

// Экспортируем функции для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initializeDragAndDrop, showNotification };
}