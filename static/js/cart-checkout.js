/**
 * LUXE & CO. — Cart & Checkout Logic
 * Standalone file — does not modify main.js
 */

document.addEventListener('DOMContentLoaded', () => {

    const TAX_RATE = 0.08;

    /* =============================================
       UTILITY HELPERS
       ============================================= */
    const fmt = (n) => '$' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    const recalcTotals = () => {
        let subtotal = 0;

        // Desktop rows
        document.querySelectorAll('#cartBody tr').forEach(row => {
            const price = parseFloat(row.dataset.price);
            const qty   = parseInt(row.querySelector('.qty-input').value);
            const sub   = price * qty;
            row.querySelector('.cart-subtotal').textContent = fmt(sub);
            subtotal += sub;
        });

        // Mobile cards
        document.querySelectorAll('#cartMobileCards .cart-mobile-item').forEach(card => {
            const price = parseFloat(card.dataset.price);
            const qty   = parseInt(card.querySelector('.qty-input').value);
            const sub   = price * qty;
            card.querySelector('.cart-subtotal').textContent = fmt(sub);
        });

        const tax   = subtotal * TAX_RATE;
        const total = subtotal + tax;

        const elSub   = document.getElementById('summarySubtotal');
        const elTax   = document.getElementById('summaryTax');
        const elTotal = document.getElementById('summaryTotal');

        if (elSub)   elSub.textContent   = fmt(subtotal);
        if (elTax)   elTax.textContent   = fmt(tax);
        if (elTotal) elTotal.textContent = fmt(total);

        checkEmpty();
    };

    const checkEmpty = () => {
        const rows    = document.querySelectorAll('#cartBody tr');
        const wrapper = document.querySelector('.row.g-5');
        const empty   = document.getElementById('cartEmpty');
        if (!rows.length && wrapper && empty) {
            wrapper.classList.add('d-none');
            empty.classList.remove('d-none');
        }
    };

    /* =============================================
       QUANTITY BUTTONS  (+/-)
       ============================================= */
    const bindQtyButtons = (scope) => {
        scope.querySelectorAll('.qty-plus').forEach(btn => {
            btn.addEventListener('click', () => {
                const input = btn.closest('.qty-control').querySelector('.qty-input');
                if (parseInt(input.value) < 10) {
                    input.value = parseInt(input.value) + 1;
                    syncMirror(btn, input.value);
                    recalcTotals();
                }
            });
        });

        scope.querySelectorAll('.qty-minus').forEach(btn => {
            btn.addEventListener('click', () => {
                const input = btn.closest('.qty-control').querySelector('.qty-input');
                if (parseInt(input.value) > 1) {
                    input.value = parseInt(input.value) - 1;
                    syncMirror(btn, input.value);
                    recalcTotals();
                }
            });
        });
    };

    /* Keep desktop & mobile in sync */
    const syncMirror = (originBtn, val) => {
        const container = originBtn.closest('[data-id]');
        if (!container) return;
        const id = container.dataset.id;

        document.querySelectorAll(`[data-id="${id}"] .qty-input`).forEach(inp => {
            inp.value = val;
        });
    };

    /* =============================================
       REMOVE SINGLE ITEM
       ============================================= */
    const bindRemoveButtons = (scope) => {
        scope.querySelectorAll('.cart-remove-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const container = btn.closest('[data-id]');
                if (!container) return;
                const id = container.dataset.id;

                // Animate out
                document.querySelectorAll(`[data-id="${id}"]`).forEach(el => {
                    el.style.transition = 'opacity 0.35s, transform 0.35s';
                    el.style.opacity = '0';
                    el.style.transform = 'translateX(30px)';
                    setTimeout(() => el.remove(), 350);
                });

                setTimeout(recalcTotals, 380);
            });
        });
    };

    /* =============================================
       CLEAR ENTIRE CART
       ============================================= */
    const clearBtn = document.getElementById('clearCartBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const allItems = document.querySelectorAll('#cartBody tr, #cartMobileCards .cart-mobile-item');
            allItems.forEach((el, i) => {
                el.style.transition = `opacity 0.3s ${i * 0.08}s, transform 0.3s ${i * 0.08}s`;
                el.style.opacity = '0';
                el.style.transform = 'translateX(40px)';
            });
            setTimeout(() => {
                allItems.forEach(el => el.remove());
                recalcTotals();
            }, allItems.length * 80 + 320);
        });
    }

    /* =============================================
       INIT BINDINGS ON CART PAGE
       ============================================= */
    const cartDesktop = document.getElementById('cartTableDesktop');
    const cartMobile  = document.getElementById('cartMobileCards');

    if (cartDesktop) bindQtyButtons(cartDesktop);
    if (cartMobile)  bindQtyButtons(cartMobile);
    if (cartDesktop) bindRemoveButtons(cartDesktop);
    if (cartMobile)  bindRemoveButtons(cartMobile);


    /* =============================================
       CHECKOUT – Payment method toggle
       ============================================= */
    window.selectPayment = (el) => {
        document.querySelectorAll('.payment-option').forEach(opt => opt.classList.remove('selected'));
        el.classList.add('selected');
        el.querySelector('input[type="radio"]').checked = true;

        const cardSection = document.getElementById('cardDetails');
        if (!cardSection) return;
        const val = el.querySelector('input').value;
        cardSection.style.display = val === 'card' ? 'block' : 'none';
    };

    /* =============================================
       CHECKOUT – Form submit
       ============================================= */
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Simple client-side validation highlight
            let valid = true;
            checkoutForm.querySelectorAll('[required]').forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e74c3c';
                    valid = false;
                } else {
                    field.style.borderColor = '#ddd';
                }
            });

            if (!valid) {
                checkoutForm.querySelector('[required]:invalid, [required]')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

            // Success state
            const btn = checkoutForm.querySelector('.btn-place-order') || document.querySelector('.btn-place-order');
            if (btn) {
                btn.textContent = 'Processing...';
                btn.style.pointerEvents = 'none';
                btn.style.opacity = '0.7';
            }

            setTimeout(() => {
                alert('Order placed successfully! Thank you for shopping with LUXE & CO.');
                if (btn) {
                    btn.textContent = 'Place Order';
                    btn.style.pointerEvents = '';
                    btn.style.opacity = '';
                }
            }, 1800);
        });
    }

    /* =============================================
       CHECKOUT – Card number formatting
       ============================================= */
    const cardNumInput = document.getElementById('ckCardNum');
    if (cardNumInput) {
        cardNumInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '').substring(0, 16);
            e.target.value = v.replace(/(.{4})/g, '$1  ').trim();
        });
    }

    const cardExpInput = document.getElementById('ckCardExp');
    if (cardExpInput) {
        cardExpInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '').substring(0, 4);
            if (v.length >= 3) v = v.substring(0, 2) + ' / ' + v.substring(2);
            e.target.value = v;
        });
    }
});
