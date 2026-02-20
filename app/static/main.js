// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('navToggle');
    var links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', function() {
            links.classList.toggle('open');
        });
    }

    // Animated counters
    var counters = document.querySelectorAll('[data-target]');
    if (counters.length > 0) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function(counter) {
            observer.observe(counter);
        });
    }

    // Page view tracking
    trackPageView();
});

function animateCounter(el) {
    var target = parseInt(el.getAttribute('data-target'));
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1500;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.floor(eased * target);
        el.textContent = current + (current >= target ? '+' : '') + suffix;
        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            el.textContent = target + '+' + suffix;
        }
    }
    requestAnimationFrame(step);
}

function trackPageView() {
    var visitorId = localStorage.getItem('gbx_vid');
    if (!visitorId) {
        visitorId = 'v_' + Math.random().toString(36).substring(2, 15);
        localStorage.setItem('gbx_vid', visitorId);
    }

    var params = new URLSearchParams(window.location.search);

    fetch('/api/v1/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            page: window.location.pathname,
            referrer: document.referrer || null,
            utm_source: params.get('utm_source') || null,
            utm_campaign: params.get('utm_campaign') || null,
            visitor_id: visitorId
        })
    }).catch(function() {});
}
