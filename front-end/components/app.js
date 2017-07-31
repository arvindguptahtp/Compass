import FoldUnfold from './forms/fold-unfold.vue'
import { checkstate } from './forms/lib.js'
import Slideover from './modals/slideover.vue'

new Vue({
    el: 'form',
    components: {
        FoldUnfold
    },
    directives: {
        check: checkstate
    }
})


new Vue({
    el: '.search-river',
    components: {
        Slideover
    },
})

new Vue({
    el: '.card--ebr',
    components: {
        Slideover
    },
})

