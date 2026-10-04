/* ==========================================
   VENUE360 - UNIFIED JAVASCRIPT CONTROLLER
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss toast notifications after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    });

    // Handle tab switching in student and admin portals
    window.switchTab = function(tabId) {
        const url = new URL(window.location.href);
        url.searchParams.set('tab', tabId);
        window.history.pushState({}, '', url);

        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `tab-${tabId}`);
        });
    };

    // Attach tab button click handlers
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.dataset.tab) {
                switchTab(btn.dataset.tab);
            }
        });
    });

    // Check URL params for initial active tab
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');
    if (activeTab) {
        switchTab(activeTab);
    }

    // Modal Control Functions
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    };

    // Close modal on clicking outside box
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Event Details Popup Modal Trigger
    window.openEventDetails = function(eventData, isRegistered, isLoggedIn) {
        const modal = document.getElementById('eventDetailsModal');
        if (!modal) return;

        const imgName = eventData.image || 'club.jpeg';
        document.getElementById('modalEventPoster').style.backgroundImage = `url('/static/images/${imgName}')`;
        document.getElementById('modalEventTitle').innerText = eventData.title || 'Event Details';
        document.getElementById('modalEventSociety').innerText = eventData.society || 'University Society';
        document.getElementById('modalEventCategory').innerText = eventData.type || 'General Event';
        document.getElementById('modalEventDateTime').innerText = `${eventData.date || ''} at ${eventData.time || ''}`;
        document.getElementById('modalEventVenue').innerText = eventData.venue || 'Campus Venue';
        document.getElementById('modalEventDescription').innerText = eventData.description || 'No description provided.';

        const priceBadge = document.getElementById('modalEventPrice');
        if (eventData.fee_type === 'Paid' && eventData.price && eventData.price !== 'Free') {
            priceBadge.className = 'badge badge-paid';
            priceBadge.innerText = `PKR ${eventData.price}`;
        } else {
            priceBadge.className = 'badge badge-free';
            priceBadge.innerText = 'FREE';
        }

        const actionContainer = document.getElementById('modalEventActionContainer');
        if (!isLoggedIn) {
            actionContainer.innerHTML = `
                <button onclick="closeModal('eventDetailsModal'); openModal('authModal');" class="btn btn-primary" style="width: 100%; padding: 0.75rem;">
                    Sign In to Register
                </button>`;
        } else if (isRegistered) {
            actionContainer.innerHTML = `
                <button class="btn btn-secondary" style="width: 100%; opacity: 0.7; padding: 0.75rem;" disabled>
                    <i class="fa-solid fa-check"></i> Already Registered
                </button>`;
        } else {
            actionContainer.innerHTML = `
                <form action="/student/register-event/${eventData.id}" method="POST">
                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 0.75rem;">
                        Register for Event
                    </button>
                </form>`;
        }

        openModal('eventDetailsModal');
    };

    // Quick Live Search filter
    window.filterCards = function(inputId, containerSelector, itemSelector, textSelector) {
        const input = document.getElementById(inputId);
        if (!input) return;

        const filter = input.value.toLowerCase().trim();
        const items = document.querySelectorAll(`${containerSelector} ${itemSelector}`);

        items.forEach(item => {
            const targetEl = item.querySelector(textSelector);
            const targetText = targetEl ? targetEl.textContent.toLowerCase() : item.textContent.toLowerCase();
            item.style.display = targetText.includes(filter) ? '' : 'none';
        });
    };
});
