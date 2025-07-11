

document.addEventListener('DOMContentLoaded', function() {
  // Путь к вашему API-эндпоинту (меняйте при необходимости)
  const url = '/api/admin_stats';

  fetch(url, {
    credentials: 'same-origin'  // чтобы передавались куки сессии admin
  })
    .then(response => {
      if (!response.ok) throw new Error(`Network error: ${response.status}`);
      return response.json();
    })
    .then(data => {
      // маппинг ключей из JSON в id элементов в DOM
      const fields = {
        active_day:      'stats-active-day',
        active_week:     'stats-active-week',
        active_month:    'stats-active-month',
        sessions_gt1:    'stats-sessions-gt1',
        return_rate:     'stats-return-rate',
        messages_total:  'stats-messages-total',
        messages_avg:    'stats-messages-avg',
        percent_active:  'stats-percent-active',
        percent_subscribers: 'stats-percent-subscribers'
      };

      // заполняем простые поля
      Object.entries(fields).forEach(([key, elId]) => {
        const el = document.getElementById(elId);
        if (el && data[key] !== undefined) {
          el.textContent = data[key];
        }
      });

      // заполняем список топ-команд
      if (Array.isArray(data.top_commands)) {
        const ul = document.getElementById('stats-top-commands');
        if (ul) {
          ul.innerHTML = '';
          data.top_commands.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.command} — ${item.count}`;
            ul.appendChild(li);
          });
        }
      }
    })
    .catch(err => {
      console.error('Ошибка при получении статистики:', err);
    });
});
