document.addEventListener('DOMContentLoaded', function () {
    // ищем все password input'ы
    const pwdFields = document.querySelectorAll('input[type="password"]');

    pwdFields.forEach(function (field) {
        // создаём обёртку вокруг поля
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';  // ширина = ширине инпута

        // вставляем обёртку вместо инпута
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        // добавим отступ справа, чтобы текст не налезал на иконку
        const currentPaddingRight = window.getComputedStyle(field).paddingRight;
        const extraPadding = 30; // px под иконку
        const currentPaddingRightNum = parseInt(currentPaddingRight || '0', 10);
        field.style.paddingRight = (currentPaddingRightNum + extraPadding) + 'px';

        // создаём иконку-глаз
        const img = document.createElement('img');
        img.src = '/static/admin/icons/icon-openeye.png';  // открытый глаз
        img.alt = 'Показать пароль';

        // все критичные стили задаём инлайном, чтобы точно сработало
        img.style.position = 'absolute';
        img.style.right = '8px';
        img.style.top = '50%';
        img.style.transform = 'translateY(-50%)';
        img.style.width = '20px';
        img.style.height = '20px';
        img.style.cursor = 'pointer';
        img.style.userSelect = 'none';
        img.style.filter = "invert(1)"

        wrapper.appendChild(img);

        img.addEventListener('click', () => {
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            img.src = isPassword
                ? '/static/admin/icons/icon-closeeye.png'   // закрытый глаз
                : '/static/admin/icons/icon-openeye.png';   // открытый глаз
            img.alt = isPassword ? 'Скрыть пароль' : 'Показать пароль';
        });
    });
});