(function () {
  function normalize(value) {
    return (value || '').toString().toLowerCase().trim();
  }

  function closeSelect(wrapper) {
    if (!wrapper) return;

    const dropdown = wrapper.querySelector('.searchable-select-dropdown');
    if (dropdown) dropdown.hidden = true;

    wrapper.classList.remove('is-open');
  }

  function closeAll(exceptWrapper) {
    document.querySelectorAll('.searchable-select.is-open').forEach(function (wrapper) {
      if (wrapper !== exceptWrapper) {
        closeSelect(wrapper);
      }
    });
  }

  function enhanceSearchableSelect(wrapper) {
    if (wrapper.dataset.searchableReady === 'true') return;

    const select = wrapper.querySelector('select');
    if (!select) return;

    wrapper.dataset.searchableReady = 'true';
    wrapper.classList.add('searchable-select-enhanced');

    const placeholder = wrapper.dataset.searchPlaceholder || 'Поиск';

    const control = document.createElement('div');
    control.className = 'searchable-select-control';

    const input = document.createElement('input');
    input.type = 'search';
    input.className = 'searchable-select-input';
    input.placeholder = placeholder;
    input.autocomplete = 'off';

    const arrow = document.createElement('span');
    arrow.className = 'searchable-select-arrow';
    arrow.innerHTML = '<i class="bi bi-chevron-down"></i>';

    const dropdown = document.createElement('div');
    dropdown.className = 'searchable-select-dropdown';
    dropdown.hidden = true;

    control.appendChild(input);
    control.appendChild(arrow);

    wrapper.insertBefore(control, select);
    wrapper.appendChild(dropdown);

    function getOptions() {
      return Array.from(select.options);
    }

    function getSelectedOption() {
      return getOptions().find(function (option) {
        return option.selected;
      });
    }

    function syncInputFromSelect() {
      const selected = getSelectedOption();

      if (selected && selected.value) {
        input.value = selected.textContent.trim();
      } else {
        input.value = '';
      }
    }

    function renderOptions() {
      const query = normalize(input.value);
      dropdown.innerHTML = '';

      let visibleCount = 0;

      getOptions().forEach(function (option) {
        const text = option.textContent.trim();
        const value = option.value;
        const isEmptyOption = value === '';
        const matches = normalize(text).includes(query);

        if (query && !matches && !isEmptyOption) return;

        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'searchable-select-option';
        item.textContent = text;

        if (option.selected) {
          item.classList.add('is-selected');
        }

        item.addEventListener('click', function () {
          select.value = option.value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          input.value = option.value ? text : '';
          closeSelect(wrapper);
        });

        dropdown.appendChild(item);
        visibleCount += 1;
      });

      if (!visibleCount) {
        const empty = document.createElement('div');
        empty.className = 'searchable-select-empty';
        empty.textContent = 'Совпадений не найдено';
        dropdown.appendChild(empty);
      }
    }

    function openSelect() {
      closeAll(wrapper);
      renderOptions();
      dropdown.hidden = false;
      wrapper.classList.add('is-open');
    }

    function toggleSelect() {
      if (wrapper.classList.contains('is-open')) {
        closeSelect(wrapper);
        input.blur();
      } else {
        openSelect();
        input.focus();
      }
    }

    syncInputFromSelect();

    control.addEventListener('click', function (event) {
      event.stopPropagation();

      const clickedInput = event.target === input;

      if (clickedInput && !wrapper.classList.contains('is-open')) {
        openSelect();
        return;
      }

      if (!clickedInput) {
        toggleSelect();
      }
    });

    input.addEventListener('focus', function () {
      if (!wrapper.classList.contains('is-open')) {
        openSelect();
      }
    });

    input.addEventListener('input', function () {
      renderOptions();
      dropdown.hidden = false;
      wrapper.classList.add('is-open');

      if (!input.value.trim()) {
        select.value = '';
        select.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    input.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closeSelect(wrapper);
        input.blur();
      }
    });

    select.addEventListener('change', function () {
      syncInputFromSelect();
      renderOptions();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-searchable-select]').forEach(enhanceSearchableSelect);

    document.addEventListener('click', function (event) {
      if (!event.target.closest('.searchable-select')) {
        closeAll(null);
      }
    });
  });
})();