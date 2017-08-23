export const checkstate = {
    inserted (el, binding) {
        const ctrl = el.querySelector("input")
        const toggle = () => {
            if (ctrl && ctrl.checked) {
                el.classList.add("is-active")
            }
            else {
                el.classList.remove("is-active")
            }
        }
        
        toggle()
        
        if (ctrl) {
            ctrl.addEventListener("change", (e) => {
                if(e.target.type == "radio") {
                    el.parentElement.querySelectorAll("label").forEach(
                        (lbl) => {
                            lbl.classList.remove("is-active")
                        }
                    )
                }
                
                toggle()
            })
        }
        
    }
}
