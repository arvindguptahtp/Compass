import FoldUnfold from './forms/fold-unfold.vue'
import { checkstate } from './forms/lib.js'

new Vue({
    el: 'form',
    components: {
        FoldUnfold
    },
    directives: {
        check: checkstate
    }
})
