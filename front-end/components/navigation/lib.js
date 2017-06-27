export const activestate = {
    inserted (el, bindings) {
        if (location.href.includes(el.href)) {
            el.classList.add("is-active")
        }
    }
}
