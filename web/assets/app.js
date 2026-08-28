(() => {
  const config = window.PQ_CONFIG || {};
  const params = new URLSearchParams(window.location.search);
  const attribution = {
    source: params.get('utm_source') || params.get('source') || 'direct',
    medium: params.get('utm_medium') || params.get('medium') || 'direct',
    campaign: params.get('utm_campaign') || params.get('campaign') || '',
    content: params.get('utm_content') || params.get('content') || ''
  };

  const emit = (event, detail = {}) => {
    const payload = { event, timestamp: new Date().toISOString(), ...attribution, ...detail };
    window.dispatchEvent(new CustomEvent('promptquarry:event', { detail: payload }));
    if (config.analyticsMode === 'console') console.info('[Prompt Quarry]', payload);
  };

  document.querySelectorAll('[data-pq-link="free"]').forEach((link) => {
    if (config.freePackUrl) link.href = config.freePackUrl;
    link.addEventListener('click', () => emit('free_cta_clicked', { product_id: 'pq-developer-starter-pack' }));
  });

  document.querySelectorAll('[data-pq-link="paid"]').forEach((link) => {
    if (config.developerPackCheckoutUrl) {
      link.href = config.developerPackCheckoutUrl;
      link.removeAttribute('aria-disabled');
      link.classList.remove('is-disabled');
    } else if (link.dataset.checkout === 'true') {
      link.href = '#checkout-pending';
      link.setAttribute('aria-disabled', 'true');
      link.classList.add('is-disabled');
    }
    link.addEventListener('click', (event) => {
      emit('paid_cta_clicked', { product_id: 'pq-developer-pack', product_version: '1.0.0' });
      if (!config.developerPackCheckoutUrl && link.dataset.checkout === 'true') event.preventDefault();
    });
  });

  document.querySelectorAll('[data-track="paid-product-view"]').forEach(() => {
    emit('paid_product_viewed', { product_id: 'pq-developer-pack', product_version: '1.0.0' });
  });

  emit('landing_view', { path: window.location.pathname });
})();
